# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/7


# 1674 -> b
# 46065 -> b

class Operation:
    def __init__(self,op,right,left=None):
        self.op = op
        self.right = right
        self.left = left

    def reduce(self):
        if isinstance(self.left,Operation):
            self.left = self.left.reduce()
        if isinstance(self.right,Operation):
            self.right = self.right.reduce()
        if self.op == 'AND':
            return self.left & self.right
        if self.op == 'OR':
            return self.left | self.right
        if self.op == 'LSHIFT':
            return self.left << self.right
        if self.op == 'RSHIFT':
            return self.left >> self.right
        if self.op == 'NOT':
            return ~self.right
        if self.op == 'PASS':
            return self.right
        raise ValueError('Operation must have an op to reduce')

wires = {}
with open('2015/07/input.txt') as f:
    for line in f:
        line = line.strip().split(' ')
        if len(line) == 3:
            op = 'PASS'
            left = None
            right = line[0]
        elif len(line) == 4:
            op = line[0]
            left = None
            right = line[1]
        elif len(line) == 5:
            op = line[1]
            left = line[0]
            right = line[2]
        else:
            raise ValueError('Line does not contain correct number of parts: {}'.format(line))
        wires[line[-1]] = Operation(op,right,left)
    for wire in wires:
        wire = wires[wire]
        if isinstance(wire.left,str):
            if wire.left.isdecimal():
                wire.left = int(wire.left)
            else:
                wire.left = wires[wire.left]
        if isinstance(wire.right,str):
            if wire.right.isdecimal():
                wire.right = int(wire.right)
            else:
                wire.right = wires[wire.right]

print('The output of wire \'a\' is {}'.format(wires['a'].reduce()))