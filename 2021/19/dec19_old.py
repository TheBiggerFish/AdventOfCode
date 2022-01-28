# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/18

from itertools import permutations
from functools import cached_property
from os import stat
from typing import Optional
from fishpy.geometry import Point3D

class Beacon(Point3D):
    @staticmethod
    def from_string(string:str) -> 'Beacon':
        coords = (int(c) for c in string.split(','))
        return Beacon(*coords)

    def __mul__(self,other:'Beacon'):
        return Beacon(self.x*other.x,self.y*other.y,self.z*other.z)

    def __repr__(self):
        return f'Beacon{str(self)}'

    @cached_property
    def permutations(self) -> list['Beacon']:
        return [
            Beacon(self.x,self.y,self.z),Beacon(self.x,-self.y,-self.z),
            Beacon(-self.x,self.y,-self.z),Beacon(-self.x,-self.y,self.z),
            Beacon(self.x,self.z,-self.y),Beacon(self.x,-self.z,self.y),
            Beacon(-self.x,self.z,self.y),Beacon(-self.x,-self.z,-self.y),

            Beacon(self.y,self.z,self.x),Beacon(self.y,-self.z,-self.x),
            Beacon(-self.y,self.z,-self.x),Beacon(-self.y,-self.z,self.x),
            Beacon(self.y,self.x,-self.z),Beacon(self.y,-self.x,self.z),
            Beacon(-self.y,self.x,self.z),Beacon(-self.y,-self.x,-self.z),

            Beacon(self.z,self.x,self.y),Beacon(self.z,-self.x,-self.y),
            Beacon(-self.z,self.x,-self.y),Beacon(-self.z,-self.x,self.y),
            Beacon(self.z,self.y,-self.x),Beacon(self.z,-self.y,self.x),
            Beacon(-self.z,self.y,self.x),Beacon(-self.z,-self.y,-self.x),
        ]

class Scanner:
    def __init__(self,known_beacons:set[Beacon]):
        self.beacons = known_beacons
        self.position = Beacon(0,0,0)

    @staticmethod
    def from_list_of_strings(beacons:list[str]) -> 'Scanner':
        known_beacons = {Beacon.from_string(beacon) for beacon in beacons}
        return Scanner(known_beacons)

    def add_list_of_beacon(self,offset:Point3D,beacons:set[Beacon]):
        for beacon in beacons:
            self.beacons.add(beacon + offset)

    def orientations(self):
        pass

    def overlapping(self,other:'Scanner') -> Optional[Point3D]:
        
        most:dict[int,tuple[int,Optional[Beacon]]] = {}
        diff:dict[int,dict[Beacon,list[tuple(int,int)]]] = {}
        beacons_s,beacons_o = list(self.beacons),list(other.beacons)
        # for s,beacon_s in enumerate(self.beacons):
        for s,beacon_s in enumerate(beacons_s):
            for permutation in range(24):
                for o,beacon_o in enumerate(beacons_o):
                # for o,beacon_o in enumerate(other.beacons):
                    # offset:Beacon = beacon_s - beacon_o.permutations[permutation]
                    offset:Beacon = beacon_s.permutations[permutation] - beacon_o
                    diff.setdefault(permutation,{})
                    diff[permutation].setdefault(offset,[])
                    diff[permutation][offset].append((s,o))
                most_common_offset = max(diff[permutation].keys(),key=lambda item:len(diff[permutation][item]))
                count = len(diff[permutation][most_common_offset])
                if count >= 12:
                    most[permutation] = (count,most_common_offset)
        print(most)
        print(diff.keys())
        for permutation in diff:
            # for offset in diff[permutation]:
            if Beacon(68,-1246,-43) in diff[permutation]:
                print(diff[permutation][Beacon(68,-1246,-43)])
            # print(diff[permutation])
                # for pair in diff[permutation][offset]:
                #     s = beacons_s[pair[0]].permutations[permutation]
                #     o = beacons_o[pair[1]]
                #     print(s,o,offset,s-o)
        return most

with open('2021/19/input.txt') as f:
    scanners = {int(group.split()[2]):Scanner.from_list_of_strings(group.split('\n')[1:]) for group in f.read().rstrip().split('\n\n')}
    # print(scanners)
    print(scanners[0].overlapping(scanners[1]))