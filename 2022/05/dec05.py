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

    def execute(self, instruction: Instruction) -> None:
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
    for instruction in instructions:
        s.execute(instruction)
    print(s.snapshot())
