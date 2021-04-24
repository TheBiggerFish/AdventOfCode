# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/15


class Disc:
    def __init__(self,id,start_pos,positions):
        self.id = id
        self.positions = positions
        self.start_pos = start_pos

    # def pass_time(self):
    #     self.pos += 1
    #     self.pos %= self.positions

    def valid_at_time(self,time):
        return (self.start_pos + time + self.id) % self.positions == 0

    @staticmethod
    def from_string(string):
        spl = string.split()
        return Disc(int(spl[1][1:]),int(spl[-1].strip('.')),int(spl[3]))

    def __str__(self):
        return f'Disc #{self.id} has {self.positions} positions; at time=0, it is at position {self.start_pos}.'

    # def __str__(self):
    #     return f'Disc #{self.id} has {self.positions} positions; at time={self.time}, it is at position {self.pos}.'

class Puzzle:
    def __init__(self,discs):
        self.discs = discs
        self.time = 0

    def pass_time(self):
        self.time += 1

    def solve(self):
        while not self.valid():
            self.pass_time()
        return self.time

    def valid(self):
        for i in range(len(self.discs)):
            disc = self.discs[i]
            if not disc.valid_at_time(self.time):
                return False
        return True


with open('2016/15/input2.txt') as f:
    discs = []
    for line in f:
        discs.append(Disc.from_string(line.strip()))
    p = Puzzle(discs)
    print(p.solve())