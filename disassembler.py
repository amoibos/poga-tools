#!/usr/bin/env python
#encoding:UTF-8

from __future__ import print_function
from sys import argv
from os.path import exists
from Poga import INSTRUCTION, BUILTIN, zeroleaded_hex_str
from os.path import splitext, split

__author__ = "Daniel Oelschlegel"
__version__ = "0.02"
__license__ = "bsdl"

DATA_START = 7
  
def interpret(data, position, is_code_segment):
    '''opcode evaluation'''
    if is_code_segment:
        instruction_name, size = INSTRUCTION[ord(data[position])]
        #little endian architecture
        param = zeroleaded_hex_str(data[position + 1: position + size][::-1])
        if instruction_name == "PUSH_STR":
            size += int(param, 16)
            param = "\'%s\'" % "".join(data[position + 2: position + size - 1])
            param = "".join([ch if ord(ch) > 31 else " " for ch in param])
        elif  instruction_name == "PUSH_FUNCADDR":
            number = int(param, 16)
            try:
                param = "__%s" % BUILTIN[number].upper()
            except KeyError:
                #internal label jump
                if number < 256 * 128:
                    param = "LBL%s" % param
        elif instruction_name in ("JUMP_ZNS", "JUMP_ZS", "JUMP"):
            param = "LBL%s" % param
        return instruction_name, param, size
    
    return "CONST", "", 1

def string_limit(text, limit):
    if len(text) > limit:
        return "%s.." % text[:limit - 2]
    return text
    
def decode(data):
    '''decoder loop which creates outputs'''
    lines, instruction_pointer, label, main_entry, code_table = [], 0, {}, -1, {}
    print("ADDRESS", "CODE\t".rjust(22), "INSTRUCTION\n%s" % ("-" * 65))
    while instruction_pointer < len(data):
        instruction_name, parameter, size = interpret(data, instruction_pointer, 
                                                instruction_pointer < DATA_START or instruction_pointer >= main_entry)
        #data segment all between opcode call main and main label
        if DATA_START <= instruction_pointer < main_entry:
            size = 2 if instruction_pointer + 2  <= main_entry else 1
            parameter, code = "", zeroleaded_hex_str(data[instruction_pointer: instruction_pointer + size])
        #collect jump marks
        if instruction_name in ("JUMP_ZNS", "JUMP_ZS", "JUMP", "PUSH_FUNCADDR"):
            if not parameter.startswith("__"):
                try:
                    number = int(parameter.split("LBL")[1], 16)
                except IndexError:
                    number = int(parameter, 16)
                if main_entry == -1:
                    main_entry = number
                #internal labels, no variable or firmware function
                if number < 128 * 256 and data[instruction_pointer + size] != 0x17:
                    label[number] = 0
        code_table[instruction_pointer] = len(lines)
        #output: LINE NUMBER | LBL*     HEX STRING      INSTRUCTION NAME       OPTIONAL ARGUMENT
        hex_str = string_limit(zeroleaded_hex_str(data[instruction_pointer:  instruction_pointer + size]).rjust(24), 24)
        lines.append("%04X\t%s\t%s\t" % (instruction_pointer, hex_str,
                                                        ("%s %s" % (instruction_name, parameter if parameter else ""))))
        instruction_pointer += size
    #replace collected line number to label
    for label_item, _ in label.items():
        lines[code_table[label_item]]= "LBL%04X    %s" % (label_item, lines[code_table[label_item]][8:])
    return lines
    
def main(file_name):
    with open(file_name, "rb") as blob:
        for line in decode(blob.read()):
            print(line)
        
def usage():
    '''prints help text'''
    print(split(splitext(__file__)[0])[1], __version__, "--", __author__)
    print("\nUsage: filename.bin");

if __name__ == "__main__":
    if len(argv) == 2 and exists(argv[1]):
            main(argv[1])
    else:
        usage()
