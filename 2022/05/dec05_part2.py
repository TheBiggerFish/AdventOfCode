from dataclasses import dataclass

from fishpy.structures import Stack


@dataclass
class Crate:
    contents: str

    def __str__(self) -> str:
        return f'[{self.contents}]'


@dataclass
class Instruction:
    count: int
    start: int
    dest: int

    @staticmethod
    def from_string(string: str) -> 'Instruction':
        count, start, dest = map(int, string.split()[1:6:2])
        return Instruction(count, start, dest)


@dataclass
class Stacks:
    stacks: list[Stack[Crate]]

    @staticmethod
    def from_lists(crates: list[list[str]]):
        # print(crates)
        columns = [[Crate(crate[1]) for crate in col if crate]
                   for col in zip(*crates)]
        stacks = [Stack.from_list(list(reversed(col))) for col in columns]
        return Stacks(stacks)

    def pop_multiple(self, stack: int, count: int) -> list[str]:
        return [self.stacks[stack-1].pop() for _ in range(count)]

    def push_multiple(self, stack: int, items: list[str]):
        for item in items:
            self.stacks[stack-1].push(item)

    def execute(self, instruction: Instruction, move_multiple: bool = False) -> None:
        if move_multiple:
            crates = self.pop_multiple(instruction.start,
                                       instruction.count)
            self.push_multiple(instruction.dest, crates[::-1])
        else:
            for _ in range(instruction.count):
                crate = self.stacks[instruction.start-1].pop()
                self.stacks[instruction.dest-1].push(crate)

    def snapshot(self) -> str:
        return ''.join(str(stack.peek().contents) for stack in self.stacks)


with open('2022/05/input.txt') as f:
    crates, instructions = f.read().split('\n\n')
    rows = [[line[i:i+4].strip() for i in range(0, len(line), 4)]
            for line in crates.splitlines()]
    s = Stacks.from_lists(rows[:-1])
    instructions = map(Instruction.from_string, instructions.splitlines())
    # map(s.execute, instructions)
    for _, instruction in enumerate(instructions):
        s.execute(instruction, True)
    print(s.snapshot())
