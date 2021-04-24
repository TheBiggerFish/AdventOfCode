# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/23


class Instruction:
    def __init__(self,ins,arg1='',arg2=''):
        self.ins = ins
        self.left = arg1 if arg1 in ('a','b','c','d') else int(arg1)
        self.right = arg2 if arg2 in ('a','b','c','d','') else int(arg2)
    
    @staticmethod
    def load_program(filename):
        with open(filename) as in_file:
            return [Instruction(*tuple(i.strip().replace(',','').split(' '))) for i in in_file]

    def __str__(self):
        return f'{self.ins} {self.left} {self.right}'
class Computer:
    def __init__(self,registers):
        self.registers = {}
        for r in registers:
            self.registers[r] = 0
        self.zero_out()

    def zero_out(self):
        self.pc = 0
        for r in self.registers:
            self.registers[r] = 0

    def set_reg(self,which,value):
        self.registers[which] = value
    
    def get_reg(self,which):
        return self.registers[which]

    def execute(self,program):
        self.instructions = program
        steps = 1
        while self.pc < len(program):
            instruction = program[self.pc]
            self.execute_instruction(instruction)
            steps += 1
        del self.instructions
        
    def execute_instruction(self,instruction):
        if instruction.ins == 'cpy':
            self.cpy(instruction.left,instruction.right)
        elif instruction.ins == 'inc':
            self.inc(instruction.left)
        elif instruction.ins == 'dec':
            self.dec(instruction.left)
        elif instruction.ins == 'jnz':
            self.jnz(instruction.left,instruction.right)
        elif instruction.ins == 'tgl':
            self.tgl(instruction.left)

        if instruction.ins in ('cpy','inc','dec'):
            self.pc += 1
        
    def cpy(self,value,reg):
        if reg not in self.registers:
            raise ValueError(f'Argument \'{reg}\' is not a valid register')
        if value in self.registers:
            value = self.get_reg(value)
        self.set_reg(reg,value)

    def inc(self,reg):
        if reg not in self.registers:
            raise ValueError(f'Argument \'{reg}\' is not a valid register')
        self.set_reg(reg,self.get_reg(reg)+1)

    def dec(self,reg):
        if reg not in self.registers:
            raise ValueError(f'Argument \'{reg}\' is not a valid register')
        self.set_reg(reg,self.get_reg(reg)-1)

    def jnz(self,value,step):
        if value in self.registers:
            value = self.get_reg(value)
        if step in self.registers:
            step = self.get_reg(step)
        if value != 0:
            self.pc += step
        else:
            self.pc += 1

    def tgl(self,value):
        if value in self.registers:
            value = self.get_reg(value)
        ins:Instruction = self.instructions[self.pc+value]
        if ins.ins == 'inc':
            ins.ins = 'dec'
        elif ins.ins in ['tgl','dec']:
            ins.ins = 'inc'
        elif ins.ins == 'jnz':
            ins.ins = 'cpy'
        elif ins.ins in ['cpy']:
            ins.ins = 'jnz'
        else:
            raise Exception('Toggl')
        print(f'Toggling instruction {self.pc+value}')
        self.instructions[self.pc+value] = ins
        self.pc += 1

    
    def __str__(self):
        string = f'Registers: pc={self.pc}'
        for reg in self.registers:
            string += f', {reg}={self.get_reg(reg)}'
        return string


c = Computer(['a','b','c','d'])
c.set_reg('a',7)
program = Instruction.load_program('2016/23/input.txt')
c.execute(program)
print(f'Register \'a\' after first run: {c.get_reg("a")}')