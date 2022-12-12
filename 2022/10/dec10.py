from queue import Queue


class CPU:
    def __init__(self, program: list[str]):
        self.x = 1
        self.program = Queue()
        self.cycle = 1

        for line in program:
            self.program.put(0)
            if line != 'noop':
                self.program.put(int(line.split()[1]))

    def exec_cycle(self) -> int:
        self.cycle += 1
        self.x += self.program.get()

        cell = (self.cycle-1) % 40
        if cell == 0:
            print()
        lit = self.x-1 <= cell <= self.x+1
        print('#' if lit else '.', end='')

        return self.cycle * self.x

    @property
    def done(self) -> bool:
        return self.program.empty()


with open('2022/10/input.txt') as f:
    cpu = CPU(f.read().splitlines())

total_signal = 0
while not cpu.done:
    signal = cpu.exec_cycle()
    if cpu.cycle in {20, 60, 100, 140, 180, 220}:
        total_signal += signal

print(total_signal)
