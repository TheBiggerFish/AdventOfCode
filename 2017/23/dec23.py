# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/23


from fishpy.computer import (ArgList, Computer, Instruction, Operand,
                             Operation, ProgramCounter, RegisterDict)


def read_value(value:str,regs:RegisterDict):
    if value in regs:
        return regs[value]
    if value.lstrip('-').isnumeric():
        return int(value)
    raise ValueError('Invalid value type')
    
def set_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] = read_value(args[1],regs)
    return pc+1

def sub_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] -= read_value(args[1],regs)
    return pc+1

def mul_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] *= read_value(args[1],regs)
    return pc+1

def jnz_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    if read_value(args[0],regs) != 0:
        return pc + read_value(args[1],regs)
    else:
        return pc + 1
    
ops = {
    'set': Operation('set',set_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'sub': Operation('sub',sub_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'mul': Operation('mul',mul_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'jnz': Operation('jnz',jnz_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT])
}

program = []
with open('2017/23/input.txt') as in_file:
    for line in in_file:
        line = line.strip().split()
        if line[0] not in ops:
            continue
        op = ops[line[0]]
        args = line[1:]
        program.append(Instruction(op,args))

registers = {letter:0 for letter in 'abcdefgh'}
comp1 = Computer(registers=registers,initial_pc=0)
comp1.execute_with_profiler(program)
