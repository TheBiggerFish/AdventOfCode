from functools import cache

with open('input.txt') as f:
    lines = f.read().splitlines()
    start = lines[0].find('S')

def part_1() -> int:
    splits: int = 0
    beams: set[int] = {start}
    for line in lines[1:]:
        splitters = {i for i, char in enumerate(line) if char == '^'}
        split_beams: set[int] = beams.intersection(splitters)
        splits += len(split_beams)
        new_beams: set[int] = {beam + offset for beam in split_beams for offset in {-1, 1}}
        beams = (beams - split_beams) | new_beams
    return splits

@cache
def part_2(line_index: int = 0, laser: int = start) -> int:
    if line_index >= len(lines):
        return 1

    if lines[line_index][laser] == '^':
        left_paths = part_2(line_index + 1, laser - 1)
        right_paths = part_2(line_index + 1, laser + 1)
        return left_paths + right_paths
    return part_2(line_index + 1, laser)

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')