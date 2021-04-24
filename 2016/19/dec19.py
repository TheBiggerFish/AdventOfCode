# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/19


input = 3001330

def largest_power_of_two(num):
    pow_two = 1
    while pow_two < num:
        pow_two <<= 1
    return pow_two >> 1

print(f'The elf who receives all of the presents is elf {2*(input-largest_power_of_two(input))+1}')