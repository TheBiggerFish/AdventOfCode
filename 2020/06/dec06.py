# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/6



with open('2020/06/input.txt','r') as input_file:
    count_1,count_2 = 0,0
    group_1 = set()
    group_2 = set('abcdefghijklmnopqrstuvwxyz')

    for line in input_file:
        line = line.strip()
        if line:
            group_1 |= set(line)
            group_2 &= set(line)
        else:
            count_1 += len(group_1)
            count_2 += len(group_2)
            group_1 = set()
            group_2 = set('abcdefghijklmnopqrstuvwxyz')
    print(f'Group 1: {count_1}, Group 2: {count_2}')