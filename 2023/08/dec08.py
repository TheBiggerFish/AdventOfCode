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
        left, right = children.strip('()').split(', ')

        nodes.setdefault(node, Node(node))
        nodes.setdefault(left, Node(left))
        nodes.setdefault(right, Node(right))

        nodes[node].add_child(nodes[left])
        nodes[node].add_child(nodes[right])

    steps = follow_directions('AAA', {'ZZZ'}, nodes, directions)
    print(f'Number of steps taken: {steps}')

    starts = list(filter(lambda node: node[-1] == 'A', nodes.keys()))
    ends = list(filter(lambda node: node[-1] == 'Z', nodes.keys()))
    ghost_steps = follow_directions_ghosts(starts, ends, nodes, directions)
    print(f'Number of ghost steps taken: {ghost_steps}')


if __name__ == '__main__':
    main()
