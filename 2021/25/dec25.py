from typing import Optional

from fishpy.geometry import LatticePoint
from fishpy.pathfinding import Location
from fishpy.pathfinding.grid import Grid


class CucumberTrench(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def new_pos(self, pos: LatticePoint) -> Optional[LatticePoint]:
        if self[pos].rep == 'v':
            return pos.up() % self.size
        if self[pos].rep == '>':
            return pos.right() % self.size
        return None

    def next_state(self) -> tuple[bool, 'CucumberTrench']:
        changed = False
        for symbol in '>v':
            cucumbers = self.char_positions('>v')
            occupied = set(cucumbers['>']) | set(cucumbers['v'])
            for cuc in cucumbers[symbol]:
                new_pos = self.new_pos(cuc)
                if new_pos is not None and new_pos not in occupied:
                    self[new_pos].rep = symbol
                    self[cuc].rep = '.'
                    changed = True
        return changed, self


with open('2021/25/input.txt') as f:
    changed, g = True, CucumberTrench.from_list_of_strings(f.read().split())
    i = 0
    while changed:  # 429 cycles
        changed, g = g.next_state()
        i += 1
        if i % 10 == 0:
            print(i)
            print(g.to_string(''))
            print()
    print(i)
