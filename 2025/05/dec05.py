from functools import partial
from fishpy.structures import Range

InclusiveRange = partial(Range.from_string, upper_inclusive=True)


def merged(ranges: list[Range]) -> list[Range]:
    """Merge all overlapping ranges together where possible"""
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)  # Sort by lower bound
    merged_ranges = [sorted_ranges[0]]  # Initialize with the first range
    for current in sorted_ranges[1:]:
        last = merged_ranges[-1]  # Peek at the last item in the stack
        if last.overlap(current):  # If they overlap, merge them together
            merged_ranges[-1] = last.combine(current)
        else:  # No overlap, keep it as is
            merged_ranges.append(current)
    return merged_ranges

with open('input.txt') as f:
    range_input, item_input = f.read().split('\n\n')
ranges = map(InclusiveRange, range_input.splitlines())
ranges = merged(ranges)
items = map(int, item_input.splitlines())

answer_1 = 0
for item_id in items:
    fresh = any(True for id_range in ranges if item_id in id_range)
    if fresh:
        answer_1 += 1

answer_2 = 0
for id_range in ranges:
    answer_2 += len(id_range)
print(f'Number of fresh items in inventory: {answer_1}')
print(f'Total number of fresh items: {answer_2}')