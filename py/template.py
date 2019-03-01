import sys
import math
import random

lines = [l.strip() for l in reversed(sys.stdin.readlines())]

def read_int_arr():
    return map(int, lines.pop().split(" "))

def read_int():
    return int(lines.pop())

def read_str():
    return lines.pop()

def read_str_arr():
    return lines.pop().split(" ")

# begin code
