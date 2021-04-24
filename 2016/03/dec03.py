# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/3


with open('2016/03/input.txt') as in_file:
    lines = [[int(side) for side in line.strip().split()] for line in in_file.readlines()]
    num_h,num_v = 0,0
    for tri in lines:
        if tri[0] + tri[1] > tri[2]:
            num_h += 1
    for col in range(3):
        for row in range(0,len(lines),3):
            tri = sorted([lines[row][col],lines[row+1][col],lines[row+2][col]])
            if tri[0] + tri[1] > tri[2]:
                num_v += 1
    print(f'The number of proper triangles horizontally is {num_h}, and vertically is {num_v}.')