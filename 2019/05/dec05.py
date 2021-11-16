# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/5



input_file = '2019/05/input.txt'

def parameter_mode(val):
    p1 = val//100 % 10
    p2 = val//1000 % 10
    p3 = val//10000 % 10
    return (bool(p1),bool(p2),bool(p3))

def output(intcode,noun,verb):
    intcode[1] = noun
    intcode[2] = verb

    pc = 0
    while pc < len(intcode) and intcode[pc] != 99:
        modes = parameter_mode(intcode[pc])

        if intcode[pc]%100 == 1:
            if not modes[2]:
                left = intcode[pc+1] if modes[0] else intcode[intcode[pc+1]]
                right = intcode[pc+2] if modes[1] else intcode[intcode[pc+2]]
                intcode[intcode[pc+3]] = left + right
                pc += 4 
        elif intcode[pc]%100 == 2:
            if not modes[2]:
                left = intcode[pc+1] if modes[0] else intcode[intcode[pc+1]]
                right = intcode[pc+2] if modes[1] else intcode[intcode[pc+2]]
                intcode[intcode[pc+3]] = left * right
                pc += 4 
        elif intcode[pc]%100 == 3:
            intcode[intcode[pc+1]] = int(input('Input:'))
            pc += 2
        elif intcode[pc]%100 == 4:
            print(f'Output:{intcode[intcode[pc+1]]}')
            pc += 2
        else:
            raise ValueError(f'Invalid intcode operation: {intcode[pc+1]}')
    return intcode[0]

with open(input_file) as f:
    intcode = [int(item) for item in f.readline().strip().split(',')]

    out = 0
    for noun in range(100):
        for verb in range(100):
            if output(intcode.copy(),noun,verb) == 19690720:
                out = noun * 100 + verb
                break

    print(f'Noun=12,Verb=2,Output={output(intcode.copy(),12,2)}')
    print(f'Output=19690720,Checksum={out}')