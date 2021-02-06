# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/5


import re
from functools import reduce


def and_reduce(a,b):
    return a and b

naughty,nice = 0,0
with open('2015/05/input.txt') as f:
    for line in f:
        condition1 = reduce(and_reduce,[])
        condition2 = re.search()
        if condition1 and condition2:
            nice += 1
        else:
            naughty += 1
        

print('There were {} nice strings and {} naughty strings'.format(nice,naughty))