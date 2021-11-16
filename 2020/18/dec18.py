# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/18


from fishpy.arithmetic import OrderedOperation,Expression
from fishpy.arithmetic import PARENTHESES,ADDITION,MULTIPLICATION

PMA = [OrderedOperation(PARENTHESES,OrderedOperation.GROUP_OPERATION_ORDER),
       OrderedOperation(ADDITION,0),
       OrderedOperation(MULTIPLICATION,0)]
PAM = [OrderedOperation(PARENTHESES,OrderedOperation.GROUP_OPERATION_ORDER),
       OrderedOperation(ADDITION,1),
       OrderedOperation(MULTIPLICATION,0)]

expressions = []
with open('2020/18/input.txt','r') as input_file:
    expressions = [line.strip().replace(' ','') for line in input_file]

count,count2 = 0,0
for expr in expressions:
    count += Expression.build_from_string(expr,PMA).evaluate()
    count2 += Expression.build_from_string(expr,PAM).evaluate()
print('Result 1:',count)
print('Result 2:',count2)