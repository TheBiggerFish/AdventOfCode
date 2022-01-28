# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/1


with open('2021/01/input.txt') as f:
    str_depths = f.read().rstrip().split()
    depths = list(map(int,str_depths))

increases = 0
for i,d1 in enumerate(depths):
    if i == len(depths)-1:
        break
    d2 = depths[i+1]
    if d1 < d2:
        increases += 1

print(f'The submarine depth increases {increases} times')


increases = 0
old_window = sum(depths[0:2])
for i in range(3,len(depths)):
    new_window = sum(depths[max(0,i-2):i+1])
    if new_window > old_window:
        increases += 1
    old_window = new_window

print(f'The submarine sliding window depth increases {increases} times')
