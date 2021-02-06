# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/6


size = 1000
grid = [[0 for _ in range(size)] for _ in range(size)]

with open('2015/06/input.txt') as f:
    for line in f:
        line = line.strip().split(' ')
        if line[0] == 'toggle':
            lower = tuple(map(int,line[1].split(',')))
            upper = tuple(map(int,line[3].split(',')))
            for x in range(lower[0],upper[0]+1):
                for y in range(lower[1],upper[1]+1):
                    grid[y][x] += 2
        else:
            lower = tuple(map(int,line[2].split(',')))
            upper = tuple(map(int,line[4].split(',')))
            for x in range(lower[0],upper[0]+1):
                for y in range(lower[1],upper[1]+1):
                    grid[y][x] = max(grid[y][x] + (line[1] == 'on') * 2 - 1,0)

lit = sum([light for row in grid for light in row])
print('There total brightness level is {}'.format(lit))