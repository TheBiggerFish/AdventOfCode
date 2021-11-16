# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/2



input = '2019/02/input.txt'

def output(intcode,noun,verb):
    intcode[1] = noun
    intcode[2] = verb

    pc = 0
    while pc < len(intcode) and intcode[pc] != 99:
        if intcode[pc] == 1:
            intcode[intcode[pc+3]] = intcode[intcode[pc+2]] + intcode[intcode[pc+1]]
        if intcode[pc] == 2:
            intcode[intcode[pc+3]] = intcode[intcode[pc+2]] * intcode[intcode[pc+1]]
        pc += 4 
    return intcode[0]

with open(input) as f:
    intcode = [int(item) for item in f.readline().strip().split(',')]

    out = 0
    for noun in range(100):
        for verb in range(100):
            if output(intcode.copy(),noun,verb) == 19690720:
                out = noun * 100 + verb
                break

    print(f'Noun=12,Verb=2,Output={output(intcode.copy(),12,2)}')
    print(f'Output=19690720,Checksum={out}')