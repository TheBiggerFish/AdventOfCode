from itertools import combinations

from fishpy.pathfinding import dijkstra
from dataclasses import dataclass
from math import prod, ceil
from functools import cache, cached_property
from typing import Any, Callable, Optional
from collections import deque
from statistics import mean
from typing import Iterable, Union
import numpy as np

def all_combinations(elements: Iterable[Any]) -> Iterable[tuple[Any]]:
    """Generate all combinations of the given elements"""
    el_list = list(elements)
    for r in range(len(el_list)+1):
        for combo in combinations(el_list, r):
            yield combo


@dataclass(frozen=True)
class MachineState:
    indicator_state: tuple[bool]
    indicator_goal: tuple[bool]
    wirings: tuple[tuple[int]]
    joltage_goal: Optional[tuple[int]] = None

    @staticmethod
    def parse_string(line: str) -> 'MachineState':
        indicator_string, *wiring_string, joltage_string = line.split()
        indicator_goal = tuple(c == "#" for c in indicator_string[1:-1])
        button_wiring = tuple((*map(int, wiring[1:-1].split(',')),) for wiring in wiring_string)
        joltage_goal = tuple(int(j) for j in joltage_string[1:-1].split(','))
        indicator_state = tuple([False] * len(indicator_goal))
        joltage_state = tuple([0] * len(joltage_goal))
        return MachineState(indicator_state=indicator_state, indicator_goal=indicator_goal,
                            joltage_goal=joltage_goal, wirings=button_wiring)

    @cached_property
    def wire_deltas(self) -> list[list[int]]:
        return [[(1 if i in wiring else 0) for i in range(len(self.joltage_goal))] for wiring in self.wirings]

    def solve_indicators(self) -> int:
        return min(map(len,self._solve_indicators_helper(self.indicator_goal)))

    def _solve_indicators_helper(self, indicator_goal: tuple[bool]) -> list[set[int]]:
        valid_combo: list[list[int]] = []
        for combo in all_combinations(self.wire_deltas):
            indicator_state = (False,) * len(indicator_goal)
            for wiring in combo:
                indicator_state = tuple(s ^ (wiring[i] == 1) for i, s in enumerate(indicator_state))
            if indicator_state == indicator_goal:
                valid_combo.append(combo)
        return valid_combo

    def solve_joltage(self) -> int:
        return self._solve_joltage_helper(self.joltage_goal)

    @cache
    def _solve_joltage_helper(self, current_joltage: tuple[int]) -> int:
        if not any(current_joltage):
            return 0

        min_steps = float('inf')
        parity = tuple(bool(j % 2) for j in current_joltage)
        for button_combo in self._solve_indicators_helper(parity):
            # Prune search if already worse than best found
            if len(button_combo) >= min_steps:
                continue

            # Add up button effects
            combined_buttons = tuple(map(sum,zip(*button_combo, (0,)*len(current_joltage))))

            # Calculate new joltage after pressing buttons and halving
            new_joltage = tuple((jolt - offset) // 2 for jolt, offset in zip(current_joltage, combined_buttons))

            # Invalid state, skip
            if any(x < 0 for x in new_joltage):
                continue

            # Recurse to solve for new joltage. Double the steps to make up for halving
            steps = len(button_combo) + 2 * self._solve_joltage_helper(new_joltage)

            # Update minimum steps found
            if steps < min_steps:
                min_steps = steps
        return min_steps

with open('input.txt') as f:
    lines = f.read().splitlines()
    machines = list(map(MachineState.parse_string, lines))

answer_1 = sum(map(MachineState.solve_indicators, machines))
print(f'Part 1: {answer_1}')

# for i, machine in enumerate(machines):
#     steps = machine.solve_joltage()
#     print(f'Machine {i} | steps to solve joltage: {steps}')

import time
start = time.perf_counter()
answer_2 = sum(map(MachineState.solve_joltage, machines))
elapsed = time.perf_counter() - start
print(f'Result: {answer_2}  Elapsed: {elapsed:.6f}s')
# answer_2 = sum(map(MachineState.solve_joltage, machines))
# print(f'Part 2: {answer_2}')
