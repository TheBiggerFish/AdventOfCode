# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/4


from typing import Dict, List, Optional, Set


class BingoBoard:
    def __init__(self,board:List[List[int]]):
        self.board = board
        self.found:Set[int] = set()
        self._row_cache:Dict[int,int] = {}
        self._col_cache:Dict[int,int] = {}

        self.winner_board = [['' for _ in range(5)] for _ in range(5)]
        self.winning_number:Optional[int] = None

        for row in range(len(board)):
            for col in range(len(board[row])):
                self._row_cache[board[row][col]] = row
                self._col_cache[board[row][col]] = col

    def __str__(self):
        return '\n'.join([' '.join([str(col) for col in row]) for row in self.board])

    def add_number(self,number):
        if number not in self._row_cache:
            return None

        row = self._row_cache[number]
        col = self._col_cache[number]
        self.winner_board[row][col] = number

    def final_score(self) -> int:
        score = 0
        for num in self._row_cache:
            row = self._row_cache[num]
            col = self._col_cache[num]
            if self.winner_board[row][col] == '':
                score += self.board[row][col]
        return score * self.winning_number
        

    def is_final(self) -> bool:
        # row
        for row in self.winner_board:
            if '' not in row:
                return True

        # col
        for col in range(5):
            found = True
            for row in range(5):
                if self.winner_board[row][col] == '':
                    found = False
                    continue
            if found:
                return True
                
        return False



with open('2021/04/input.txt') as f:
    numbers = [int(x) for x in f.readline().rstrip().split(',')]
    f.readline()

    boards:List[BingoBoard] = []
    board:List[str] = []
    while line := f.readline():
        if line == '\n':
            boards.append(BingoBoard(board))
            board = []
        else:
            board.append([int(num) for num in line.rstrip().split()])
    boards.append(BingoBoard(board))

    first_winner:Optional[BingoBoard] = None
    last_winner:Optional[BingoBoard] = None
    for number in numbers:
        for bingo_board in boards:
            if bingo_board.winning_number is not None:
                continue
            bingo_board.add_number(number)
            if bingo_board.is_final():
                bingo_board.winning_number = number
                if not first_winner:
                    first_winner = bingo_board
                last_winner = bingo_board

    print('The final score of the first winner is', first_winner.final_score())
    print('The final score of the last winner is', last_winner.final_score())
