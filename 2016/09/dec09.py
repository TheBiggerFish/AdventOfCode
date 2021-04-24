# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/9


import re

with open('2016/09/input.txt') as f:
    comp = f.read().strip()
    uncomp1 = ''
    while comp != '':
        search = re.search(r'\(\d+x\d+\)',comp)
        match = [int(x) for x in search.group().strip('()').split('x')]
        comp = comp[len(search.group()):]
        uncomp1 += comp[:match[0]]*match[1]
        comp = comp[match[0]:]
        # if (search := re.search(r'\(\d+x\d+\)',comp)) != None:
        #     step = search.start()
    print(f'The length of the file after uncompressing with the first method is {len(uncomp1)}')
    # print(f'The length of the file after uncompressing with the second method is {len(uncomp2)}')