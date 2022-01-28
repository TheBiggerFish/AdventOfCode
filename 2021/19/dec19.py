# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/18


from typing import Optional
from fishpy.geometry import Point3D

class Beacon(Point3D):
    @staticmethod
    def from_string(string:str) -> 'Beacon':
        return Beacon(*(int(c) for c in string.split(',')))

    def __mul__(self,other:'Beacon'):
        return Beacon(self.x*other.x,self.y*other.y,self.z*other.z)

    def __repr__(self):
        return f'Beacon{str(self)}'

    def orientations(self,orientation:int) -> 'Beacon':
        match orientation:
            case 0: return Beacon(self.x,self.y,self.z)
            case 1: return Beacon(self.x,-self.y,-self.z)
            case 2: return Beacon(-self.x,self.y,-self.z)
            case 3: return Beacon(-self.x,-self.y,self.z)
            case 4: return Beacon(self.x,self.z,-self.y)
            case 5: return Beacon(self.x,-self.z,self.y)
            case 6: return Beacon(-self.x,self.z,self.y)
            case 7: return Beacon(-self.x,-self.z,-self.y)

            case 8: return Beacon(self.y,self.z,self.x)
            case 9: return Beacon(self.y,-self.z,-self.x)
            case 10: return Beacon(-self.y,self.z,-self.x)
            case 11: return Beacon(-self.y,-self.z,self.x)
            case 12: return Beacon(self.y,self.x,-self.z)
            case 13: return Beacon(self.y,-self.x,self.z)
            case 14: return Beacon(-self.y,self.x,self.z)
            case 15: return Beacon(-self.y,-self.x,-self.z)

            case 16: return Beacon(self.z,self.x,self.y)
            case 17: return Beacon(self.z,-self.x,-self.y)
            case 18: return Beacon(-self.z,self.x,-self.y)
            case 19: return Beacon(-self.z,-self.x,self.y)
            case 20: return Beacon(self.z,self.y,-self.x)
            case 21: return Beacon(self.z,-self.y,self.x)
            case 22: return Beacon(-self.z,self.y,self.x)
            case 23: return Beacon(-self.z,-self.y,-self.x)

    def inverse_orientation(self,orientation:int) -> 'Beacon':
        inverses = {0:0, 1:1, 2:2, 3:3, 4:5, 5:4, 6:6, 7:7,
                    8:16, 9:18, 10:19, 11:17, 12:12, 13:14, 14:13, 15:15,
                    16:8, 17:11, 18:9, 19:10, 20:22, 21:21, 22:20, 23:23}
        return self.orientations(inverses[orientation])

class Scanner:
    def __init__(self,id:int,known_beacons:set[Beacon]):
        self.id = id
        self.beacons = known_beacons
        self.neighbors = []
        self.position = Beacon(0,0,0)

    def __repr__(self) -> str:
        return f'Scanner({self.id},{self.beacons})'

    @staticmethod
    def from_list_of_strings(lines:list[str]) -> 'Scanner':
        id = int(lines[0].split()[2])
        known_beacons = {Beacon.from_string(beacon) for beacon in lines[1:]}
        return Scanner(id,known_beacons)

    def overlaps(self,other:'Scanner') -> tuple[Optional[Point3D],int]:
        distances:dict[int,dict[Point3D,int]] = {}
        for p in range(24):
            distances.setdefault(p,{})
            for my_beacon in self.beacons:
                for other_beacon in other.beacons:
                    distance = my_beacon - other_beacon.orientations(p)
                    distances[p].setdefault(distance,0)
                    distances[p][distance] += 1

        for p in range(24):
            maximum = max(distances[p],key=lambda offset:distances[p][offset])
            if distances[p][maximum] >= 12:
                return maximum,p
        return None,-1

    def overtake(self,other:'Scanner',offset:Point3D,orientation:int) -> 'Scanner':
        self.neighbors.append(Beacon(offset.x,offset.y,offset.z))
        for beacon in other.beacons:
            new_beacon = beacon.orientations(orientation) + offset
            self.beacons.add(new_beacon)
        return self

with open('2021/19/input.txt') as f:
    scanners = [Scanner.from_list_of_strings(group.split('\n')) for group in f.read().rstrip().split('\n\n')]

    root = scanners[0]
    del scanners[0]

    while scanners:
        print(len(scanners))
        for i,scanner in enumerate(scanners):
            offset,orientation = root.overlaps(scanner)
            if offset is not None:
                root.overtake(scanner,offset,orientation)
                del scanners[i]
                break

    scanners = [Beacon(0,0,0)] + root.neighbors
    max_distance = 0
    for i in range(len(scanners)-1):
        for j in range(i+1,len(scanners)):
            if (dist := scanners[i].manhattan_distance(scanners[j])) > max_distance:
                max_distance = dist

    print(f'The total number of beacons in the system is',len(root.beacons))
    print(f'The maximal Manhattan distance between any two scanners is',max_distance)
    