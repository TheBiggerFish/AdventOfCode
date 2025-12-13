from dataclasses import dataclass
from functools import cached_property
from typing import NewType

from fishpy.geometry import LatticePoint

Shape = NewType('shape', list[str])

PRESENTS_COUNT = 6

@dataclass
class Present:
    id: int
    shape: Shape

    @staticmethod
    def load_from_string(string: str) -> 'Present':
        id_line, *shape_lines = string.splitlines()
        id = int(id_line[0].strip(':'))
        return Present(id=id, shape=shape_lines)

    @staticmethod
    def mirror_y(shape: str) -> Shape:
        return [line[::-1] for line in shape]

    @staticmethod
    def mirror_x(shape: str) -> Shape:
        return shape[::-1]

    @staticmethod
    def rotate_cw(shape: Shape) -> Shape:
        return [''.join(row) for row in zip(*shape[::-1])]

    @staticmethod
    def rotate_ccw(shape: Shape) -> Shape:
        return [''.join(row) for row in zip(*shape)][::-1]

    @cached_property
    def area(self) -> int:
        return sum(line.count('#') for line in self.shape)

    @cached_property
    def family(self) -> list[Shape]:
        family = [
            self.shape,
            Present.mirror_x(self.shape),
            Present.mirror_y(self.shape),
        ]
        extended_family = []
        for shape in family:
            extended_family.append(shape)
            extended_family.append(Present.rotate_cw(shape))
            extended_family.append(Present.rotate_cw(Present.rotate_cw(shape)))
            extended_family.append(Present.rotate_ccw(shape))
        unique_family = []
        for shape in extended_family:
            if shape not in unique_family:
                unique_family.append(shape)
        return unique_family

aabbs_fit, insufficient_area, undetermined = 0, 0, 0
@dataclass
class Region:
    dimensions: LatticePoint
    present_counts: list[int]

    @staticmethod
    def load_from_string(string: str) -> 'Region':
        dim_string, counts_string = string.split(': ')
        dimensions = LatticePoint(*map(int, dim_string.split('x')))
        present_counts = list(map(int, counts_string.split()))
        return Region(dimensions=dimensions, present_counts=present_counts)

    def has_insufficient_area_for(self, presents: list[Present]) -> bool:
        required_area = sum(present.area * count for present, count in zip(presents, self.present_counts))
        return required_area > self.dimensions.volume()

    def can_fit_without_overlap(self, count: int) -> bool:
        aabb_size = LatticePoint(3, 3)
        aabbs = (self.dimensions // aabb_size).volume()
        return aabbs.volume() >= count

    def can_fit_presents(self, presents: list[Present]) -> bool:
        global aabbs_fit, insufficient_area, undetermined
        if self.can_fit_without_overlap(sum(self.present_counts)):
            aabbs_fit += 1
            return True
        if self.has_insufficient_area_for(presents):
            insufficient_area += 1
            return False
        undetermined += 1

with open('input.txt') as f:
    *present_strings, regions_string = f.read().split('\n\n')

presents = list(map(Present.load_from_string, present_strings))
regions = list(map(Region.load_from_string, regions_string.splitlines()))

list(map(Region.can_fit_presents, regions, [presents]*len(regions)))
print(f'AABBs fit: {aabbs_fit}')
print(f'Insufficient area: {insufficient_area}')
print(f'Undetermined: {undetermined}')
