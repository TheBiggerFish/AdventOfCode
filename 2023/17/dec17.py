from dataclasses import dataclass
from queue import PriorityQueue

from fishpy.geometry import LatticePoint
from fishpy.pathfinding import Direction
from fishpy.pathfinding.grid import Grid
from fishpy.utility import timer

DIRECTIONS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


@dataclass(frozen=True, order=True)
class State:
    pos: LatticePoint
    turn: int  # how many cells remaining in a line
    dir: Direction


@dataclass(frozen=True, order=True)
class DijkstraItem:
    cost: int
    g: int  # distance from start
    h: int  # heuristic distance from end
    state: State


@timer
def shortest_path(start: LatticePoint, target: LatticePoint, grid: Grid,
                  min_turn: int, max_turn: int) -> int:
    q: PriorityQueue[DijkstraItem] = PriorityQueue()
    state = State(start, min_turn, LatticePoint(0,0))
    q.put(DijkstraItem(cost=0, g=0, h=0, state=state))
    
    seen: set[LatticePoint] = set()
    while not q.empty():
        item: DijkstraItem = q.get()
        state = item.state
        if state in seen:
            continue
        seen.add(state)
        
        if state.pos == target and min_turn <= state.turn <= max_turn:
            return item.g
        
        for direction in DIRECTIONS:
            if direction == -state.dir:
                # Don't allow direction reversal
                continue
            
            same_dir = direction == state.dir
            turn = state.turn+1 if same_dir else state.turn
            if not same_dir and turn < min_turn:
                # If turning, ensure we've hit minimum distance
                continue
            elif same_dir and turn > max_turn:
                # If not turning, ensure we're under max distance
                continue
            
            new_pos = state.pos + direction
            if new_pos not in grid:
                continue
            
            new_turn = turn if same_dir else 1
            new_state = State(pos=new_pos, dir=direction, turn=new_turn)
            
            g = item.g + grid[new_pos].rep
            h = target.manhattan_distance(new_pos)
            cost = g+h
            q.put(DijkstraItem(cost, g, h, new_state))
    raise Exception('Target not found')

def main():
    with open('2023/17/input.txt') as f:
        lines = f.read().splitlines()
    grid = Grid.from_list_of_strings([list(map(int, line)) for line in lines])
    
    start = LatticePoint(0,0)
    target = grid.bounds[1] - LatticePoint(1, 1)
    
    crucible_cost = shortest_path(start, target, grid, 1, 3)
    print(f'The heat cost for the crucible to reach the factory is {crucible_cost}')
    
    ultra_crucible_cost = shortest_path(start, target, grid, 4, 10)
    print(f'The heat cost for the ultra crucible to reach the factory is {ultra_crucible_cost}')


if __name__ == '__main__':
    main()
