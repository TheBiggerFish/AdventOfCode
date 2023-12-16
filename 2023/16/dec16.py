from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding import Direction
from fishpy.geometry import LatticePoint
from dataclasses import dataclass
from queue import Queue

@dataclass(frozen=True)
class BeamHead:
    """Represents the state of the "head" of a beam"""
    pos: LatticePoint
    dir: Direction

# A mapping of the direction each mirror reflects an incoming beam
mirror: dict[str, dict[Direction, Direction]] = {
    '/': {
        Direction.NORTH: Direction.EAST,
        Direction.SOUTH: Direction.WEST,
        Direction.EAST: Direction.NORTH,
        Direction.WEST: Direction.SOUTH,
    },
    '\\': {
        Direction.NORTH: Direction.WEST,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
        Direction.WEST: Direction.NORTH,
    }
}

# A mapping of the directions each splitter sends an incoming beam
splitter: dict[str, dict[Direction, tuple[Direction]]] = {
    '-': {
        Direction.NORTH: (Direction.EAST, Direction.WEST),
        Direction.SOUTH: (Direction.EAST, Direction.WEST),
        Direction.EAST: (Direction.EAST,),
        Direction.WEST: (Direction.WEST,),
    },
    '|': {
        Direction.NORTH: (Direction.NORTH,),
        Direction.SOUTH: (Direction.SOUTH,),
        Direction.EAST: (Direction.NORTH, Direction.SOUTH),
        Direction.WEST: (Direction.NORTH, Direction.SOUTH),
    },
}

def energized(grid: Grid, start: BeamHead) -> int:
    """Returns the number of cells that a given beam passes through"""
    seen: set[LatticePoint] = set()
    states: set[BeamHead] = set()
    beams: Queue[BeamHead] = Queue()
    beams.put(start)

    while not beams.empty():
        incoming = beams.get()
        if incoming in states:
            continue
        states.add(incoming)

        pos = incoming.pos
        if pos not in grid:
            continue
        seen.add(pos)

        next_dir: Direction
        char = grid[pos].rep
        if char in mirror:
            next_dir = mirror[char][incoming.dir]
            outgoing = BeamHead(pos + next_dir, next_dir)
            beams.put(outgoing)
        elif char in splitter:
            for next_dir in splitter[char][incoming.dir]:
                outgoing = BeamHead(pos + next_dir, next_dir)
                beams.put(outgoing)
        elif char == '.':
            outgoing = BeamHead(pos + incoming.dir, incoming.dir)
            beams.put(outgoing)
    return len(seen)


def main():
    with open('2023/16/input.txt') as f:
        lines = f.read().splitlines()
    grid = Grid.from_list_of_strings(lines)

    start = BeamHead(LatticePoint(0,0), Direction.EAST)
    beams: Queue[BeamHead] = Queue()
    beams.put(start)

    single_energized = energized(grid, start)
    print(f'There were {single_energized} tiles energized by the single beam')
    
    highest = 0
    for x in range(grid.width):
        highest = max(highest, energized(grid, BeamHead(LatticePoint(x, 0), Direction.SOUTH)))
        highest = max(highest, energized(grid, BeamHead(LatticePoint(x, grid.height-1), Direction.NORTH)))
    for y in range(grid.height):
        highest = max(highest, energized(grid, BeamHead(LatticePoint(0, y), Direction.EAST)))
        highest = max(highest, energized(grid, BeamHead(LatticePoint(grid.width-1, y), Direction.WEST)))
    print(f'There were {highest} tiles energized by best beam')

if __name__ == '__main__':
    main()
