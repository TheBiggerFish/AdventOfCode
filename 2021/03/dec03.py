# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/3


def most_common_bit(numbers:list[str], position:int) -> str:
    counts = {}
    for number in numbers:
        if number[position] in counts:
            counts[number[position]] += 1
        else:
            counts[number[position]] = 1
    if counts['0'] == counts['1']:
        return '1'
    return sorted(counts.keys(), key = lambda key: counts[key])[-1]

def oxygen_generator_rating(numbers:list[str]) -> int:
    bits = len(numbers[0])
    for pos in range(bits):
        mcb = most_common_bit(numbers,pos)
        numbers = list(filter(lambda number: number[pos] == mcb, numbers))
        if len(numbers) == 1:
            break
    return int(list(numbers)[0],2)

def co2_scrubber_rating(numbers:list[str]) -> int:
    bits = len(numbers[0])
    for pos in range(bits):
        lcb = '0' if most_common_bit(numbers,pos) == '1' else '1'
        numbers = list(filter(lambda number: number[pos] == lcb, numbers))
        if len(numbers) == 1:
            break
    return int(list(numbers)[0],2)

with open('2021/03/input.txt') as f:
    lines = f.read().strip().split()
    bits = len(lines[0])

    gamma = ''
    for pos in range(bits):
        gamma += most_common_bit(lines,pos)

    mask = int('1' * bits,2)
    gamma = int(gamma,2)
    epsilon = gamma^mask
    power = gamma * epsilon
    print(f'The power consumption of the submarine is {power}')

    o2 = oxygen_generator_rating(lines)
    co2 = co2_scrubber_rating(lines)
    life_support = o2 * co2
    print(f'The life support rating of the submaring is {life_support}')
