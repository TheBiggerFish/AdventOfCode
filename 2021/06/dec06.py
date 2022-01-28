# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/6


# days = 80
days = 256

with open('2021/06/input.txt') as f:
    line = f.readline().rstrip().split(',')
    state = {i:line.count(str(i)) for i in range(9)}

next_state = state.copy()
for _ in range(days):
    births = state[0]
    next_state[0] -= births

    for i in range(8):
        next_state[i] = state[i+1]
    next_state[6] += births
    next_state[8] = births
    state = next_state
print(f'The number of fish after {days} days is {sum(state.values())}')
