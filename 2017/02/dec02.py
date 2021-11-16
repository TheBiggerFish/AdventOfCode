# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/2


from typing import List


def get_row_difference(row:List[int]):
    return max(row) - min(row)

def get_row_dividend(row:List[int]):
    for i,n1 in enumerate(row):
        for _,n2 in enumerate(row[i+1:],start=i+1):
            if n1%n2 == 0:
                return n1//n2
            if n2%n1 == 0:
                return n2//n1
    raise Exception('No dividend on row')

with open('2017/02/input.txt') as in_file:
    spreadsheet = []
    for line in in_file.read().splitlines():
        row = []
        for col in line.strip().split():
            row.append(int(col))
        spreadsheet.append(row)

sum_1 = sum([get_row_difference(row) for row in spreadsheet])
print(f'The solution to part 1 is: {sum_1}')
sum_2 = sum([get_row_dividend(row) for row in spreadsheet])
print(f'The solution to part 2 is: {sum_2}')
