# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/11


import re, itertools
from EulerLib.pathfinding import Dijkstra
from EulerLib.debug import profile

input = '2016/11/input2.txt'

class Compatible:
    def __init__(self,element:str,type:int,floor:int):
        self.element = element
        self.type = type
        self.floor = floor

    @property
    def print_str(self) -> str:
        suffix = 'M' if self.type == 'microchip' else ''
        suffix = 'G' if self.type == 'generator' else suffix
        return self.element[:2].upper() + suffix

    def __str__(self) -> str:
        return f'{self.element} {self.type} on floor {self.floor}'
    
    @staticmethod
    def create_list_from_string(string:str,id:int) -> list:
        generators = re.findall(r'([a-zA-Z]+) generator',string)
        generators = [Compatible(x,'generator',id) for x in generators]

        chips = re.findall(r'([a-zA-Z]+)-compatible microchip',string)
        chips = [Compatible(x,'microchip',id) for x in chips]

        return generators + chips

    def __lt__(self,other) -> bool:
        if self.element < other.element:
            return True
        if self.element > other.element:
            return False
        return self.type < other.type
    
    def __eq__(self,other) -> bool:
        return self.element == other.element and self.type == other.type
    
    def __hash__(self) -> int:
        return hash(self.element[:2]+self.type[0]+str(self.floor))

    def move_floor(self,new_floor):
        return Compatible(self.element,self.type,new_floor)


class Building:
    def __init__(self,items:list,floors:int,elevator:int=1,new=False):
        self.items = items
        if new:
            self.items = sorted(self.items)
        self.floors = floors
        self.elevator = elevator

    def __str__(self) -> str:
        string = ''
        for i in range(self.floors,0,-1):
            string += f'F{i}  {"E" if i == self.elevator else "."} '
            for item in self.items:
                if item.floor == i:
                    string += ' ' + item.print_str + ''
                else:
                    string += '  . '
            string += '\n'
        return string.strip()

    def __eq__(self,other) -> bool:
        return self.elevator == other.elevator and self.floors == other.floors and len(self.items) == len(other.items) and len([True for i in range(len(self.items)) if self.items[i].floor != other.items[i].floor or self.items[i] != other.items[i]]) == 0

    def __hash__(self):
        # return hash(tuple(self.items + [self.elevator]))
        string = f'{self.elevator}{self.floors}'
        for item in self.items:
            string += str(item)
        return hash(string)

    def is_valid_state(self) -> bool:
        return not self.is_fail_state()

    def is_fail_state(self) -> bool:
        safe_elevator = False

        for i in range(0,len(self.items),2):
            gen = self.items[i]
            chip = self.items[i+1]
            if gen.floor == self.elevator or chip.floor == self.elevator:
                safe_elevator = True
            if gen.floor == chip.floor:
                continue

            for j in range(0,len(self.items),2):
                gen = self.items[j]
                if chip.floor == gen.floor:
                    return True
        return not safe_elevator

    def set_elevator_floor(self,floor):
        return Building(self.items[:],self.floors,floor)

    def get_next_states(self) -> list:
        states = []
        items_on_floor = self.elevator_items
        lowest_floor = not bool([item for floor in range(1,self.elevator) for item in self.items_on_floor(floor)])

        iters = list(itertools.combinations(items_on_floor,2)) + [[item] for item in items_on_floor]
        for subset in iters:
            for dir in (1,) if lowest_floor else (-1,1):
                if 1 <= self.elevator + dir <= self.floors:
                    new_state = self.set_elevator_floor(self.elevator + dir)
                    for item in subset:
                        new_state.move_item(item,new_state.elevator)
                    if not new_state.is_fail_state():
                        states.append(new_state)
        return states

    def h(self,_) -> int:
        return round(sum([self.floors - item.floor for item in self.items]) / 2)

    def move_item(self,item:Compatible,floor:int):
        self.items[self.items.index(item)] = item.move_floor(floor)

    @profile
    def steps_to_finish(self):
        target = self.set_elevator_floor(self.floors)
        for item in target.items:
            target.move_item(item,target.floors)
        d = Dijkstra(self,target,adjacency_function=Building.get_next_states,heuristic_function=Building.h,verbose=False)
        # d = Dijkstra(self,target,Building.get_next_states,Building.is_valid_state,Building.h)
        d.search()
        return d.dist

    def items_on_floor(self,floor):
        return [item for item in self.items if item.floor == floor]

    @property
    def elevator_items(self) -> list:
        return self.items_on_floor(self.elevator)

    # def get_items_on_floor(self,floor:int) -> list:
    #     return [item for item in self.items if item.floor == floor]


with open(input) as f:
    items = []
    i = 1
    for line in f:
        items += Compatible.create_list_from_string(line,i)
        i += 1
    b = Building(items,i-1,new=True)
    print(f'Move completed in {b.steps_to_finish()} rides on the elevator')


    # print(b)
    # print(b.is_fail_state(),'\n\n\n')

    # for new_b in b.get_next_states():
    #     print(new_b,'\n')


