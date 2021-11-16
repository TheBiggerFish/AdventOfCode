# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/22


from typing import List

player1,player2 = [],[]
with open('2020/22/input.txt','r') as input_file:
    input_file.readline()
    while (line := input_file.readline()) != '\n':
        player1.append(int(line.strip()))
    
    input_file.readline()
    while line := input_file.readline():
        player2.append(int(line.strip()))
    
def score(player:List[str]):
    return sum([i*n for i,n in enumerate(reversed(player),1)])
    
rounds = 0
while player1 and player2:
    print(f'-- Round {rounds+1} --')
    print(f'Player 1\'s deck: {tuple(player1)}')
    print(f'Player 2\'s deck: {tuple(player2)}')
    print(f'Player 1 plays: {player1[0]}')
    print(f'Player 2 plays: {player2[0]}')
    if player1[0] > player2[0]:
        player1.append(player1[0])
        player1.append(player2[0])
        print('Player 1 wins the round!\n')
    else:
        player2.append(player2[0])
        player2.append(player1[0])
        print('Player 2 wins the round!\n')
    del player1[0]
    del player2[0]
    rounds += 1
    
if player1:
    print(f'Player One won in {rounds} rounds')
    print(f'Player One had a score of {score(player1)}')
else:
    print(f'Player Two won in {rounds} rounds')
    print(f'Player Two had a score of {score(player2)}')