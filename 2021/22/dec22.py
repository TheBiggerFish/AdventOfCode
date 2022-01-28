# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/22


# Didn't do this one, logic largely copied

from typing import Optional
from fishpy.geometry import Point3D
from fishpy.geometry import Cuboid

class ReactorCuboid(Cuboid):
    def __init__(self,lower:Point3D,upper:Point3D,status:bool):
        super().__init__(lower,upper)
        self.status = status

    def __repr__(self):
        status = 'on' if self.status else 'off'
        return f'ReactorCuboid({status},{self.lower}..{self.upper})'

    @property
    def volume(self):
        return self.lower.volume(self.upper+Point3D(1,1,1))

    def overlap(self,other:'ReactorCuboid') -> Optional['ReactorCuboid']:
        low_x,high_x = max(self.lower.x,other.lower.x),min(self.upper.x,other.upper.x)
        low_y,high_y = max(self.lower.y,other.lower.y),min(self.upper.y,other.upper.y)
        low_z,high_z = max(self.lower.z,other.lower.z),min(self.upper.z,other.upper.z)
        low,high = Point3D(low_x,low_y,low_z),Point3D(high_x,high_y,high_z)
        if low_x > high_x or low_y > high_y or low_z > high_z:
            return None
        return ReactorCuboid(low,high,not other.status)


step_1:list[ReactorCuboid] = []
step_2:list[ReactorCuboid] = []
with open('2021/22/input.txt') as f:
    lines = [line.split() for line in f.read().splitlines()]
    for line in lines:
        coords = line[1].split(',')
        min_x,max_x = coords[0].lstrip('x=').split('..')
        min_y,max_y = coords[1].lstrip('y=').split('..')
        min_z,max_z = coords[2].lstrip('z=').split('..')
        rc = ReactorCuboid(Point3D(int(min_x),int(min_y),int(min_z)),
                           Point3D(int(max_x),int(max_y),int(max_z)),
                           True if line[0] == 'on' else False)
        if rc.overlap(ReactorCuboid(Point3D(-50,-50,-50),Point3D(50,50,50),False)):
            step_1.append(rc)
        step_2.append(rc)


cuboids:list[ReactorCuboid] = []
for i,c1 in enumerate(step_2):
    intersections = []
    for j,c2 in enumerate(cuboids):
        if overlap := c1.overlap(c2):
            intersections.append(overlap)
    cuboids += intersections
    if c1.status:
        cuboids.append(c1)
    
count = 0
for cuboid in cuboids:
    if cuboid.status:
        count += cuboid.volume
    else:
        count -= cuboid.volume
print(count)