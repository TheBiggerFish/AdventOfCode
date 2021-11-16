# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/2


from fishpy.structures import Range

with open('2020/02/input.txt') as f:
    count1,count2 = 0,0
    for line in f:
        split = line.strip().split()
        range = Range.from_string(split[0],upper_inclusive=True)
        char = split[1][0]
        string = split[2]

        if string.count(char) in range:
            count1 += 1
        sub_string = string[range.lower-1] + string[range.upper-1]
        if sub_string.count(char) == 1:
            count2 += 1
    print(f'There are {count1} valid passwords in the list using sled policy')
    print(f'There are {count2} valid passwords in the list using toboggan policy')

