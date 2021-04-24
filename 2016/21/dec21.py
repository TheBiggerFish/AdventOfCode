# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/21


input = 'abcdefgh'
reverse_input = 'fbgdceah'

class Scramler:
    def __init__(self,string:str):
        self.string = string

    def swap_pos(self,x,y):
        first = min((x,y))
        last = max((x,y))
        self.string = self.string[:first] + self.string[last] + self.string[first+1:last] + self.string[first] + ('' if last == len(self.string)-1 else self.string[last+1:])

    def swap_letter(self,a,b):
        x = self.string.index(a)
        y = self.string.index(b)
        self.swap_pos(x,y)

    def rot_left(self,x):
        self.string = self.string[x:] + self.string[:x]

    def rot_right(self,x):
        y = len(self.string) - x
        self.string = self.string[y:] + self.string[:y]
        
    def rot_letter(self,a):
        x = self.string.index(a)
        x += 2 if x > 3 else 1
        self.rot_right(x)

    def rot_letter_reverse(self,a):
        x = self.string.index(a)
        if x == 0:
            self.rot_left(1)
        elif x == 1:
            self.rot_left(1)
        elif x == 2:
            self.rot_right(2)
        elif x == 3:
            self.rot_left(2)
        elif x == 4:
            self.rot_right(1)
        elif x == 5:
            self.rot_left(3)
        elif x == 6:
            pass
        elif x == 7:
            self.rot_left(4)
        else:
            raise Exception('Rotating invalid number of times')

    def reverse_pos(self,x,y):
        if y < len(self.string)-1 and x > 0:
            self.string = self.string[:x] + self.string[y:x-1:-1] + self.string[y+1:]
        elif y < len(self.string)-1:
            self.string = self.string[y::-1] + self.string[y+1:]
        elif x > 0:
            self.string = self.string[:x] + self.string[y:x-1:-1]
        else:
            self.string = self.string[::-1]

    def move_pos(self,x,y):
        char = self.string[x]
        self.string = self.string[:x] + ('' if x == len(self.string) + 1 else self.string[x+1:])
        self.string = self.string[:y] + char + self.string[y:]

    def move_pos_reverse(self,x,y):
        self.move_pos(y,x)

    def execute(self,instruction:str):
        instruction = instruction.split()
        if instruction[0] == 'swap':
            if instruction[1] == 'position':
                self.swap_pos(int(instruction[2]),int(instruction[5]))
            elif instruction[1] == 'letter':
                self.swap_letter(instruction[2],instruction[5])
        elif instruction[0] == 'rotate':
            if instruction[1] == 'left':
                self.rot_left(int(instruction[2]))
            elif instruction[1] == 'right':
                self.rot_right(int(instruction[2]))
            elif instruction[1] == 'based':
                self.rot_letter(instruction[6])
        elif instruction[0] == 'reverse':
            self.reverse_pos(int(instruction[2]),int(instruction[4]))
        elif instruction[0] == 'move':
            self.move_pos(int(instruction[2]),int(instruction[5]))

    def execute_reverse(self,instruction:str):
        instruction = instruction.split()
        if instruction[0] == 'swap':
            if instruction[1] == 'position':
                self.swap_pos(int(instruction[2]),int(instruction[5]))
            elif instruction[1] == 'letter':
                self.swap_letter(instruction[2],instruction[5])
        elif instruction[0] == 'rotate':
            if instruction[1] == 'left':
                self.rot_right(int(instruction[2]))
            elif instruction[1] == 'right':
                self.rot_left(int(instruction[2]))
            elif instruction[1] == 'based':
                self.rot_letter_reverse(instruction[6])
        elif instruction[0] == 'reverse':
            self.reverse_pos(int(instruction[2]),int(instruction[4]))
        elif instruction[0] == 'move':
            self.move_pos_reverse(int(instruction[2]),int(instruction[5]))


with open('2016/21/input.txt') as f:
    s = Scramler(input)
    for line in f:
        s.execute(line.strip())
    print(f'The scrambled password is {s.string}')

    
with open('2016/21/input.txt') as f:
    s = Scramler(reverse_input)
    for line in reversed(f.read().strip().split('\n')):
        s.execute_reverse(line.strip())
    print(f'The unscrambled password is {s.string}')