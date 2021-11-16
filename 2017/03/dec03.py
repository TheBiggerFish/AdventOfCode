# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/3


input = 361527
side = input // int(input ** 0.5)
square = side ** 2
diff = input - square
x = (side-1)//2
y = diff-(x)
print(x+y)
