# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/9


with open('2016/09/input.txt') as f:
    string = f.read().strip()
    index = 0
    values = [1 for _ in range(len(string))]

    while index < len(string):
        if string[index] == '(':
            past = string.find(')',index) + 1
            match = string[index:past]
            marker = [int(x) for x in match.strip('()').split('x')]
            for x in range(index,past):
                values[x] = 0
            for x in range(past,past+marker[0]):
                values[x] *= marker[1]
            index = past
        else:
            index += 1

    print(f'The length of the file after uncompressing with the second method is {sum(values)}')

