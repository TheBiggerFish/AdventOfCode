# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/5


import re

naughty,nice = 0,0
with open('2015/05/input.txt') as f:
    for line in f:
        condition1 = len(re.findall(r'(\w)(\w).*\1\2',line)) >= 1
        condition2 = len(re.findall(r'(\w).\1',line)) >= 1
        if condition1 and condition2:
            nice += 1
        else:
            naughty += 1

print('There were {} nice strings and {} naughty strings'.format(nice,naughty))