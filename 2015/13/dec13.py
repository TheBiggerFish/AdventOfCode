# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/13


import networkx as nx
from itertools import permutations

def get_length(G,path):
    return sum([G.edges[path[i],path[(i+1)%len(path)]]['weight'] + G.edges[path[(i+1)%len(path)],path[i]]['weight'] for i in range(len(path))])

G = nx.DiGraph()
with open('2015/13/input2.txt') as f:
    for line in f:
        line = line.strip().strip('.').split(' ')
        G.add_nodes_from((line[0],line[10]))
        G.add_edge(line[0],line[10], weight=int(line[3])*(-1 if line[2] == 'lose' else 1))

min_ = min([get_length(G,perm) for perm in permutations(G.nodes)])
max_ = max([get_length(G,perm) for perm in permutations(G.nodes)])

# optimal_happiness = optimize(G)
print('The optimal happiness of the group is {}'.format(max_))