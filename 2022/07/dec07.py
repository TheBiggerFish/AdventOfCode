import math
from functools import cached_property
from typing import Optional

from fishpy.structures import Node, Range


class File(Node):
    def __init__(self, size: int = 0, name: str = '', dir: bool = False,
                 children: Optional[list['File']] = None,
                 parent: Optional['File'] = None, root: bool = False):
        super().__init__(value=size, name=name, children=children, parent=parent)
        self._dir = dir
        self._root = root
        self.children: list[File]
        self.parent: Optional[File]

    @cached_property
    def size(self) -> int:
        if not self.dir:
            return self.value
        return sum([file.size for file in self.children])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(dir={self.dir},path={self.full_path()},size={self.size})'

    def full_path(self) -> str:
        cur = self
        path = []
        while not cur.root:
            path.append(cur.name)
            cur = cur.parent
        return '/' + '/'.join(path[::-1])

    @property
    def dir(self) -> bool:
        return self._dir

    @property
    def root(self) -> bool:
        return self._root

    def cd(self, location: str) -> 'File':
        if location == '..':
            if self.parent is None:
                raise Exception(f'{self.name} has no parent directory to'
                                'cd into')
            return self.parent
        for child in self.children:
            if child.name == location:
                if child.dir:
                    return child
                raise NotADirectoryError('Operation only works on directories')
        raise ValueError(f'Directory {location} not known')

    def find(self, name: Optional[str] = None, size: Optional[Range] = None) -> list['File']:
        results = []
        for child in self.children:
            results += child.find(name, size)
        if name is None or name in self.name:
            if size is None or self.size in size:
                results.append(self)
        return results


class FileSystem:
    def __init__(self):
        self.root = self.wd = File(name='', dir=True, root=True)
        self.root.parent = self.root

    def cd(self, location: str):
        if location == '/':
            self.wd = self.root
        else:
            self.wd = self.wd.cd(location)

    def mkdir(self, name: str):
        if not self.wd.dir:
            raise NotADirectoryError('Operation only works on directories')
        self.wd.add_child(File(name=name, dir=True, parent=self.wd))

    def touch(self, name: str, size: int):
        if not self.wd.dir:
            raise NotADirectoryError('Operation only works on directories')
        self.wd.add_child(File(size=size, name=name, parent=self.wd))

    def pwd(self) -> str:
        return self.wd.full_path()

    def size(self, location: str = '.') -> int:
        if location == '.':
            return self.wd.size
        if location == '..':
            return self.wd.parent.size
        if location == '/':
            return self.root.size
        raise NotImplementedError('Cannot view size of child directory')

    def find(self, name: Optional[str] = None, size: Optional[Range] = None) -> list[File]:
        return self.wd.find(name, size)


def main():
    with open('2022/07/input.txt') as f:
        commands = list(map(str.splitlines, f.read().split('$')))

    fs = FileSystem()
    for command in commands[2:]:
        cmd = command[0].strip().split()
        results: list[str] = list(map(str.split, command[1:]))
        if cmd[0] == 'ls':
            for result in results:
                if result[0] == 'dir':
                    fs.mkdir(result[1])
                else:
                    fs.touch(result[1], int(result[0]))
        elif cmd[0] == 'cd':
            fs.cd(cmd[1])
    fs.cd('/')

    files = fs.find(size=Range(fs.root.size - 40000000, math.inf))
    files = sorted(files, key=lambda f: f.size)
    print(files)


if __name__ == '__main__':
    main()
