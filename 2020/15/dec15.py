# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/15


puzzle_input = [8,11,0,19,1]
last_number = 2
target = 30000000

numbers = {}
for i,item in enumerate(puzzle_input,start=1):
    numbers[item] = i

start = len(puzzle_input) + 1
for turn in range(start,target + 1):
    if last_number in numbers:
        last_seen = turn - numbers[last_number]
    else:
        last_seen = 0
    numbers[last_number] = turn
    last_number = last_seen
target_number = sorted(numbers,key=lambda item: numbers[item])[-1]
print(target_number)