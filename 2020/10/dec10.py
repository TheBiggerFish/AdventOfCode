# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/10


from functools import lru_cache

with open('2020/10/input.txt','r') as input_file:
    numbers = [0] + sorted([int(line.strip()) for line in input_file])
target = max(numbers)+3

ones,threes = 0,1
for i in range(len(numbers)-1):
    if numbers[i+1]-numbers[i] == 1:
        ones += 1
    elif numbers[i+1]-numbers[i] == 3:
        threes += 1
print('Result 1:', ones*threes)


@lru_cache(maxsize=1000)
def recurse(previous:int):
    global target,numbers

    if previous < 0:
        return sum(recurse(i) for i in range(0,3) if numbers[i] <= 3)

    if 0 < target-numbers[previous] <= 3:
        return 1

    return sum(recurse(i) for i in range(previous+1,min(len(numbers),previous+4)) if numbers[i]-numbers[previous] <= 3)

print('Result 2:', recurse(0))