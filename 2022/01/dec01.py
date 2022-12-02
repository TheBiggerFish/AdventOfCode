from dataclasses import dataclass
from functools import cached_property

@dataclass
class Elf:
    food: list[int]

    @cached_property
    def calories(self) -> int:
        return sum(self.food)

    def __lt__(self, other: 'Elf') -> bool:
        return self.calories < other.calories

with open('2022/01/input.txt') as f:
    elves = [Elf(list(map(int,block.split()))) for block in f.read().split('\n\n')]
    top_3 = sorted(elves, reverse=True)[:3]
    total = sum(map(lambda elf: elf.calories, top_3))
    print(total)