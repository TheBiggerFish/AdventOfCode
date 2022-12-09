from operator import xor

from fishpy.geometry import Direction, LatticePoint, Vector2D

dir_map = {'U': Direction.UP,
           'D': Direction.DOWN,
           'L': Direction.LEFT,
           'R': Direction.RIGHT}


with open('2022/09/input.txt') as f:
    rope = [LatticePoint(0, 0) for _ in range(10)]

    visited: set[LatticePoint] = set()

    for dir, step in map(str.split, f.read().splitlines()):
        for _ in range(int(step)):
            rope[0] += dir_map[dir]
            for i, segment in enumerate(rope[1:], 1):
                lead = rope[i-1]
                relative = lead - segment
                if relative.x > 1 or relative.x < -1 or relative.y < -1 or relative.y > 1:
                    new_pos = segment + LatticePoint(min(relative.x, 1) if relative.x > 0 else max(relative.x, -1),
                                                     min(relative.y, 1) if relative.y > 0 else max(relative.y, -1))
                    segment.x, segment.y = new_pos.x, new_pos.y
                else:
                    break
            visited.add(rope[-1].copy())
    print(len(visited))
