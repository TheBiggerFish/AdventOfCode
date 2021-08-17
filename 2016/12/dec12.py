# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/12


from typing import Any,Dict,List
from fishpy.computer import Computer, Instruction, Operand, Operation, ProgramCounter

def cpy_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    registers[arguments[1]] = int(arg0)
    return pc+1

def inc_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    registers[arguments[0]] += 1
    return pc+1

def dec_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    registers[arguments[0]] -= 1
    return pc+1

def jnz_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    if int(arg0) == 0:
        return pc + 1
    else:
        return pc + int(arguments[1])

ops = {
    'cpy': Operation('cpy',cpy_func,[Operand.REGISTER|Operand.CONSTANT,Operand.REGISTER]),
    'inc': Operation('inc',inc_func,[Operand.REGISTER]),
    'dec': Operation('dec',dec_func,[Operand.REGISTER]),
    'jnz': Operation('jnz',jnz_func,[Operand.REGISTER|Operand.CONSTANT,Operand.CONSTANT]),
}

program = []
with open('2016/12/input.txt') as f:
    for line in f:
        cmd = line.strip().split()
        op = ops[cmd[0]]
        args = cmd[1:]
        program.append(Instruction(op,args))

comp1 = Computer(registers={'a':0,'b':0,'c':0,'d':0},initial_pc=0)
comp2 = Computer(registers={'a':0,'b':0,'c':1,'d':0},initial_pc=0)

comp1.execute(program)
print('Value in register \'a\' after run 1:',comp1.regs['a'])
comp2.execute(program)
print('Value in register \'a\' after run 2:',comp2.regs['a'])
