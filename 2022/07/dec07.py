from typing import Optional

from fishpy.structures import Node

available = 40000000


def size(node: Node) -> int:
    if node.value != -1:
        return node.value
    return sum(map(size, node.children))


def collect(node: Node, min_size: int = 0, max_size: Optional[int] = None) -> list[Node]:
    if node.value != -1:
        return []
    collection = []
    for child in node.children:
        collection += collect(child, min_size, max_size)
    if max_size is None or size(node) <= max_size:
        if size(node) >= min_size:
            collection.append(node)
    return collection


with open('2022/07/input.txt') as f:
    commands = list(map(str.splitlines, f.read().split('$')))
    root = Node(-1, '/')
    cur = root
    for command in commands[2:]:
        cmd = command[0].split()
        results: list[str] = list(map(str.split, command[1:]))
        if cmd[0] == 'ls':
            for result in results:
                if result[0] == 'dir':
                    cur.add_child(Node(-1, result[1], parent=cur))
                else:
                    cur.add_child(Node(int(result[0]), result[1], parent=cur))
        elif cmd[0] == 'cd':
            if cmd[1] == '..':
                cur = cur.parent
            else:
                changed = False
                for child in cur.children:
                    if child.name == cmd[1]:
                        cur = child
                        changed = True
                        break
                if not changed:
                    raise Exception(f'Failed to cd to {cmd[1]}')

remove = size(root) - available
print(remove, size(root))
print(sorted(map(lambda n: (size(n), n.name), collect(root, remove))))
