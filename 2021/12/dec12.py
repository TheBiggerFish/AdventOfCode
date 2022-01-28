# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/12


from typing import Set
from networkx import Graph

def path_count(current:str,target:str,seen:Set[str],graph:Graph,doubled_used:bool) -> int:
    """Count the paths through the cave system"""

    if current == target:
        return 1

    seen = seen if current.isupper() else seen | {current}

    count = 0
    for neighbor in graph[current]:
        if neighbor in seen and not doubled_used and neighbor != 'start':
            count += path_count(neighbor,target,seen,graph,True)
        elif neighbor not in seen:
            count += path_count(neighbor,target,seen,graph,doubled_used)
    return count

graph = Graph()
with open('2021/12/input.txt') as f:
    lines = f.read().strip().split()
    edges = [line.strip().split('-') for line in lines]
    graph.add_edges_from(edges)
    
print('Solution 1:',path_count('start','end',{'start'},graph,doubled_used=True))
print('Solution 2:',path_count('start','end',{'start'},graph,doubled_used=False))
