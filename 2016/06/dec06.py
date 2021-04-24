# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/6

chars = 8
freq = []
for _ in range(chars):
    freq += [{}]

with open('2016/06/input.txt') as in_file:
    for line in in_file:
        for ind in range(len(line.strip())):
            char = line[ind]
            if char not in freq[ind]:
                freq[ind][char] = 0
            freq[ind][char] += 1

letters1,letters2 = [],[]
for ind in range(len(freq)):
    freq[ind] = {k: v for k, v in sorted(freq[ind].items(), key=lambda item: item[1],reverse=True)}
    letters1.append(next(iter(freq[ind])))
    freq[ind] = {k: v for k, v in sorted(freq[ind].items(), key=lambda item: item[1])}
    letters2.append(next(iter(freq[ind])))
print(f'The error-corrected version of the message being sent is {"".join(letters1)}')
print(f'The actual message being sent is {"".join(letters2)}')
