
# AX: Rock ; BY: Paper ; CZ: Scissors
score_dict = {'X': 1, 'Y': 2, 'Z': 3}
draw_dict = {'A': 'X', 'B': 'Y', 'C': 'Z'}
beat_dict = {'A': 'Z', 'B': 'X', 'C': 'Y'}
lose_dict = {'A': 'Y', 'B': 'Z', 'C': 'X'}
with open('2022/02/input.txt') as f:
    rounds = f.read().splitlines()
score_1, score_2 = 0, 0
for round in rounds:
    score_1 += score_dict[round[-1]]
    if lose_dict[round[0]] == round[-1]:
        score_1 += 6
    elif draw_dict[round[0]] == round[-1]:
        score_1 += 3

    if round[-1] == 'X':
        score_2 += score_dict[beat_dict[round[0]]]
    if round[-1] == 'Y':
        score_2 += 3 + score_dict[draw_dict[round[0]]]
    if round[-1] == 'Z':
        score_2 += 6 + score_dict[lose_dict[round[0]]]
print(score_1, score_2)
