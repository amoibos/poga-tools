#!/usr/bin/env python
#encoding:UTF-8

from __future__ import print_function
from sys import argv
from os.path import splitext, exists, split
import serial
from time import sleep
from math import ceil
from struct import pack

__author__ = "Daniel Oelschlegel"
__version__ = "0.01"
__license__ = "bsdl"

def preheat(port):
    try:
        ser = serial.Serial(port, timeout=1)
    except serial.serialutil.SerialException:
        print("couldn\'t establish a serial connection")
        print("possible reasons:\n\twrong serial port\n\tswitch off/on your device\n\tunplug and plug the device" +
              "\n\treboot if driver crashed")
    ser.setDTR(True)
    sleep(0.2)
    ser.setDTR(False)
    sleep(0.2)
    write_with_response(ser, "4dgl", "G", 0.2)
    ser.write("@V")
    print(ser.read())
    ser.write("@D")
    #response = ser.read(ser._in_waiting())
    ser.write("E")
    ser.close()

def firmware_upload(data, port, speed):
    '''uploads firmware as a PmmC'''
    
    CHUNK_SIZE, ACK = 256, "\x06"
    chunk_amount = len(data) / CHUNK_SIZE
    preheat(port)
    ser = connect(data, port, speed, True)
    print("sending commands")
    error = ""
    for _ in range(3):
        response = write_with_response(ser, "4DGL", "4dgl", 0.5)
        #sleep(1)
        if response:
            break
    if response:
        print("flashing:", end="")
        if not write_with_response(ser, "e", ""):
            for index in range(chunk_amount - 1, -1, -1):
                chunk = "".join(data[index * CHUNK_SIZE: (index + 1) * CHUNK_SIZE])
                checksum = -sum(map(ord, chunk)) & 0xFF
                block = "p%s%s%c" % (pack("H", index), chunk, checksum)
                if write_with_response(ser, block, ACK, 1):
                    print(".", end="")
                else:
                    print("stopped flashing because of missing ACK")
                    break
            print("\n")
        else:
            error = "no response on flashing command"
    else:
        error = "device has not responded"
    if error:
        print("communication error:", error)            
    print("closing port")
    ser.close()
        
def write_with_response(ser, command, expected, time=0.1):
    '''writing messages to device and check the expected answer with waiting time'''
    ser.write(command)
    sleep(time)
    response = ser.read()
    print(response)
    return expected == response
        
def connect(data, port, speed, firmware=False):
    '''connect to the device, causes a reset for a terminal session'''
    print("opening port %s with baudrate of %d" % (port, speed))
    try:
        ser = serial.Serial(
            port=port,
            baudrate=speed,
            #dsrdtr=0,
            #rtscts=0,
            #xonxoff=1,
            timeout=1)
    except serial.serialutil.SerialException:
        print("couldn\'t establish a serial connection")
        print("possible reasons:\n\twrong serial port\n\tswitch off/on your device\n\tunplug and plug the device"+
              "\n\treboot if driver crashed")
        exit(-1)

    if firmware:
        ser.setRTS(False)
    #    ser.setDTR(False)
    #    ser.flushInput()
    #    ser.flushOutput()
    ser.setDTR(True)
    ser.setDTR(False)
    if not firmware:
        ser.flushInput()
        ser.flushOutput()
    return ser

def program_upload(data, port, speed):
    '''transfer data to given port'''
    
    CHUNK_SIZE, ACK = 64, "\0"
    ser = connect(data, port, speed)
    print("sending commands")
    for _ in range(3):
        response = write_with_response(ser, "4dgl", "G")
        if response:
            break
    if response:
        ser.write("L%c" % int(ceil(len(data) / (CHUNK_SIZE * 1.0))))
        response = ser.read()
        print("transferring:", end="")
        for start in range(0, len(data), CHUNK_SIZE):
            chunk = data[start: start + CHUNK_SIZE]
            if len(chunk) < CHUNK_SIZE:
                chunk = chunk.ljust(CHUNK_SIZE, '\xFF')
            checksum = -sum(map(ord, chunk)) & 0xFF
            if write_with_response(ser, chunk + chr(checksum), ACK):
                print(".", end="")
            else:
                print("transferring stopped because of missing ACK")
                break
        print("\n")
    else:
        print("communication error by initialisation")
    print("closing port")
    ser.close()

def main(file_name, port, speed):
    upload = firmware_upload if splitext(file_name)[1].lower() == ".pmmc" else program_upload
    print("uploading", "firmware" if upload == firmware_upload else "program")
    with open(file_name, "rb") as binary:
        upload(binary.read(), port, speed)

def usage():
    print(split(splitext(__file__)[0])[1], __version__, "--", __author__)
    print("\nUsage: filename portnumber [baudrate]")

if __name__ == "__main__":
    main(r"C:\Users\daoe\poga\PoGa-R01.PmmC", "com1", 115200)
    exit()
    if 3 <= len(argv) <= 4 and exists(argv[1]):
        speed = 115200
        if len(argv) == 4:
            try:
                speed = int(argv[3])
            except ValueError:
                pass
        main(argv[1], argv[2], speed)
    else:
        usage()