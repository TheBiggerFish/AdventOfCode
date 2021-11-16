# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/4


import re

LOWER = 372304
UPPER = 847060


def asc(num:int) -> bool:
    string = str(num)
    for i in range(len(string)-1):
        if int(string[i]) > int(string[i+1]):
            return False
    return True

def double(num:int) -> bool:
    return len(re.findall(r'(\w)\1',str(num))) >= 1

def double_not_triple(num:int) -> bool:
    return len(re.findall(r'(\w)\1[^\1]',str(num))) >= 1

count1,count2 = 0,0
for i in range(LOWER,UPPER):
    if asc(i):
        if double(i):
            count1 += 1
        if double_not_triple(i):
            count2 +=1
print(count1,count2)