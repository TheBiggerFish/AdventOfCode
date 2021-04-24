# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/8


from EulerLib.geometry import Point

class LCD:
    def __init__(self,dim:Point):
        self.screen = [[False]*dim.x for row in range(dim.y)]
        self.dim = dim
    
    def pixel_is_on(self,pt:Point) -> bool:
        return self.screen[pt.y][pt.x]
    
    def set_pixel(self,pt:Point,value:bool):
        self.screen[pt.y][pt.x] = value

    def __str__(self) -> str:
        string = ''
        for row in self.screen:
            for col in row:
                if col:
                    string += '# '
                else:
                    string += '. '
            string.rstrip()
            string += '\n'
        return string.rstrip()

    def rect(self,pt:Point):
        for y in range(pt.y):
            for x in range(pt.x):
                self.set_pixel(Point(x,y),True)
        return self

    def rotate_col(self,x,steps):
        col = [self.screen[y][x] for y in range(len(self.screen))]
        col = col[-(steps%len(col)):] + col[:-(steps%len(col))]
        for y in range(len(col)):
            self.screen[y][x] = col[y]
        return self

    def rotate_row(self,y,steps):
        row = self.screen[y]
        row = row[-(steps%len(row)):] + row[:-(steps%len(row))]
        self.screen[y] = row
        return self

    def execute_steps(self,steps):
        for step in steps:
            step = step.split()
            if step[0] == 'rect':
                axb = step[1].split('x')
                self.rect(Point(int(axb[0]),int(axb[1])))
            elif step[0] == 'rotate':
                which = int(step[2].split('=')[1])
                num = int(step[4])
                if step[1] == 'column':
                    self.rotate_col(which,num)
                elif step[1] == 'row':
                    self.rotate_row(which,num)
                    
    def lit_pixels(self):
        return sum([sum(self.screen[y]) for y in range(self.dim.y)])

with open('2016/08/input.txt') as f:
    lcd = LCD(Point(50,6))
    lcd.execute_steps(f.readlines())
    print(f'If the screen did work, there would be {lcd.lit_pixels()} pixels lit up')
    print(lcd)