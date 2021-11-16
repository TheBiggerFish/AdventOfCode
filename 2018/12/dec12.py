# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/12

input = '2018/12/input.txt'
generations = 20

from typing import Dict
    
class Terrarium:
    def __init__(self,initial_state:str,rules:Dict[str,str]):
        self.state = initial_state
        self.negative_state = ''
        self.rules = rules
        self.offset = 0

    def pass_time(self):
        next = '.'
        for i in range(len(self.state)):
            if i < 2:
                cur = self.state[:i+3].rjust(5,'.')
            elif i >= len(self.state) - 3:
                cur = self.state[i-2:].ljust(5,'.')
            else:
                cur = self.state[i-2:i+3]
            next += self.rules[cur]
        return next

with open(input) as f:
    initial_state = f.readline().strip().split(': ')[1]
    f.readline()

    rules = dict(tuple(line.strip().split(' => ')) for line in f)
    
    t = Terrarium(initial_state,rules)
    for i in range(generations):
        print(f'{str(i).rjust(2," ")}: {t.state}')
        t.state = t.pass_time()
    print(f'{str(i+1).rjust(2," ")}: {t.state}')