# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/1



input = '2019/01/input.txt'


with open(input) as f:
    fuel = lambda num: max(num // 3 - 2, 0)
    sum1,sum2 = 0,0
    for line in f:
        sub_fuel = fuel(int(line.strip()))
        sum1 += sub_fuel
        sub_sum = sub_fuel
        extra = fuel(sub_sum)
        while extra > 0:
            sub_sum += extra
            extra = fuel(extra)
        sum2 += sub_sum

    print(f'Initial fuel required is {sum1}')

    print(f'Total fuel required is {sum2}')