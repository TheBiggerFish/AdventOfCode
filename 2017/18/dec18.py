# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/18


from fishpy.computer import (ArgList, Computer, Instruction, Operand,
                             Operation, ProgramCounter, RegisterDict)


def read_value(value:str,regs:RegisterDict):
    if value in regs:
        return regs[value]
    if value.lstrip('-').isnumeric():
        return int(value)
    raise ValueError('Invalid value type')
    

def snd_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs['_sound'] = read_value(args[0])
    return pc+1

def set_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] = read_value(args[1])
    return pc+1

def add_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] += read_value(args[1])
    return pc+1

def mul_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] *= read_value(args[1])
    return pc+1

def mod_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    regs[args[0]] %= read_value(args[1])
    return pc+1

def rcv_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    if read_value(args[0]) != 0:
        print(regs['_sound'])
        return -1
    return pc+1

def jgz_func(args:ArgList,regs:RegisterDict,pc:ProgramCounter) -> ProgramCounter:
    if read_value(args[0]) > 0:
        return pc + read_value(args[1])
    else:
        return pc + 1
    
ops = {
    'snd': Operation('snd',snd_func,[Operand.REGISTER]),
    'set': Operation('set',set_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'add': Operation('add',add_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'mul': Operation('mul',mul_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'mod': Operation('mod',mod_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT]),
    'rcv': Operation('rcv',rcv_func,[Operand.REGISTER]),
    'jgz': Operation('jgz',jgz_func,[Operand.REGISTER,Operand.REGISTER|Operand.CONSTANT])
}

program = []
with open('2017/18/input.txt') as in_file:
    for line in in_file:
        line = line.strip().split()
        op = ops[line[0]]
        args = line[1:]
        program.append(Instruction(op,args))

comp1 = Computer(registers={'a':0,'b':0,'f':0,'i':0,'p':0},initial_pc=0)
comp1.execute(program)
