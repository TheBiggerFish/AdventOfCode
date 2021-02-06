# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/2


sum_paper,sum_ribbon = 0,0
with open('2015/02/input.txt') as f:
    for line in f:
        dim = line.strip().split('x')
        dim = tuple(map(lambda x: int(x),dim))
        sum_paper += 2 * (dim[0]*dim[1] + dim[1]*dim[2] + dim[2]*dim[0]) + min(dim[0]*dim[1],dim[1]*dim[2],dim[2]*dim[0])
        sum_ribbon += 2* min(dim[0]+dim[1],dim[1]+dim[2],dim[2]+dim[0]) + dim[0]*dim[1]*dim[2]

print('The elves will need {} sq. feet of wrapping paper and {} feet of ribbon.'.format(sum_paper,sum_ribbon))