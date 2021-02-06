# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/9


import networkx as nx
from itertools import permutations

def get_length(G,path):
    return sum([G.edges[path[i],path[i+1]]['weight'] for i in range(len(path)-1)])
        
G = nx.Graph()
with open('2015/09/input.txt') as f:
    for line in f:
        line = line.strip().split(' ')
        G.add_nodes_from((line[0],line[2]))
        G.add_edge(line[0],line[2], weight=int(line[-1]))
min_ = min([get_length(G,perm) for perm in permutations(G.nodes)])
max_ = max([get_length(G,perm) for perm in permutations(G.nodes)])
print('The shortest path is {} and the longest path is {}'.format(min_,max_))