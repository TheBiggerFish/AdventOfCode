from dataclasses import dataclass
from typing import Optional


@dataclass
class Lense:
    label: str
    focus: Optional[int] = None

    @staticmethod
    def hash(label: str) -> int:
        value = 0
        for char in label:
            value += ord(char)
            value *= 17
        return value % 256

class LenseBox:
    def __init__(self, box_id):
        self.lenses: list[Lense] = []
        self.id = box_id
    
    def focus_power(self) -> int:
        power = 0
        for slot, lense in enumerate(self.lenses, 1):
            power += lense.focus * slot
        return power * self.id

    def add_lense(self, lense: Lense):
        for i, _ in enumerate(self.lenses):
            if self.lenses[i].label == lense.label:
                self.lenses[i] = lense
                return
        self.lenses.append(lense)
    
    def remove_lense(self, label: str):
        for i, lense in enumerate(self.lenses):
            if lense.label == label:
                del self.lenses[i]
                break

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, lenses={self.lenses})'

def main():
    with open('2023/15/input.txt') as f:
        sequence = f.readline().strip().split(',')
    
    hash_sum = 0
    hash_map: dict[int, LenseBox] = {i: LenseBox(box_id=i+1) for i in range(256)}
    for step in sequence:
        hash_sum += Lense.hash(label=step)
        if '=' == step[-2]:
            label, focus = step.split('=')
            lense = Lense(label, int(focus))
            hash_ = Lense.hash(label)
            hash_map[hash_].add_lense(lense)
        elif '-' == step[-1]:
            label = step.strip('-')
            hash_ = Lense.hash(label)
            hash_map[hash_].remove_lense(label)

    print(f'The sum of initialization steps is {hash_sum}')

    power = sum(box.focus_power() for box in hash_map.values())
    print(f'The sum of focusing power of the lenses is {power}')


if __name__ == '__main__':
    main()
