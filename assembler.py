#!/usr/bin/env python
#encoding:UTF-8

__author__ = "Daniel Oelschlegel"
__version__ = "0.01"
__license__ = "bsdl"

from __future__ import print_function
from sys import argv

def main(file_name):
    pass

def usage():
    print(__file__.splitext(".py"), __version__, "--", __author__)
    print("\nUsage: filename.4dg");

if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        usage()