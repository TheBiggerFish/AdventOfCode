from dataclasses import dataclass
from functools import lru_cache

from fishpy.geometry import Point3D
from fishpy.pathfinding.grid import Grid3D

bricks: dict[int, 'Brick'] = {}
supporter_map: dict[int, set[int]] ={}

@dataclass
class Brick:
    """Represents a cuboid in the 3D grid"""
    id: int
    low: Point3D
    high: Point3D

    def supporters(self, grid: Grid3D) -> set[int]:
        """Use the 3D grid to determine what supporters are directly underneath self"""
        if self.low.z == 1:
            return set()
        supporters: set[int] = set()
        for x in range(self.low.x, self.high.x+1):
            for y in range(self.low.y, self.high.y+1):
                pt = Point3D(x, y, self.low.z-1)
                down = grid[pt].rep
                if isinstance(down, int):
                    supporters.add(down)
        return supporters

    def drop(self, grid: Grid3D):
        """Reduce the z value of self by 1 and update the grid to reflect"""
        self.low.z -= 1
        self.high.z -= 1
        for x in range(self.low.x, self.high.x+1):
            for y in range(self.low.y, self.high.y+1):
                grid[Point3D(x, y, self.low.z)].rep = self.id
                grid[Point3D(x, y, self.high.z+1)].rep = '.'

@lru_cache
def would_fall(brick: int, disintegrated: int) -> bool:
    """Determine if 'brick' would fall if 'disintegrated' was removed"""
    # If the brick has no supporters, it's probably resting on the ground and would not fall
    if len(supporter_map[brick]) == 0:
        return False
    # If the disintegrated brick is higher, then it couldn't cause the brick to fall
    if bricks[disintegrated].high.z > bricks[brick].low.z:
        return False

    for supporter in supporter_map[brick]:
        if supporter != disintegrated and not would_fall(supporter, disintegrated):
            return False
    return True

def fall_count(brick: int) -> int:
    """Determine how many other bricks would fall if 'brick' was disintegrated"""
    count = 0
    for other in supporter_map.keys():
        if other == brick:
            continue
        if would_fall(other, brick):
            count += 1
    return count
    

def main():
    global supporter_map
    global bricks
    
    # Read input
    with open('2023/22/input.txt') as f:
        lines = f.read().splitlines()
    
    # Parse input
    bricks = {}
    highest = Point3D(0,0,0)
    for i, line in enumerate(lines):
        low, high = line.split('~')
        low = Point3D(*map(int,low.split(',')))
        high = Point3D(*map(int,high.split(',')))
        highest = Point3D(max(highest.x, high.x+1), 
                          max(highest.y, high.y+1),
                          max(highest.z, high.z+1))
        bricks[i] = Brick(i, low, high)

    # Create and populate 3D grid with brick ids
    grid = Grid3D.blank(highest)
    for brick in bricks.values():
        for x in range(brick.low.x, brick.high.x+1):
            for y in range(brick.low.y, brick.high.y+1):
                for z in range(brick.low.z, brick.high.z+1):
                    grid[Point3D(x,y,z)].rep = brick.id

    # Bring all bricks to rest at lowest z value possible
    for brick in sorted(bricks.values(), key=lambda b: b.low.z):
        while brick.low.z != 1 and not brick.supporters(grid):
            brick.drop(grid)
    
    # Map each brick ID to a set of brick IDs that are supporting it
    supporter_map = {brick.id: brick.supporters(grid) for brick in bricks.values()}

    # Create a set of all brick ids and remove bricks which are the only supporter for upper bricks
    # This leaves bricks which can be safely deleted
    disintegratable = {brick.id for brick in bricks.values()}
    for _, supporters in supporter_map.items():
        if len(supporters) == 1:
            supporter = list(supporters)[0]
            if supporter in disintegratable:
                disintegratable.remove(supporter)
    print(f'There are {len(disintegratable)} bricks which can be safely disintegrated')
    
    # Find the total number of bricks that would fall if a brick was removed
    count = 0
    for brick in bricks.keys():
        count += fall_count(brick)
    print(f'The sum of the number of other bricks that would fall is {count}')
            

if __name__ == '__main__':
    main()
