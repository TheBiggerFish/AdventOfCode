# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/14


from typing import List

def masked_value(input_value:int,mask:str) -> int:
    val = bin(input_value)[2:].rjust(36,'0')
    new_value = [v_bit if m_bit == 'X' else m_bit for v_bit,m_bit in zip(val,mask)]
    return int(''.join(new_value),2)

def masked_value_list(input_value:int,mask:str) -> List[int]:
    rv = []
    val = bin(input_value)[2:].rjust(36,'0')
    masked = ''.join([v_bit if m_bit == '0' else m_bit for v_bit,m_bit in zip(val,mask)])
    for i in range(2**masked.count('X')):
        floats = bin(i)[2:].rjust(masked.count('X'),'0')
        new_val = masked
        which_x = 0
        for i in range(len(val)):
            if new_val[i] == 'X':
                new_val = new_val[:i] + floats[which_x] + new_val[i+1:]
                which_x += 1
        rv.append(int(''.join(new_val),2))
    return rv

operations = []
with open('2020/14/input.txt','r') as input_file:
    for line in input_file:
        operation = line.strip().split(' = ')
        if operation[0] != 'mask':
            operation[0] = operation[0].split('[')[1][:-1]
        operations.append(tuple(operation))

mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
mem_1,mem_2 = {},{}

for op,value in operations:
    if op == 'mask':
        mask = value
    else:
        mem_1[op] = masked_value(int(value),mask)
        for key in masked_value_list(int(op),mask):
            mem_2[key] = int(value)

print('Result 1:',sum(mem_1.values()))
print('Result 2:',sum(mem_2.values()))