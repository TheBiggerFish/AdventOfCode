# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/18


from typing import Optional, Union
from fishpy.mathematics.arithmetic import GroupOperation



class SnailfishNumber:
    def __init__(self,left:Union[int,'SnailfishNumber'],right:Union[int,'SnailfishNumber']):
        self.left = left
        self.right = right
        self.parent:Optional[SnailfishNumber] = None

    def __str__(self):
        return f'[{str(self.left)},{str(self.right)}]'
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash((hash(self.left),hash(self.right)))

    def __add__(self,other:'SnailfishNumber') -> 'SnailfishNumber':
        sn = SnailfishNumber(self,other)
        if isinstance(sn.left,SnailfishNumber):
            sn.left.parent = sn
        if isinstance(sn.right,SnailfishNumber):
            sn.right.parent = sn
        return sn

    @staticmethod
    def from_string(string:str) -> Union[int,'SnailfishNumber']:
        if string.isdigit():
            return int(string)
        if string[1].isdigit():
            i = 1
            while string[i].isdigit():
                i += 1
            left = string[1:i]
            right = string[i+1:-1]
        else:
            split = GroupOperation('[',']').find_matching_operator(string,1)+1
            left = string[1:split]
            right = string[split+1:-1]
        return SnailfishNumber.__add__(SnailfishNumber.from_string(left),
                                       SnailfishNumber.from_string(right))

    def _explode_to_left_neighbor(self) -> bool:
        cur = self
        while cur.parent.left == cur:
            cur = cur.parent
            if cur.parent is None:
                return False

        if isinstance(cur.parent.left,int):
            cur.parent.left += self.left
            return True

        cur = cur.parent.left
        while isinstance(cur,SnailfishNumber) and isinstance(cur.right,SnailfishNumber):
            cur = cur.right
        cur.right += self.left
        return True

    def _explode_to_right_neighbor(self) -> bool:
        cur = self
        while cur.parent.right == cur:
            cur = cur.parent
            if cur.parent is None:
                return False

        if isinstance(cur.parent.right,int):
            cur.parent.right += self.right
            return True

        cur = cur.parent.right
        while isinstance(cur,SnailfishNumber) and isinstance(cur.left,SnailfishNumber):
            cur = cur.left
        cur.left += self.right
        return True

    def _explode_once(self):
        if not isinstance(self.left,int) or not isinstance(self.right,int):
            raise TypeError('A node must be a leaf to be exploded')
        self._explode_to_left_neighbor()
        self._explode_to_right_neighbor()
        if self == self.parent.right:
            self.parent.right = 0
        if self == self.parent.left:
            self.parent.left = 0
        
    def _split_once(self,is_left:bool):
        if is_left:
            self.left = SnailfishNumber(self.left//2,self.left//2+self.left%2)
            self.left.parent = self
        else:
            self.right = SnailfishNumber(self.right//2,self.right//2+self.right%2)
            self.right.parent = self

    def _try_explode(self,depth:int=0) -> bool:
        if depth == 4:
            self._explode_once()
            return True
        for child in (self.left,self.right):
            if isinstance(child,SnailfishNumber) and child._try_explode(depth+1):
                return True
        return False

    def _try_split(self) -> bool:
        for child,is_left in ((self.left,True),(self.right,False)):
            if isinstance(child,int) and child >= 10:
                self._split_once(is_left)
                return True
            if isinstance(child,SnailfishNumber) and child._try_split():
                return True

    def magnitude(self):
        mag = 0
        if isinstance(self.left,SnailfishNumber):
            mag += 3 * self.left.magnitude()
        else:
            mag += 3 * self.left
        if isinstance(self.right,SnailfishNumber):
            mag += 2 * self.right.magnitude()
        else:
            mag += 2 * self.right
        return mag
        
    def reduce(self):
        while self._try_explode() or self._try_split():
            pass
        return self

with open('2021/18/input.txt') as f:
    lines = f.read().rstrip().split()
    

result = SnailfishNumber.from_string(lines[0])
for line in lines[1:]:
    result:SnailfishNumber = result + SnailfishNumber.from_string(line)
    result.reduce()
    # print(result)
print('Answer 1:',result.magnitude())


top_mag = 0
for i,line_1 in enumerate(lines):
    for j,line_2 in enumerate(lines):
        if i == j:
            continue
        result:SnailfishNumber = SnailfishNumber.from_string(line_1) + SnailfishNumber.from_string(line_2)
        mag = result.reduce().magnitude()
        if mag > top_mag:
            top_mag = mag
print('Answer 2:',top_mag)