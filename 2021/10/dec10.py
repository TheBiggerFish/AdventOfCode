# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/10


from fishpy.structures import Stack


with open('2021/10/input.txt') as f:
    lines = f.read().strip().split()

error_scores_dict = {')': 3, ']': 57, '}': 1197, '>': 25137}
autocomplete_scores_dict = {')': 1, ']': 2, '}': 3, '>': 4}
match = {'(':')',')':'(','[':']',']':'[','{':'}','}':'{','<':'>','>':'<'}

error_score = 0
autocomplete_scores = []
for line in lines:
    stack = Stack()
    valid = True
    for char in line:
        if char in {'(','[','{','<'}:
            stack.push(char)
        elif match[char] != stack.pop():
            error_score += error_scores_dict[char]
            valid = False
            break
    if valid:
        autocomplete_score = 0
        while not stack.empty():
            char = match[stack.pop()]
            autocomplete_score *= 5
            autocomplete_score += autocomplete_scores_dict[char]
        autocomplete_scores.append(autocomplete_score)

autocomplete_scores = sorted(autocomplete_scores)

print(error_score)
print(autocomplete_scores[len(autocomplete_scores)//2])
