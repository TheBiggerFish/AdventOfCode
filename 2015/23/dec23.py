# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/23


from typing import Any,Dict,List
from fishpy.computer import Computer, Instruction, Operand, Operation, ProgramCounter


def hlf_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    registers[arguments[0]] //= 2
    return pc+1

def tpl_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    registers[arguments[0]] *= 3
    return pc+1

def inc_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    registers[arguments[0]] += 1
    return pc+1

def jmp_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    return pc+int(arguments[0])

def jie_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    if registers[arguments[0]] % 2 == 0:
        return pc + int(arguments[1])
    else:
        return pc + 1

def jio_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    if registers[arguments[0]] == 1:
        return pc + int(arguments[1])
    else:
        return pc + 1

ops = {
    'hlf': Operation('hlf',hlf_func,[Operand.REGISTER]),
    'tpl': Operation('tpl',tpl_func,[Operand.REGISTER]),
    'inc': Operation('inc',inc_func,[Operand.REGISTER]),
    'jmp': Operation('jmp',jmp_func,[Operand.CONSTANT]),
    'jie': Operation('jie',jie_func,[Operand.REGISTER,Operand.CONSTANT]),
    'jio': Operation('jio',jio_func,[Operand.REGISTER,Operand.CONSTANT])
}


program = []
with open('2015/23/input.txt') as f:
    for line in f:
        cmd = line.replace(',','').strip().split()
        op = ops[cmd[0]]
        args = cmd[1:]
        program.append(Instruction(op,args))

comp1 = Computer(registers={'a':0,'b':0},initial_pc=0)
comp2 = Computer(registers={'a':1,'b':0},initial_pc=0)

comp1.execute(program)
print('Value in register b after run 1:',comp1.regs['b'])
comp2.execute(program)
print('Value in register b after run 2:',comp2.regs['b'])
