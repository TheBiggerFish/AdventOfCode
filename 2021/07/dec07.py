# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/7


from functools import lru_cache

@lru_cache
def fuel_use(distance:int) -> int:
    total = 0
    for i in range(1,distance+1):
        total += i
    return total

with open('2021/07/input.txt') as f:
    line = f.read().rstrip().split(',')
    positions = [int(entry) for entry in line]
    min_,max_ = min(positions),max(positions)

    min_fuel = float('inf')
    for i in range(min_,max_+1):
        total = 0
        for position in positions:
            # total += abs(i-position)
            total += fuel_use(abs(i-position))
        if total < min_fuel:
            min_fuel = total
    print(min_fuel)