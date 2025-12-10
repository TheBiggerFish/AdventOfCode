from functools import partial, cache

@cache
def maximize_joltage(bank: str, digits: int) -> int:
    if digits == 1:
        return int(max(bank))

    maximum = 0
    for i, digit in enumerate(bank[:-digits+1]):
        rest = maximize_joltage(bank[i + 1:], digits - 1)
        maximum = max(maximum, int(digit + str(rest)))

    return maximum

part_1 = partial(maximize_joltage, digits=2)
part_2 = partial(maximize_joltage, digits=12)

with open('input.txt') as f:
    banks = f.read().splitlines()

answer_1 = sum(map(part_1, banks))
print("Answer 1:", answer_1)
answer_2 = sum(map(part_2, banks))
print("Answer 2:", answer_2)