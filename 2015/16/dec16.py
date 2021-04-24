# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/16


class Sue:
    def __init__(self,id,properties):
        self.properties = {}
        self.id = id
        for p in properties:
            self.properties[p[0]] = int(p[1])

    def __eq__(self,other):
        return sum([self.properties[p1]!=other.properties[p2] for p1 in self.properties for p2 in other.properties if p1 == p2]) == 0

    def __str__(self):
        return 'Sue {}: '.format(self.id) + ', '.join(['{}: {}'.format(p,self.properties[p]) for p in self.properties])

    @staticmethod
    def from_string(string):
        split = ' '.join([sub.strip(',:\n ') for sub in string.split(' ')]).split(' ')
        return Sue(split[1],[(split[i],split[i+1]) for i in range(2,len(split),2)])



with open('2015/16/target.txt') as f:
    goal = Sue.from_string(f.readline())
with open('2015/16/input.txt') as f:
    for line in f:
        sue = Sue.from_string(line)
        if sue == goal:
            print(sue.id)

