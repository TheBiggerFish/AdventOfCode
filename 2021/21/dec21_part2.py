# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/21

from functools import lru_cache
from collections import Counter
from itertools import product

class Player:
    def __init__(self,position:int,score:int=0):
        self.position = position
        self.score = score

    def step(self,rolls:int):
        self.position += rolls
        self.position %= 10
        if self.position == 0:
            self.position = 10
        self.score += self.position
        return self

    def copy(self) -> 'Player':
        return Player(self.position,self.score)

    def __repr__(self) -> str:
        return f'Player({self.position},{self.score})'

    def __eq__(self,other:'Player') -> bool:
        return self.position == other.position and self.score == other.score

    def __hash__(self):
        return hash((self.position,self.score))

TARGET_SCORE = 21
DIRAC_ROLLS = Counter(d1+d2+d3 for d1,d2,d3 in product([1,2,3],repeat=3))

@lru_cache(maxsize=None)
def play_dice(p1:Player,p2:Player,turn:bool) -> tuple[int,int]:
    if p1.score >= TARGET_SCORE:
        return 1,0
    if p2.score >= TARGET_SCORE:
        return 0,1

    p1_wins,p2_wins = 0,0
    for roll,freq in DIRAC_ROLLS.items():
        if turn:
            scores = play_dice(p1.copy().step(roll),p2,False)
        else:
            scores = play_dice(p1,p2.copy().step(roll),True)
        p1_wins += scores[0] * freq
        p2_wins += scores[1] * freq

    return p1_wins,p2_wins


with open('2021/21/input.txt') as f:
    p1_line,p2_line = f.read().splitlines()
p1 = Player(int(p1_line.split()[-1]))
p2 = Player(int(p2_line.split()[-1]))

print(play_dice(p1,p2,True))