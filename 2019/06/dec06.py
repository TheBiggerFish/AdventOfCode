# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/6

from fishpy.pathfinding import Dijkstra

input = '2019/06/input.txt'

class Planet:
    def __init__(self,name):
        self.name = name
        self.satellites = set()
        self.parent = None
        self._parent_orbits = -1
    
    def add_satellite(self,sat):
        self.satellites.add(sat)

    def __eq__(self,other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def count_of_parent_orbits(self):
        if self._parent_orbits != -1:
            return self._parent_orbits
        if self.parent is None:
            return 0
        self._parent_orbits = self.parent.count_of_parent_orbits() + 1
        return self._parent_orbits

    def adjacent(self): 
        return {self.parent} | self.satellites if self.parent is not None else self.satellites 

    def orbits(self,other):
        return self in other.satellites

    def __str__(self):
        return self.name + (': ' + ','.join([sat.name for sat in self.satellites]) if self.satellites else '')


with open(input) as f:
    planets = {}
    for line in f:
        spl = line.strip().split(')')
        host,sat_name = spl[0],spl[1]
        if host not in planets:
            planets[host] = Planet(host)
        if sat_name not in planets:
            planets[sat_name] = Planet(sat_name)
        planets[sat_name].parent = planets[host]
        planets[host].add_satellite(planets[sat_name])

print(sum([planets[p].count_of_parent_orbits() for p in planets]))

d = Dijkstra(planets['YOU'],planets['SAN'], adjacency_function=Planet.adjacent)
print(d.search()-2)