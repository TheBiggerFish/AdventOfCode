from typing import Optional


def rotate(pattern: list[str]) -> list[str]:
    """Returns a rotated list of strings"""
    return [''.join(col) for col in zip(*pattern)]

def is_symmetric(pattern: list[str], index: int, ignore: Optional[tuple[int, int]] = None) -> bool:
    """Check if the pattern is symmetric around a given index, ignoring up to one pair of indices"""
    if index >= len(pattern):
        return False
    for i in range(0, len(pattern) - index):
        if index - i - 1 < 0:
            break
        if ignore is not None and index+i in ignore:
            continue
        if pattern[index + i] != pattern[index - i - 1]:
            return False
    return True

def symmetry(pattern: list[str]) -> int:
    """Find the symmetry for a given input pattern, or 0 if none"""
    
    # Map each line to the list of indices which look the same
    similars: dict[str, list[int]] = {}
    for i, line in enumerate(pattern):
        similars.setdefault(line, list())
        similars[line].append(i)
        
    for i, line in enumerate(pattern):
        for opp_index in similars[line]:
            if i % 2 == opp_index % 2:
                continue
            possible_middle = (i + opp_index + 1) // 2
            if is_symmetric(pattern, possible_middle):
                return possible_middle
    return 0

def off_by_ones(line: str) -> list[str]:
    """Return a list of strings that are 1 character different from the input"""
    opposite = {
        '.': '#',
        '#': '.',
    }
    
    results = []
    for i, _ in enumerate(line):
        chars = list(line)
        chars[i] = opposite[chars[i]]
        results.append(''.join(chars))
    return results

def smudgy_symmetry(pattern: list[str]) -> int:
    """Find the second symmetry for a given input ignoring one smudge (flipped character)"""
    
    # Ignore the normal symmetry for the given pattern
    ignore = symmetry(pattern)
    
    # Map each line to the list of indices which look the same
    similars: dict[str, list[int]] = {key: list() for key in set(pattern)}
    for i, line in enumerate(pattern):
        similars[line].append(i)
    
    # For each line, find all possible smudges (versions with one flipped character)
    smudgy_similars: list[list[str]] = list(map(off_by_ones, pattern))

    for i, line in enumerate(pattern):
        for similar in smudgy_similars[i]:
            # If smudged line not in pattern, skip it
            if similar not in similars:
                continue
            for opp_index in similars[similar]:
                if i % 2 == opp_index % 2:
                    continue
                possible_middle = (i + opp_index + 1) // 2
                if possible_middle == ignore:
                    continue
                if is_symmetric(pattern, possible_middle, ignore=(i, opp_index)):
                    return possible_middle
    return 0

def main():
    patterns: list[list[str]] = []
    with open('2023/13/input.txt') as f:
        for pattern in f.read().split('\n\n'):
            patterns.append(pattern.strip().split())
    
    summary = 0
    for pattern in patterns:
        summary += 100 * symmetry(pattern)
        summary += symmetry(rotate(pattern))
    print(f'Summarized notes: {summary}')

    smudgy_summary = 0
    for pattern in patterns:
        smudgy_summary += 100 * smudgy_symmetry(pattern)
        smudgy_summary += smudgy_symmetry(rotate(pattern))
    print(f'Smudgy summarized notes: {smudgy_summary}')


if __name__ == '__main__':
    main()
