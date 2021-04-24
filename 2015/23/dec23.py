# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/23


class Instruction:
    def __init__(self,ins,arg1='',arg2=''):
        self.ins = ins
        self.reg = arg1 if arg1 in ('a','b') else ''
        if arg1[0] in ('+','-'):
            arg2 = arg1
        self.offset = int(str(arg2).strip('+')) if arg2 != '' else 0
    
    @staticmethod
    def load_program(filename):
        with open(filename) as in_file:
            return [Instruction(*tuple(i.strip().replace(',','').split(' '))) for i in in_file]

    def __str__(self):
        string = self.ins
        if self.reg != '':
            string += ' ' + self.reg + (',' if self.ins in ('jio','jie') else '')
        if self.offset != 0:
            string += ' ' if self.offset < 0 else ' +' + str(self.offset)
        return string

class Computer:
    def __init__(self):
        self.zero_out()

    def zero_out(self):
        self.a = 0
        self.b = 0
        self.pc = 0

    def execute(self,program):
        steps = 1
        while self.pc < len(program):
            instruction = program[self.pc]
            if instruction.ins == 'hlf':
                self.hlf(instruction.reg)
            elif instruction.ins == 'tpl':
                self.tpl(instruction.reg)
            elif instruction.ins == 'inc':
                self.inc(instruction.reg)
            elif instruction.ins == 'jmp':
                self.jmp(instruction.offset)
            elif instruction.ins == 'jie':
                self.jie(instruction.reg,instruction.offset)
            elif instruction.ins == 'jio':
                self.jio(instruction.reg,instruction.offset)
            # print(f'Registers after {steps} steps of program: a={c.a}, b={c.b}, pc={c.pc}')
            steps += 1
    
    def hlf(self,r):
        if r == 'a':
            self.a //= 2
        if r == 'b':
            self.b //= 2
        self.pc += 1

    def tpl(self,r):
        if r == 'a':
            self.a *= 3
        if r == 'b':
            self.b *= 3
        self.pc += 1

    def inc(self,r):
        if r == 'a':
            self.a += 1
        if r == 'b':
            self.b += 1
        self.pc += 1

    def jmp(self,offset):
        self.pc += offset

    def jie(self,r,offset):
        if r == 'a':
            if self.a % 2 == 0:
                self.pc += offset
            else:
                self.pc += 1
        elif r == 'b':
            if self.b % 2 == 0:
                self.pc += offset
            else:
                self.pc += 1

    def jio(self,r,offset):
        if r == 'a':
            if self.a == 1:
                self.pc += offset
            else:
                self.pc += 1
        elif r == 'b':
            if self.b == 1:
                self.pc += offset
            else:
                self.pc += 1


c = Computer()
program = Instruction.load_program('2015/23/input.txt')
c.execute(program)
print(f'Registers upon completion of program: a={c.a}, b={c.b}')

c.zero_out()
program2 = Instruction.load_program('2015/23/input2.txt')
c.execute(program2)
print(f'Registers upon completion of program with register a starting with value 1: a={c.a}, b={c.b}')