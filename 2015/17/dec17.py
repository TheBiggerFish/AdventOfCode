# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/17



LITERS = 150
INPUT_FILE = '2015/17/input.txt'


def fill_containers(containers,amount):
    if amount == 0:
        return 1
    if amount < 0 or len(containers) == 0:
        return 0
    return fill_containers(containers[:-1],amount) + fill_containers(containers[:-1],amount-containers[-1])


# def fewest_containers(containers,amount):
#     if amount == 0:
#         return containers[-1]
#     if amount < 0 or len(containers) == 0:
#         return []
#     return fewest_containers(containers[:-1])


with open(INPUT_FILE) as in_file:
    containers = sorted([int(line.strip()) for line in in_file])
part1 = fill_containers(containers,LITERS)

print(f'The number of combinations of containers that can fit exactly {LITERS} liters is {part1}.')
