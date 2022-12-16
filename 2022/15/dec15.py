import re
from dataclasses import dataclass
from functools import cached_property

from fishpy.geometry import LatticePoint, Line, Point2D
from fishpy.structures import Range
from fishpy.utility import timer

regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): '
                   r'closest beacon is at x=(-?\d+), y=(-?\d+)')


@dataclass
class Sensor:
    position: LatticePoint
    beacon: LatticePoint

    @cached_property
    def radius(self) -> int:
        return self.position.manhattan_distance(self.beacon)

    def distance(self, other: 'Sensor') -> int:
        return self.position.manhattan_distance(other.position)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(position={self.position}, beacon={self.beacon}, radius={self.radius})'

    def gap_line(self, other: 'Sensor') -> Line:
        if self.position.is_above(other.position) and self.position.is_left_of(other.position):
            return Line(self.position.y - self.radius - self.position.x - 1, 1)
        if other.position.is_above(self.position) and other.position.is_left_of(self.position):
            return Line(other.position.y - self.radius - other.position.x - 1, 1)
        if self.position.is_below(other.position) and self.position.is_left_of(other.position):
            return Line(self.position.y + self.radius + self.position.x + 1, -1)
        if other.position.is_below(self.position) and other.position.is_left_of(self.position):
            return Line(other.position.y + self.radius + other.position.x + 1, -1)
        raise Exception('Unknown gap slope')


@dataclass
class Zone:
    sensors: list[Sensor]

    @staticmethod
    def from_strings(strings: list[str]) -> 'Zone':
        sensors = []
        for string in strings:
            match = regex.match(string)
            sensor = LatticePoint(int(match[1]), int(match[2]))
            beacon = LatticePoint(int(match[3]), int(match[4]))
            sensors.append(Sensor(sensor, beacon))
        return Zone(sensors)

    def valid_position(self, pos: LatticePoint) -> bool:
        for sensor in self.sensors:
            dist = pos.manhattan_distance(sensor.position)
            if pos.manhattan_distance(sensor.position) <= sensor.radius:
                return False
        return True

    @timer
    def row_coverage(self, row: int) -> int:

        # Determine ranges which are known to not be beacons
        ranges: set[Range] = set()
        for sensor in self.sensors:
            length = sensor.radius
            dist = abs(row-sensor.position.y)
            if dist > length:
                continue
            start = sensor.position.x - (length - dist)
            end = sensor.position.x + (length - dist)
            if sensor.beacon.y == row:
                if sensor.beacon.x == start:
                    start += 1
                if sensor.beacon.x == end:
                    end -= 1
            if start > end:
                continue
            ranges.add(Range(start, end, True))

        # Combine ranges
        reducing = True
        while reducing:
            reducing = False
            remove = set()
            new_ranges = set()
            for r1 in ranges:
                for r2 in ranges:
                    if r1 == r2 or not r1.overlap(r2):
                        continue
                    new_ranges.add(r1.combine(r2))
                    remove |= {r1, r2}
                    reducing = True
            for removed in remove:
                ranges.remove(removed)
            ranges |= new_ranges

        return sum(map(len, ranges)) + len(ranges)

    def distress_beacon(self) -> LatticePoint:
        lines: list[Line] = []
        for i, sensor_i in enumerate(self.sensors):
            for sensor_j in self.sensors[i+1:]:
                sensor_j: Sensor
                gap = (sensor_i.distance(sensor_j) - 1
                       - sensor_i.radius
                       - sensor_j.radius)

                if gap == 1:
                    line = sensor_i.gap_line(sensor_j)
                    lines.append(line)

        for line in lines:
            for pt in line.lattice_points_along(LatticePoint(0, 0),
                                                LatticePoint(4*10**6, 4*10**6)):
                if self.valid_position(pt):
                    return pt

    @staticmethod
    def tuning_frequency(beacon: LatticePoint) -> int:
        return beacon.x * 4_000_000 + beacon.y


with open('2022/15/input_test.txt') as f:
    lines = f.read().splitlines()
    z = Zone.from_strings(lines)
    print(z.row_coverage(2000000))

    distress_beacon = z.distress_beacon()
    print(z.tuning_frequency(distress_beacon))

    # (2740279, 2625406)
