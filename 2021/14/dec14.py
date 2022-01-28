# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/14


iterations = 40
with open('2021/14/input.txt') as f:
    template = f.readline().rstrip()
    f.readline()
    rules = {line[:2]:line[6] for line in f.readlines()}

polymer = {rule:0 for rule in rules}
for i in range(len(template)-1):
    substr = template[i:i+2]
    polymer[substr] += 1


for _ in range(iterations):
    new_polymer = {rule:0 for rule in rules}
    for pair in polymer:
        triple = pair[0] + rules[pair] + pair[1]
        new_polymer[triple[:2]] += polymer[pair]
        new_polymer[triple[1:]] += polymer[pair]
    polymer = new_polymer

character_counts = {rule[0]:0 for rule in rules}
character_counts[template[-1]] = 1
for pair in polymer:
    character_counts[pair[0]] += polymer[pair]
print(character_counts)

min_ = min(character_counts,key=lambda item:character_counts[item])
max_ = max(character_counts,key=lambda item:character_counts[item])
print(f'{min_}={character_counts[min_]}',f'{max_}={character_counts[max_]}')
print(f'{max_} - {min_} = {character_counts[max_]-character_counts[min_]}')