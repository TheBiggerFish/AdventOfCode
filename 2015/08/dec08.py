# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/8


from re import sub

total_code = 0
total_string = 0

with open('2015/08/input.txt') as f:
    for line in f:
        line = line.strip()
        total_code += len(line)
        string = line.replace('\\\"','\"').replace('\\\\','\\')[1:-1]
        string = sub(r"\\x..","?",string)
        total_string += len(string)
        # print(len(line),len(string),line,string)

print('The number of characters of code minus the number of characters in memory is {} - {} = {}'.format(total_code,total_string,total_code-total_string))