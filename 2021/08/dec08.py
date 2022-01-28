# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/8


from typing import List, Optional


class SegmentDisplay:
    DIGITS = {
        0: [1,1,1,0,1,1,1], 1: [0,0,1,0,0,1,0], 2: [1,0,1,1,1,0,1], 
        3: [1,0,1,1,0,1,1], 4: [0,1,1,1,0,1,0], 5: [1,1,0,1,0,1,1], 
        6: [1,1,0,1,1,1,1], 7: [1,0,1,0,0,1,0], 8: [1,1,1,1,1,1,1], 
        9: [1,1,1,1,0,1,1],
    }

    def __init__(self,layout:str):
        self.layout = layout
        self.digits = {n:''.join(sorted([char for i,char in enumerate(layout) if SegmentDisplay.DIGITS[n][i] == 1])) for n in range(10)}

    def get_digit_value(self,digit:str) -> Optional[int]:
        for i in range(10):
            if self.digits[i] == digit:
                return i
        return None

    def get_number_value(self,digits:List[str]):
        value = 0
        for digit in digits:
            value *= 10
            value += self.get_digit_value(digit)
        return value

    @staticmethod
    def build_from_digits(digits:List[str]):
        layout = [''] * 7
        key = sorted([set(string) for string in digits],key=lambda entry: len(entry))

        layout[0] = (key[1] - key[0]).pop()
        
        letters_5 = [letter for digit in key[3:6] for letter in digit]
        count_5 = {letter:letters_5.count(letter) for letter in 'abcdefg'}
        layout[1] = (set(filter(lambda entry:count_5[entry] == 1,count_5.keys())) & key[2]).pop()

        layout[3] = (key[2] - key[0] - {layout[1]}).pop()

        layout[4] = (set(filter(lambda entry:count_5[entry] == 1,count_5.keys())) - {layout[1]}).pop()

        layout[6] = (set(filter(lambda entry:count_5[entry] == 3,count_5.keys())) - {layout[0],layout[3]}).pop()

        digit_2 = list(filter(lambda digit: layout[4] in digit,key[3:6]))[0]
        layout[2] = (key[0] & digit_2).pop()
        layout[5] = (key[0] - digit_2).pop()

        return SegmentDisplay(''.join(layout))
        

with open('2021/08/input.txt') as f:
    lines = [line.rstrip().split(' | ') for line in f.readlines()]
    unique_digit_count = 0
    for line in lines:
        for digit_string in line[1].split():
            for digit in {1,4,7,8}:
                if len(digit_string) == SegmentDisplay.DIGITS[digit].count(1):
                    unique_digit_count += 1
    print(f'{unique_digit_count=}')

    sum_ = 0
    for line in lines:
        output = [''.join(sorted(string)) for string in line[1].split()]
        display = SegmentDisplay.build_from_digits(line[0].split())
        sum_ += display.get_number_value(output)
    print('Total sum:',sum_)
         