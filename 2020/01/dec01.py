# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/1



with open('2020/01/input.txt') as f:
    nums = [int(line.strip()) for line in f.readlines()]
    for i in range(len(nums)):
        for j in range(i,len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i]*nums[j])
            for k in range(j,len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i]*nums[j]*nums[k])