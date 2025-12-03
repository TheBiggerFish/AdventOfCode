from functools import partial, lru_cache

@lru_cache(maxsize=None)
def maximize_joltage(bank: str, digits: int = 2) -> int:
    if digits == 1:
        return int(max(bank))

    maximum = 0
    for i, digit in enumerate(bank[:-digits+1]):
        rest = maximize_joltage(bank[i + 1:], digits - 1)
        value = int(digit + str(rest))
        if value > maximum:
            maximum = value

    return maximum

part2 = partial(maximize_joltage, digits=12)

with open('input.txt') as f:
    banks = f.read().splitlines()


answer_1 = sum(map(maximize_joltage, banks))
print("Answer 1:", answer_1)
answer_2 = sum(map(part2, banks))
print("Answer 2:", answer_2)