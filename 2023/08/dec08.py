from math import lcm

from fishpy.structures import Node


def follow_directions(start: str, ends: set[str], nodes: dict[str, Node], directions: str) -> int:
    steps = 0
    current = nodes[start]
    while current.value not in ends:
        step = directions[steps % len(directions)]
        if step == 'L':
            current = current.children[0]
        else:
            current = current.children[1]
        steps += 1
    return steps


def follow_directions_ghosts(starts: list[str], ends: set[str], nodes: dict[str, Node], directions: str) -> int:
    distances: list[int] = []
    for start in starts:
        distances.append(follow_directions(start, ends, nodes, directions))
    return lcm(*distances)


def main():
    with open('2023/08/input.txt') as f:
        directions = f.readline().strip()
        f.readline()
        lines = f.read().splitlines()

    nodes: dict[str, Node] = {}
    for line in lines:
        node, children = line.split(' = ')
        children = children.strip('()').split(', ')
        nodes.setdefault(node, Node(node, node))
        nodes.setdefault(children[0], Node(children[0], children[0]))
        nodes.setdefault(children[1], Node(children[1], children[1]))
        nodes[node].add_child(nodes[children[0]])
        nodes[node].add_child(nodes[children[1]])

    print(follow_directions('AAA', {'ZZZ'}, nodes, directions))

    starts = list(filter(lambda node: node[-1] == 'A', nodes.keys()))
    ends = list(filter(lambda node: node[-1] == 'Z', nodes.keys()))
    print(follow_directions_ghosts(starts, ends, nodes, directions))


if __name__ == '__main__':
    main()
