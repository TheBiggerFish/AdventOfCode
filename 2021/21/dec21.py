# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/21


class Player:
    def __init__(self,id:int,position:int,score:int=0):
        self.id = id
        self.position = position
        self.score = score

    def step(self,rolls:int):
        self.position += rolls
        self.position %= 10
        self.position = 10 if self.position == 0 else self.position

        self.score += self.position

with open('2021/21/input.txt') as f:
    p1_line,p2_line = f.read().splitlines()
p1 = Player(int(p1_line.split()[1]),int(p1_line.split()[-1]))
p2 = Player(int(p2_line.split()[1]),int(p2_line.split()[-1]))

which = 0
die = 1
while p1.score < 1000 and p2.score < 1000:
    rolls = die * 3 + 3
    die += 3
    if which%2 == 0:
        p1.step(rolls)
    else:
        p2.step(rolls)
    which += 1
print(min(p1.score,p2.score)*(die-1))
