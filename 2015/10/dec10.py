# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/10


input_ = '3113322113'
iterations = 50

def look_and_say(input_):
    output = ''
    current = 0
    while current < len(input_):
        running = input_[current]
        run = 0
        while current < len(input_) and input_[current] == running:
            run += 1
            current += 1
        output += str(run) + running
    return output

sequence = input_
for _ in range(iterations):
    sequence = look_and_say(sequence)
    
print('After {} iterations, the length of the new sequence is {}'.format(iterations,len(sequence)))