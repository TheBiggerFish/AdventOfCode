# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/9


from typing import List

PREAMBLE = 25

def is_sum_of_preceding(number:int,preceding:List[int]):
    for i in range(len(preceding)-1):
        for j in range(i+1,len(preceding)):
            if number == preceding[i] + preceding[j]:
                return True
    return False

with open('2020/09/input.txt','r') as input_file:
    numbers = [int(line.strip()) for line in input_file]
        
for i in range(PREAMBLE,len(numbers)):
    if not is_sum_of_preceding(numbers[i],numbers[i-PREAMBLE:i]):
        result_1 = numbers[i]
        break
print('Part 1:',result_1)

for length in range(2,PREAMBLE):
    for i in range(0,len(numbers)-length+1):
        if result_1 == sum(numbers[i:i+length]):
            result_2 = min(numbers[i:i+length]) + max(numbers[i:i+length])
            break
print('Part 2:',result_2)

