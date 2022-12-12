from dataclasses import dataclass
from functools import reduce
from queue import Queue
from typing import Callable


@dataclass
class Monkey:
    id: int
    items: Queue[int]
    op: Callable[[int], int]
    test: int
    if_true: int
    if_false: int
    inspected: int = 0

    @staticmethod
    def from_str(config: str) -> 'Monkey':
        id = int(config[0].rstrip(':').split()[-1])

        items = Queue()
        items_str = config[1].split(':')[1].split(',')
        for item in map(int, items_str):
            items.put(item)

        op = Monkey.get_op(*config[2].split()[-2:])
        test = int(config[3].split()[-1])
        if_true = int(config[4].split()[-1])
        if_false = int(config[5].split()[-1])
        return Monkey(id, items, op, test, if_true, if_false)

    def throw_to(self, others: list['Monkey'], worry_reduction: bool, lcm: int):
        while not self.items.empty():
            item = self.items.get()
            item = self.op(item)
            if worry_reduction:
                item //= 3
            item %= lcm  # Mod by least common multiple of test divisors
            if item % self.test == 0:
                others[self.if_true].items.put(item)
            else:
                others[self.if_false].items.put(item)
            self.inspected += 1

    @staticmethod
    def business(monkies: list['Monkey'], rounds: int, worry_reduction: bool) -> int:
        lcm: int = reduce(int.__mul__, [m.test for m in monkies])
        for _ in range(rounds):
            for monkey in monkies:
                monkey.throw_to(monkies, worry_reduction, lcm)
        businesses = sorted([m.inspected for m in monkies], reverse=True)
        return businesses[0] * businesses[1]

    @staticmethod
    def get_op(op: str, value: str) -> Callable[[int], int]:
        if op == '*' and value == 'old':
            return lambda old: old * old
        elif value.isnumeric():
            if op == '*':
                return lambda old: old * int(value)
            elif op == '+':
                return lambda old: old + int(value)
        else:
            raise ValueError('Unknown value passed to operation')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, items={self.items.queue}, test=({self.test}?{self.if_true}:{self.if_false})))'


with open('2022/11/input.txt') as f:
    monkey_strings = list(map(str.splitlines, f.read().split('\n\n')))

    monkies_1: list[Monkey] = list(map(Monkey.from_str, monkey_strings))
    monkey_business = Monkey.business(monkies_1, 20, True)

    monkies_2: list[Monkey] = list(map(Monkey.from_str, monkey_strings))
    monkey_business = Monkey.business(monkies_2, 10000, False)
    print(monkey_business)
