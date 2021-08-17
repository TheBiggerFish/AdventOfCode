# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/19


from fishpy.structures import Cycle

input = 3001330

def largest_power_of_two(num):
    pow_two = 1
    while pow_two < num:
        pow_two <<= 1
    return pow_two >> 1

print(f'The elf who receives all of the presents is elf {2*(input-largest_power_of_two(input))+1}')


elves = Cycle(range(input))

elf = 0
while len(elves) > 1:
    dead = (elf + len(elves)//2) % len(elves)
    if len(elves) % 10**4 == 0:
        print(f'{dead}/{len(elves)}')
    del elves[dead]
    if dead < elf:
        elf -= 1
    elf = (elf+1) % len(elves)
    
print(elves[0]+1)
    