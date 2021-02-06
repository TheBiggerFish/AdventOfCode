# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/5


naughty,nice = 0,0
with open('2015/05/input.txt') as f:
    for line in f:
        if len(''.join(list(filter(lambda x: x in 'aeiou',line)))) < 3:
            naughty += 1
        elif 'ab' in line or 'cd' in line or 'pq' in line or 'xy' in line:
            naughty += 1
        else:
            while len(line) > 1 and line[0] != line[1]:
                line = line[1:]
            if len(line) == 1:
                naughty += 1
            else:
                nice += 1

print('There were {} nice strings and {} naughty strings'.format(nice,naughty))