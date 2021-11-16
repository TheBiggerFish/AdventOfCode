# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/8


from fishpy.structures import Node
from typing import Dict,Tuple,List

input = '2018/08/input.txt'

def recursive_nodes(data,initial_index) -> Tuple[int,Node]:
    count_children = data[initial_index]
    count_metadata = data[initial_index+1]
    length = 2

    children = []
    for _ in range(count_children):
        step,child = recursive_nodes(data,initial_index+length)
        children.append(child)
        length += step

    metadata = data[initial_index+length:initial_index+length+count_metadata]
    length += count_metadata

    header = {'children':count_children,'count_metadata':count_metadata,'metadata':metadata}
    node = Node(value=header,name=str(initial_index),children=children)
    for child in node.children:
        child.parent = node
    return (length,node)


def sum_of_metadata(root:Node) -> int:
    return sum([sum_of_metadata(child) for child in root.children]) + sum(root.value['metadata'])

def sum_of_values(root:Node) -> int:
    if root.value['children']:
        return sum([sum_of_values(root.children[meta-1]) for meta in root.value['metadata'] if 1 <= meta <= root.value['children']])
    return sum(root.value['metadata'])

with open(input) as f:
    data = [int(num) for num in f.read().strip().split()]
    root = recursive_nodes(data,0)[1]
    print(sum_of_metadata(root))
    print(sum_of_values(root))
