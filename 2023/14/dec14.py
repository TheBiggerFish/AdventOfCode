from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid

NORTH = LatticePoint(0,-1)
WEST = LatticePoint(-1,0)
SOUTH = LatticePoint(0,1)
EAST = LatticePoint(1,0)
ORDERED_DIRECTIONS = [NORTH, WEST, SOUTH, EAST]

class Platform(Grid):
    def move(self, rock: LatticePoint, dir:LatticePoint) -> tuple[bool, LatticePoint]:
        """Move a single rock in a given direction as far as it can go"""
        if self[rock].rep != 'O':
            return False, rock
        moved = rock + dir
        if moved not in self or self[moved].rep != '.':
            return False, rock
        self[moved].rep = 'O'
        self[rock].rep = '.'
        return True, moved
    
    def tilt(self, direction: LatticePoint) -> list[LatticePoint]:
        """Roll all rocks in a given direction as far as they can go"""
        
        # Sort rocks for northmost rocks to move first
        rocks = self.char_positions('O')['O']
        if direction == NORTH:
            rocks = sorted(rocks, key=lambda rock: rock.y)
        elif direction == WEST:
            rocks = sorted(rocks, key=lambda rock: rock.x)
        elif direction == SOUTH:
            rocks = sorted(rocks, key=lambda rock: rock.y, reverse=True)
        elif direction == EAST:
            rocks = sorted(rocks, key=lambda rock: rock.x, reverse=True)

        for i, rock in enumerate(rocks):
            moved = True
            while moved:
                moved, rock = self.move(rock, direction)
            rocks[i] = rock
        return rocks

    @property
    def load(self):
        """Determine the overall load for all rocks on the platform"""
        total = 0
        for rock in self.char_positions('O')['O']:
            total += self.height - rock.y
        return total


def extend_loop(loop: list[int], index: int, target: int) -> int:
    """Determine the loop and extend it to a given index"""
    for loop_size in range(1, len(loop)):
        if loop[-1] == loop[-loop_size - 1]:
            break
    offset_index = index % loop_size
    
    # Cut out a single iteration of the loop appropriately aligning the index to modulo loop_size
    # E.g. if loop_size = 5, [3,4,0,1,2,3,4,0,1,2] -> [0,1,2,3,4]
    loop = loop[-offset_index-1:] + loop[-loop_size:-offset_index-1]
    
    # Determine where in the loop the target would fall
    target_index = target % loop_size
    return loop[target_index]


def main():
    with open('2023/14/input.txt') as f:
        lines = f.read().splitlines()
    platform = Platform.from_list_of_strings(lines)
    
    seen: set[int] = set()
    loop: list[int] = []
    once = True
    load = 0
    # Cycle until we start seeing the same load size in a loop
    for i in range(10**9):
        if load in seen:
            loop.append(load)
            print(f'Load at index {i}: {load}')
            if len(loop) == 50:
                break
        seen.add(load)
        for dir in ORDERED_DIRECTIONS:
            platform.tilt(dir)
            load = platform.load
            if once:
                print(f'Load after one tilt: {load}')
                once = False

    target = extend_loop(loop, i, 10**9)
    print(f'Load after 1,000,000,000 cycles: {target}')

if __name__ == '__main__':
    main()
