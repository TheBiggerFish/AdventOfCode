from functools import reduce


class Rucksack:
    def __init__(self, items: str):
        self.pocket_1 = set(items[:len(items)//2])
        self.pocket_2 = set(items[len(items)//2:])

    @staticmethod
    def priority(item: str):
        if ord('a') <= ord(item) <= ord('z'):
            return ord(item) - ord('a') + 1
        elif ord('A') <= ord(item) <= ord('Z'):
            return ord(item) - ord('A') + 27
        else:
            raise ValueError(f'Item should be a string, found: {type(item)}')

    def find_error(self) -> str:
        overlap = self.pocket_1.intersection(self.pocket_2)
        return list(overlap)[0]

    def bag(self) -> set[str]:
        return self.pocket_1 | self.pocket_2

    @staticmethod
    def badge(group: list['Rucksack']) -> str:
        bags = map(Rucksack.bag, group)
        overlap = reduce(set.intersection, bags)
        return list(overlap)[0]


with open('2022/03/input.txt') as f:
    rucksacks = list(map(Rucksack, f.read().splitlines()))
    groups = [rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)]

errors = map(Rucksack.find_error, rucksacks)
priorities = map(Rucksack.priority, errors)
print(sum(priorities))

badges = map(Rucksack.badge, groups)
priorities = map(Rucksack.priority, badges)
print(sum(priorities))
