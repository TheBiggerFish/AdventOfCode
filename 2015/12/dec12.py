# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/12


def recursive_sum(data):
    if isinstance(data,int):
        return data
    if isinstance(data,str):
        return 0
    if isinstance(data,list):
        return(sum([recursive_sum(datum) for datum in data]))
    if isinstance(data,dict):
        red_value = sum([True for which in data if data[which] == 'red'])
        if red_value > 0:
            return 0
        return(sum([recursive_sum(data[which]) for which in data if 'red' not in data]))
    raise(TypeError(type(data),'can not be used for recursive sum:',data))

import json
with open('2015/12/input.json') as f:
    data = json.load(f)
    print('The total sum of integers when ignoring maps with the value "red" is {}'.format(recursive_sum(data)))
