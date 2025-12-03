from math import log10
from fishpy.structures.range import Range

def is_invalid_simple(id_) -> bool:
    digits = log10(id_) + 1
    mask = 10 ** (int(digits) // 2)
    left = id_ // mask
    right = id_ % mask
    return left == right

def is_invalid_stringy(id_) -> bool:
    id_str = str(id_)
    for i in range(1, len(id_str) // 2 + 1):
        if len(id_str) % i != 0:
            continue
        repetitions = len(id_str) // i
        if id_str[:i] * repetitions == id_str:
            return True
    return False

answer_1 = 0
answer_2 = 0
with open('input.txt') as f:
    id_ranges = map(lambda string: Range.from_string(string, True),
                    f.readline().split(','))

for id_range in id_ranges:
    for value in id_range:
        if is_invalid_simple(value):
            answer_1 += value
        if is_invalid_stringy(value):
            answer_2 += value
print(f'Part 1: {answer_1}, Part 2: {answer_2}')



