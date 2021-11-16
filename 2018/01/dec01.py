# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/1



input = '2018/01/input.txt'

with open(input) as f:
    nums = [int(num) for num in f.read().strip().split('\n')]
    total = 0
    seen = set()

    answer1,answer2 = 0,0

    found = False
    while not found:
        for i in range(len(nums)):
            if total in seen:
                found = True
                print(total)
            seen.add(total)
            total += nums[i]
        

    print(total)