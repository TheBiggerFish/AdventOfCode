# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/23


from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding.depthfirst import shortest_path
from fishpy.pathfinding import Dijkstra
from fishpy.utility.debug import profile,timer
from copy import copy


class LatticeHash(LatticePoint):
    def __hash__(self) -> int:
        return self.y * 100 + self.x

    @staticmethod
    def from_point(pt:LatticePoint):
        return LatticeHash(pt.x,pt.y)

with open('2021/23/input_2.txt') as f:
    grid = Grid.from_list_of_strings(f.read().splitlines())
wall_positions = grid.char_positions('# ')
walls = {LatticeHash.from_point(pos) for char in wall_positions for pos in wall_positions[char]}
ROOM_SIZE = grid.height - 3

class Amphipod:
    MOVE_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    BANNED_POSITIONS = {LatticeHash(3,1),LatticeHash(5,1),LatticeHash(7,1),LatticeHash(9,1)}
    ALLOWED_ROOMS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}

    def __init__(self,position:LatticeHash,type:str):
        self.position = position
        self.type = type

    def __hash__(self) -> int:
        return hash((self.position,self.type))

    def __eq__(self,other:'Amphipod') -> bool:
        return self.position == other.position and self.type == other.type

    def cost(self,pos:LatticeHash) -> int:
        if self.position.y > 1 and pos.y > 1:
            return Amphipod.MOVE_COST[self.type] * self.position.manhattan_distance(LatticeHash(pos.x,2-pos.y))
        return Amphipod.MOVE_COST[self.type] * self.position.manhattan_distance(pos)

    def copy(self) -> 'Amphipod':
        return Amphipod(self.position.copy(),self.type)

    def __repr__(self) -> str:
        return f'Amphipod({self.type}:{self.position})'

    def is_allowed_space(self,pos:LatticeHash) -> bool:
        if pos.y == 1 and pos not in Amphipod.BANNED_POSITIONS:
            return True
        if pos.y > 1 and pos.x == Amphipod.ALLOWED_ROOMS[self.type]:
            return True
        return False

    def valid_moves(self,neighbor_positions:dict[LatticeHash,str]) -> list[tuple[LatticeHash,int]]:
        moves:list[LatticeHash] = []
        cost_per_step = Amphipod.MOVE_COST[self.type]
        goal_room = Amphipod.ALLOWED_ROOMS[self.type]

        blocking_neighbor = False
        if self.position.x == goal_room:
            for y in range(self.position.y,3+ROOM_SIZE):
                pos = LatticeHash(self.position.x,y)
                if pos in neighbor_positions and Amphipod.ALLOWED_ROOMS[neighbor_positions[pos]] != goal_room:
                    blocking_neighbor = True
                    break

        if self.position.x != goal_room or blocking_neighbor:
            for y in range(self.position.y-1,1,-1):
                if LatticeHash(self.position.x,y) in neighbor_positions:
                    return []
            if self.position.y > 1:
                for x in range(self.position.x-1,0,-1):
                    steps = self.position.y - 1 + abs(self.position.x - x)
                    pos = LatticeHash(x,1)
                    if pos in neighbor_positions:
                        break
                    if x < 3 or x > 9 or x % 2 == 0:
                        moves.append((pos,steps*cost_per_step))
                for x in range(self.position.x+1,12):
                    steps = self.position.y - 1 + abs(self.position.x - x)
                    pos = LatticeHash(x,1)
                    if pos in neighbor_positions:
                        break
                    if x < 3 or x > 9 or x % 2 == 0:
                        moves.append((pos,steps*cost_per_step))
            else:
                if self.position.x < goal_room:
                    range_args = (self.position.x+1,goal_room)
                else:
                    range_args = (self.position.x-1,goal_room,-1)
                for x in range(*range_args):
                    if LatticeHash(x,1) in neighbor_positions:
                        return []
                x_dist = abs(self.position.x-goal_room)
                for y in range(ROOM_SIZE+1,1,-1):
                    y_dist = y-1
                    pos = LatticeHash(goal_room,y)
                    if pos in neighbor_positions and Amphipod.ALLOWED_ROOMS[neighbor_positions[pos]] != goal_room:
                        return []
                    if pos not in neighbor_positions:
                        moves.append((pos,(x_dist+y_dist)*cost_per_step))
        return moves

class SimState:
    def __init__(self,amphipods:list[Amphipod],cost:int=0):
        self.amphipods = amphipods
        self.cost = cost
        self.creation_cost = 0

    def __repr__(self) -> str:
        return f'SimState{str(self.amphipods)}'

    def __eq__(self,other:'SimState') -> str:
        self_positions = {amph.position:amph.type for amph in self.amphipods}
        other_positions = {amph.position:amph.type for amph in other.amphipods}
        for pos in self_positions:
            if pos not in other_positions:
                return False
            if self_positions[pos] != other_positions[pos]:
                return False
        return True

    def __hash__(self) -> int:
        return hash(tuple([hash(amph) for amph in self.amphipods]))

    def get_adjacent_states(self) -> list['SimState']:
        adj:list[SimState] = []
        amph_positions = {amph.position:amph.type for amph in self.amphipods}
        for i,amph in enumerate(self.amphipods):
            for move,cost in amph.valid_moves(amph_positions):
                state_copy = SimState(copy(self.amphipods),self.cost+cost)
                state_copy.creation_cost = cost
                state_copy.amphipods[i] = Amphipod(move,amph.type)
                adj.append(state_copy)
        return adj

    def heuristic(self,_) -> int:
        cost = 0
        for amph in self.amphipods:
            goal_x = Amphipod.ALLOWED_ROOMS[amph.type]
            if amph.position.x != goal_x:
                cost += amph.cost(LatticeHash(goal_x,2))
        return cost

@timer
def main():
    a_pos = grid.char_positions('ABCD')
    initial_state = SimState([Amphipod(LatticeHash.from_point(pos),letter) for letter in a_pos for pos in a_pos[letter]])
    goal_state = SimState([Amphipod(LatticeHash(Amphipod.ALLOWED_ROOMS[type],y),type) for type in 'ABCD' for y in range(2,2+ROOM_SIZE)])
    print(goal_state)
    dijkstra = Dijkstra(initial_state,goal_state,
                        adjacency_function=SimState.get_adjacent_states,
                        heuristic_function=SimState.heuristic,
                        cost_function=lambda _,state: state.creation_cost)
    moves = dijkstra.search()
    print(moves,'\n')
    # print(initial_state,'\n')
    # for state in dijkstra.path:
    #     print(state,state.creation_cost)


if __name__ == '__main__':
    main()