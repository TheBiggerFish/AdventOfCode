# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/14


import re
from hashlib import md5

input = 'cuanljph'

class MD5:
    def __init__(self,string:str,i:int,stretch=0):
        self.plaintext = string+str(i)
        self.id = i
        self.hash = MD5.hash(self.plaintext,stretch)
        # self.hash = str(md5(self.plaintext.encode()).hexdigest())
        self.threes = set(re.findall(r'(\w)\1\1',self.hash)[:1])
        self.fives = set(re.findall(r'(\w)\1\1\1\1',self.hash))
        self.found = None

    @staticmethod
    def hash(string,stretch=0):
        for _ in range(stretch+1):
            string = str(md5(string.encode()).hexdigest())
        return string

recent = []
i = 0
keys = 0
while True:
    cur = MD5(input,i,stretch=2016)
    while len(recent) != 0 and i - recent[0].id > 1000:
        top = recent[0]
        recent = recent[1:]
        if top.found:
            keys += 1
            print(f'Key {keys}: ID {top.id} generated {top.hash} matched with ID {top.found.id} hash {top.found.hash}')
        if keys == 64:
            print(top.id)
            exit()
    for item in recent:
        for three in item.threes:
            if three in cur.fives:
                item.found = cur
    if len(cur.threes) != 0:
        recent.append(cur)

    i += 1
