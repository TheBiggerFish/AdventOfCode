# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/2


from fishpy.geometry import Point

class Keypad:
    layout1 = [
        ['1','2','3'],
        ['4','5','6'],
        ['7','8','9']
    ]
    layout2 = [
        ['','','1','',''],
        ['','2','3','4',''],
        ['5','6','7','8','9'],
        ['','A','B','C',''],
        ['','','D','','']
    ]
    def __init__(self,layout):
        self.pos = Point(1,1)
        self.layout = layout
    
    def get_current_key(self):
        return self.get_key_at(self.pos)

    def get_key_at(self,pos):
        return self.layout[len(self.layout)-pos.y-1][pos.x]

    def move(self,dir):
        newpos = None
        if dir == 'U':
            newpos = self.pos + Point(0,1)
        elif dir == 'D':
            newpos = self.pos + Point(0,-1)
        elif dir == 'R':
            newpos = self.pos + Point(1,0)
        elif dir == 'L':
            newpos = self.pos + Point(-1,0)
        upper_bound = Point(len(self.layout[0]),len(self.layout))
        if newpos.in_bounds(lower_bound=Point(0,0),upper_bound=upper_bound) and self.get_key_at(newpos) != '':
            self.pos = newpos
        

with open('2016/02/input.txt') as in_file:
    kp1 = Keypad(layout=Keypad.layout1)
    kp2 = Keypad(layout=Keypad.layout2)
    passwd1 = ''
    passwd2 = ''
    for line in in_file:
        for char in line.strip():
            kp1.move(char)
            kp2.move(char)
        passwd1 += kp1.get_current_key()
        passwd2 += kp2.get_current_key()
    print(f'The password for the theoretical keypad is {passwd1} and the password for the actual keypad is {passwd2}')