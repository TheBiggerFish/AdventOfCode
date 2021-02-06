# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/3


SANTAS = 2
pos = [[0,0] for _ in range(SANTAS)]
turn = 0
visited = {}
with open('2015/03/input.txt') as f:
    line = f.readline().strip()
    for char in line:
        who = turn % SANTAS
        if char == '^':
            pos[who][1] += 1
        elif char == 'v':
            pos[who][1] -= 1
        elif char == '>':
            pos[who][0] += 1
        elif char == '<':
            pos[who][0] -= 1

        tup = tuple(pos[who])
        if tup not in visited:
            visited[tup] = 0
        visited[tup] += 1
        turn += 1

print('{} alternating Santas visited {} houses'.format(SANTAS,len(visited)))