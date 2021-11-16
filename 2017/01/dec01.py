# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/1


from fishpy.structures import Cycle

with open('2017/01/input.txt') as in_file:
    cycle = Cycle(''.join(in_file.read().split()))
    for i,_ in enumerate(cycle):
        cycle[i] = int(cycle[i])

sum_1,sum_half = 0,0
for i,n in enumerate(cycle):
    if n == cycle[i+1]:
        sum_1 += n
    if n == cycle[i+len(cycle)//2]:
        sum_half += n
print(f'The solution to part 1 is {sum_1}')
print(f'The solution to part 2 is {sum_half}')
