# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/8


from typing import Any, Dict, List, Tuple, TypeVar

from fishpy.computer import (ArgList, Computer, Instruction, Operand,
                             Operation, ProgramCounter, RegisterDict)


def nop_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    return pc+1

def acc_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    registers['acc'] += arguments[0]
    return pc+1

def jmp_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    return pc+arguments[0]

ops = {
    'nop': Operation('nop',nop_func,[Operand.CONSTANT]),
    'acc': Operation('acc',acc_func,[Operand.CONSTANT]),
    'jmp': Operation('jmp',jmp_func,[Operand.CONSTANT])
}

def do_swap_instruction(program:List[Instruction],instr_n:int):
    if 0 <= instr_n < len(program):
        if program[instr_n].operation.identifier == 'jmp':
            program[instr_n].operation = ops['nop']
        elif program[instr_n].operation.identifier == 'nop':
            program[instr_n].operation = ops['jmp']

def attempt_execution(program:List[Instruction],swap_instruction:int=-1) -> Tuple[int,bool]:
    comp = Computer({'acc': 0})
    executed_code = set()
    failed = False

    do_swap_instruction(program,swap_instruction)
    while 0 <= comp.pc < len(program):
        if comp.pc in executed_code:
            failed = True
            break
        else:
            executed_code.add(comp.pc)
        comp.execute_instruction(program[comp.pc])
    do_swap_instruction(program,swap_instruction)

    return comp.regs['acc'],failed

program = []
with open('2020/08/input.txt') as f:
    for line in f:
        cmd = line.strip().split()
        op = ops[cmd[0]]
        args = [int(cmd[1])]
        program.append(Instruction(op,args))

print('Accumulator at failure:',attempt_execution(program)[0])  # Part 1

failed = True
swap_instruction = 0
while failed:
    value,failed = attempt_execution(program,swap_instruction)
    swap_instruction += 1

print(f'Corrected run: {swap_instruction}, accumulator at completion: {value}')
