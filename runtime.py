#!/usr/bin/env python
#encoding:UTF-8

from __future__ import print_function
from os.path import exists, splitext, split
import pygame
from pygame.locals import QUIT
from sys import argv, exit
from Poga import INSTRUCTION, BUILTIN, zeroleaded_hex_str

__author__ = "Daniel Oelschlegel"
__version__ = "0.01"
__license__ = "bsdl"


FONTS = ["monospace",""]

resolution = 128, 128

STACK_SIZE = 128
MEM_BASE = 0x8000
#compiler limit/EVE or hardware?
MAX_VARIABLES = 0xFF
#EVE memory
LOCAL_OFFSET = 0x180 + 0x80
#complete memory, local variable stored after stack(hack)
MAX_MEMORY_SIZE = LOCAL_OFFSET + MAX_VARIABLES
#EVE stack upwards
STACK_OFFSET = 0x180 - 1
#pscontent of the stack pointer in EVE
SP = 128
#offset of user variables
VAR_OFFSET = 129
VM_RETVAL = 0x51
VM_OVERFLOW = 0x50

def usage():
    print(split(splitext(__file__)[0])[1], __version__, "--", __author__)
    print("\nUsage: filename.bin");

def for_aborting():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

class Poga(object):
    def __init__(self, data, file_name):
        self._data = data
        self._ip = 0
        #two times because global and local in one
        self._memory = [0x0000] * MAX_MEMORY_SIZE
        self._zero_flag = False
        pygame.init()
        pygame.display.set_caption(file_name.split(".")[0])
        self._surface = pygame.display.set_mode(resolution, pygame.RESIZABLE, 24)

    def run(self, start=0):
        self._ip = start
        while self._ip < len(self._data):
            instruction_name, size = INSTRUCTION[ord(self._data[self._ip])]
            param = zeroleaded_hex_str(self._data[self._ip + 1: self._ip + size][::-1])
            if instruction_name == "END":
                return
            print(hex(self._ip), "_%s" % instruction_name, param, )
            getattr(self, "_%s" % instruction_name.lower())(param)
            self._ip += size
            for_aborting()

    def _push_funcaddr(self, param):
        self._add_to_stack(int(param, 16))

    def top_from_stack(self):
        return self._memory[self._memory[SP]]

    def _remove_from_stack(self):
        value = self._memory[STACK_OFFSET + self._memory[SP]]
        self._memory[SP] = max(0, self._memory[SP] - 1)
        return value

    def _add_to_stack(self, value):
        self._memory[STACK_OFFSET + self._memory[SP] + 1] = value
        self._memory[SP] = min(STACK_SIZE, self._memory[SP] + 1)

    def _call_no(self, param):
        #get arguments
        arg_count = int(param, 16)
        parameter = []
        for index in range(arg_count):
            parameter.append(self._remove_from_stack())
        address = self._remove_from_stack()
        if address < 128 * 256:
            self._add_to_stack(self._ip + len(param) / 2 + 1)
            self._add_to_stack(int(param, 16))
            self._ip = address - (len(param) / 2 + 1)
        else:
            getattr(self, "_%s" % BUILTIN[address].lower())(parameter)

    def _peekw(self, parameter):
        #TODO word or byte, limits, organisation
        self._add_to_stack(self._memory[parameter[0]])

    def _peekb(self, parameter):
        #TODO word or byte, limits, organisation
        self._add_to_stack(self._memory[parameter[0]])

    def _pokew(self, parameter):
        #TODO word or byte, limits, organisation
        self._memory[parameter[0]] = parameter[1]

    def _pokeb(self, parameter):
        #TODO word or byte, limits, organisation
        self._memory[parameter[0]] = parameter[1]

    def _ass_loc(self, param):
        self._add_to_stack("L%s" % param)

    def _ass_glob(self, param):
        self._add_to_stack("G%s" % param)

    def _push(self, param):
        self._add_to_stack(int(param, 16))

    def _load_glovar(self, param):
        self._add_to_stack(self._memory[VAR_OFFSET +  + int(param, 16)])

    def _and(self, param):
        pass

    def _or(self, param):
        pass

    def _xor(self, param):
        pass

    def _neg(self, param):
        pass

    def _shl(self, param):
        pass

    def _shr(self, param):
        pass

    def _inc(self, param):
        pass

    def _dec(self, param):
        pass

    def _add(self, param):
        pass

    def _sub(self, param):
        pass

    def _div(self, param):
        pass

    def _mul(self, param):
        pass

    def _mod(self, param):
        pass


    def comparision(self):
        return self._remove_from_stack(), self._remove_from_stack()

    def _cmp_l(self, param):
        #TODO check changed order because naming left, right
        left, right = self.comparision()
        self._zero_flag = left < right

    def _cmp_g(self, param):
        #TODO check changed order because naming left, right
        left, right = self.comparision()
        self._zero_flag = left > right

    def _cmp_ge(self, param):
        #TODO check changed order because naming left, right
        left, right = self.comparision()
        self._zero_flag = left >= right

    def _cmp_le(self, param):
        #TODO check changed order because naming left, right
        left, right = self.comparision()
        self._zero_flag = left <= right

    def _cmp_e(self, param):
        #TODO check changed order because naming left, right
        self._zero_flag = not self._cmp_ne(param)

    def _cmp_ne(self, param):
        #TODO check changed order because naming left, right
        left, right = self.comparision()
        self._zero_flag = left != right


    def _jump_zns(self, param):
        if not self._zero_flag:
            self._ip = int(param, 16) - (len(param) / 2 + 1)

    def _jump_zs(self, param):
        if self._zero_flag:
            self._ip = int(param, 16) - (len(param) / 2 + 1)

    def _push_str(self, param):
        str_len = int(param, 16)
        self._add_to_stack("".join(self._data[self._ip + 2: self._ip + str_len + 1]))
        self._ip += str_len - (len(param)/2 + 1)

    def _putstr(self, param):
        arg_count = int(param, 16)
        for index in range(arg_count):
            #self._surface
            text = self._remove_from_stack()
            self._memory[VM_RETVAL] = len(text)
            self.output(text)

    def _print(self, param):
        #TODO: param[0] always 0x50A, what does this mean??
        for element in param[1:]:
            self._simple_output(element)


    def _jump(self, param):
        self._ip = int(param, 16) - (len(param) / 2 + 1)

    def _push_retval(self, param):
        self._add_to_stack(self._memory[VM_RETVAL])

    def _end(self, param):
        #processed in the main loop
        pass

    def _write_var(self, param):
        value = self._remove_from_stack()
        entry = self._remove_from_stack()
        var_type, memory_index = entry[0], int(entry[1:], 16)
        self._memory[(VAR_OFFSET if var_type == "G" else LOCAL_OFFSET) + memory_index] = value

    def _ret(self, param):
        #FIXME: different behaviour internal function call and own function
        #solution: own address with prefix
        #self._ip = self._remove_from_stack()
        pass



    def _simple_output(self, text):
        position = (self._memory[0x64], self._memory[0x64])
        fgcolor = self._memory[0x55]
        font, font_size = self._memory[0x88], self._memory[0x8c]
        self._gfx_output(text, position, fgcolor, font, font_size)

    def _gfx_output(self, text, position, color, font, font_size):
        font_name = FONTS(font)
        self._surface.blit(self._surface.font.SysFont(font_name, font_size).render(text, 1, color), position)
        self._surface.display.flip()

def main(file_name):
    with open(file_name, "rb") as blob:
        Poga(blob.read(), split(file_name)[1]).run()
        while True:
            for_aborting()

if __name__ == "__main__":
    main(main(r"C:\programmieren\4dgl\POGA INTRO\HELLO WORLD\HELLO WORLD.bin"))#argv[1])
    if len(argv) == 2 and exists(argv[1]):
        main(argv[1])
    else:
        usage()