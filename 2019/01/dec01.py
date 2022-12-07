# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/1

def fuel_cost(m):
    return m // 3 - 2


def recursive_cost(weight):
    added = fuel_cost(weight)
    while added > 0:
        weight += added
        added = fuel_cost(added)
    return weight


with open('2019/01/input.txt') as f:
    modules = map(int, f.read().split())
    tanks = list(map(fuel_cost, modules))
    print(f'Initial fuel required is {sum(tanks)}')

    fuel = map(recursive_cost, tanks)
    print(f'Total fuel required is {sum(fuel)}')
