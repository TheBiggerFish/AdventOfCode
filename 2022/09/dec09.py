from fishpy.geometry import Direction, LatticePoint, Vector2D

dir_map = {'U': Direction.UP,
           'D': Direction.DOWN,
           'L': Direction.LEFT,
           'R': Direction.RIGHT}


class Rope:
    def __init__(self, segments: int):
        self.segments = [LatticePoint(0, 0) for _ in range(segments)]
        self.visited: set[LatticePoint] = set()

    @property
    def head(self) -> LatticePoint:
        return self.segments[0]

    @head.setter
    def head(self, value: LatticePoint):
        self.segments[0] = value

    @property
    def tail(self) -> LatticePoint:
        return self.segments[-1]

    def move_head(self, direction: Vector2D, steps: int):
        for _ in range(steps):
            self.head: LatticePoint = self.head + direction
            for i, follower in enumerate(self.segments[1:], 1):
                leader = self.segments[i-1]
                new_pos = Rope._pull(leader, follower)
                if new_pos == follower:
                    # If this segment doesn't move, later segments also won't need to
                    break
                self.segments[i] = new_pos
            self.visited.add(self.tail.copy())

    @staticmethod
    def _pull(leader: LatticePoint, follower: LatticePoint) -> LatticePoint:
        if leader.is_adjacent(follower, diagonals=True):
            return follower
        relative = leader - follower
        step = relative.clamp_bounds(lower_bound=LatticePoint(-1, -1),
                                     upper_bound=LatticePoint(1, 1))
        return follower + step


with open('2022/09/input.txt') as f:
    rope_2 = Rope(2)
    rope_10 = Rope(10)
    for dir, step in map(str.split, f.read().splitlines()):
        dir, step = dir_map[dir], int(step)
        rope_2.move_head(dir, step)
        rope_10.move_head(dir, step)
    print(f'Tail of 2-segment rope visited {len(rope_2.visited)} positions')
    print(f'Tail of 10-segment rope visited {len(rope_10.visited)} positions')
