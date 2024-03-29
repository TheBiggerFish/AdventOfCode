import re
from dataclasses import dataclass

import yaml

# Global variable which has all workflows loaded in main()
workflows: dict[str, 'Workflow']

@dataclass
class Range:
    """Tracks a range of valid integers"""
    low: int
    high: int
    
    def lt(self, value: int):
        """Limit the range to fit the condition 'less than'"""
        return Range(self.low, min(self.high, value - 1))

    def gt(self, value: int):
        """Limit the range to fit the condition 'greater than'"""
        return Range(max(self.low, value + 1), self.high)

    def le(self, value: int):
        """Limit the range to fit the condition 'less than or equal'"""
        return Range(self.low, min(self.high, value))
    
    def ge(self, value: int):
        """Limit the range to fit the condition 'greater than or equal'"""
        return Range(max(self.low, value), self.high)

    @property
    def count(self) -> int:
        """The number of valid integers in the range"""
        return self.high - self.low + 1


@dataclass
class PartRanges:
    """Tracks a whole set of accepted parts in the form of multiple ranges"""
    x: Range
    m: Range
    a: Range
    s: Range

    def apply_condition(self, cond: 'Condition') -> tuple['PartRanges', 'PartRanges']:
        """Returns 2 versions of self, one having a condition applied and the other having an inversion of the condition applied"""
        func = {'<': Range.lt, '>': Range.gt}[cond.comparison]
        inv_func = {'<': Range.ge, '>': Range.le}[cond.comparison]
        match cond.property:
            case 'x':
                return PartRanges(func(self.x, cond.value), self.m, self.a, self.s), PartRanges(inv_func(self.x, cond.value), self.m, self.a, self.s)
            case 'm':
                return PartRanges(self.x, func(self.m, cond.value), self.a, self.s), PartRanges(self.x, inv_func(self.m, cond.value), self.a, self.s)
            case 'a':
                return PartRanges(self.x, self.m, func(self.a, cond.value), self.s), PartRanges(self.x, self.m, inv_func(self.a, cond.value), self.s)
            case 's':
                return PartRanges(self.x, self.m, self.a, func(self.s, cond.value)), PartRanges(self.x, self.m, self.a, inv_func(self.s, cond.value))
            case other:
                raise ValueError(f'Unknown property: {other}')

    @property
    def count(self) -> int:
        """The number of accepted parts within the PartRanges"""
        return max(0, self.x.count * self.m.count * self.a.count * self.s.count)


@dataclass(frozen=True)
class Part:
    """Stores a single part"""
    x: int
    m: int
    a: int
    s: int
    
    def __getitem__(self, key: str) -> int:
        """Provides a [] accessor on the Part object"""
        match(key):
            case 'x':
                return self.x
            case 'm':
                return self.m
            case 'a':
                return self.a
            case 's':
                return self.s
            case other:
                raise KeyError(f'Could not find key: {other}')

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s

    @property
    def accepted(self) -> bool:
        """Follow the workflow for the part to determine whether its an accepted part"""
        flow = 'in'
        while flow != 'A' and flow != 'R':
            flow = workflows[flow].flow(self)
        return flow == 'A'


class Condition:
    """Represents a conditional branch of a workflow"""
    def __init__(self, string):
        matches = re.findall(r'(\w)([><])(\d+):(\w+)', string)[0]
        self.property = matches[0]
        self.comparison = matches[1]
        self.value = int(matches[2])
        self.branch = matches[3]

    def matches(self, part: Part) -> bool:
        """Predicate to determine if a part passes the condition"""
        value = part[self.property]
        if self.comparison == '<' and value < self.value:
            return True
        elif self.comparison == '>' and value > self.value:
            return True
        return False


class Workflow:
    """Represents a single workflow with conditional and default branches"""
    def __init__(self, string):
        matches = re.findall(r'[\d\w><:]+', string)
        self.name = matches[0]
        self.conditions = list(map(Condition, matches[1:-1]))
        self.default = matches[-1]

    def flow(self, part: Part) -> str:
        """Follow the workflow for a single part"""
        for condition in self.conditions:
            if condition.matches(part):
                return condition.branch
        return self.default


def accepted_ranges(start: str, initial_range: PartRanges) -> list[PartRanges]:
    """Recursively build a list of PartRanges to represent "Accepted" parts"""
    if start == 'A':
        return [initial_range]
    elif start == 'R':
        return []
    ranges: list[PartRanges] = []
    current_range = initial_range
    workflow = workflows[start]
    for condition in workflow.conditions:
        current_range, otherwise_range = current_range.apply_condition(condition)
        ranges += accepted_ranges(condition.branch, current_range)
        current_range = otherwise_range
    ranges += accepted_ranges(workflow.default, current_range)
    return ranges


def main():
    global workflows
    with open('2023/19/input.txt') as f:
        workflow_str, parts_str = f.read().split('\n\n')
    workflows = {workflow.name: workflow for workflow in map(Workflow, workflow_str.split())}

    # Parse parts input for part 1
    def json_loads(part: str) -> Part:
        part = part.replace('=',': ')
        return Part(**yaml.safe_load(part))
    parts: list[Part] = list(map(json_loads, parts_str.splitlines()))
    
    # Part 1
    value = sum(part.value for part in parts if part.accepted)
    print(f'The sum of accepted parts is {value}')
    
    # Part 2
    accepted = accepted_ranges('in', PartRanges(
        x=Range(1, 4000), m=Range(1, 4000),
        a=Range(1, 4000), s=Range(1, 4000),
    ))
    total = sum(a_range.count for a_range in accepted)
    print(f'The number of accepted parts is {total}')
    

if __name__ == '__main__':
    main()
