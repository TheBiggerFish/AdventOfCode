# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/23


from math import factorial

from fishpy.computer import (ArgList, Computer, Instruction, Operand,
                             Operation, ProgramCounter, RegisterDict)

puzzle_input_1 = 7
puzzle_input_2 = 12

def toggle(instr:Instruction):
    if len(instr.operation.operands) == 1:
        if instr.operation.identifier == 'inc':
            instr.operation = ops['dec']
        else:
            instr.operation = ops['inc']
    elif len(instr.operation.operands) == 2:
        if instr.operation.identifier == 'jnz':
            instr.operation = ops['cpy']
        else:
            instr.operation = ops['jnz']

def cpy_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    if arguments[1] in registers:
        registers[arguments[1]] = int(arg0)
    return pc+1

def inc_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    if arguments[0] in registers:
        registers[arguments[0]] += 1
    return pc+1

def dec_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    if arguments[0] in registers:
        registers[arguments[0]] -= 1
    return pc+1

def jnz_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    arg0,arg1 = arguments[0],arguments[1]
    if arg0 in registers:
        arg0 = registers[arg0]
    if arg1 in registers:
        arg1 = registers[arg1]

    if int(arg0) == 0:
        return pc + 1
    else:
        return pc + int(arg1)

def tgl_func(arguments:ArgList,registers:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    target = pc + int(arg0)
    if 0 <= target < len(program):
        toggle(program[target])
    return pc+1

ops = {
    'cpy': Operation('cpy',cpy_func,[Operand.REGISTER|Operand.CONSTANT,
                                     Operand.REGISTER]),
    'inc': Operation('inc',inc_func,[Operand.REGISTER]),
    'dec': Operation('dec',dec_func,[Operand.REGISTER]),
    'jnz': Operation('jnz',jnz_func,[Operand.REGISTER|Operand.CONSTANT,
                                     Operand.REGISTER|Operand.CONSTANT]),
    'tgl': Operation('tgl',tgl_func,[Operand.REGISTER|Operand.CONSTANT])
}

program = []
with open('2016/23/input.txt') as f:
    for line in f:
        cmd = line.strip().split()
        op = ops[cmd[0]]
        args = cmd[1:]
        program.append(Instruction(op,args))
        

comp1 = Computer(registers={'a':puzzle_input_1,'b':0,'c':0,'d':0},initial_pc=0)
comp1.execute(program)
print('Value in register \'a\' after run 1:',comp1.regs['a'])

# Program performs factorial on input, then adds 93*80=7440
print('Predicted value in register \'a\' after run 2:',factorial(puzzle_input_2)+(93*80))
