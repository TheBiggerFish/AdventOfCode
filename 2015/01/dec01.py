# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/1


floor = 0
count = 0
done = False
with open('2015/01/input.txt') as f:
    instructions = f.readline().strip()
    for char in instructions:
        count += 1
        if char == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1 and not done:
            done = True
            print(count)
print(floor)
