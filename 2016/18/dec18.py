# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/18


row = '^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.'
num_rows = 400000
grid = []

def next_row(row):
    new_row = ''
    for i in range(len(row)):
        left = i-1 >= 0 and row[i-1] == '^'
        center = row[i] == '^'
        right = i+1 < len(row) and row[i+1] == '^'
        if left and center and not right:
            new_row += '^'
        elif not left and center and right:
            new_row += '^'
        elif left and not center and not right:
            new_row += '^'
        elif not left and not center and right:
            new_row += '^'
        else:
            new_row += '.'
    return new_row

count = 0
for i in range(num_rows):
    count += len(list(filter(lambda c: c == '.',row)))
    row = next_row(row)
    
print(f'There are {count} safe tiles')

