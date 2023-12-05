from dataclasses import dataclass

from fishpy.structures import Range


class Mapping:
    def __init__(self, dest_start: int, source_start: int, length: int):
        self.source = Range(source_start, source_start + length)
        self.dest = Range(dest_start, dest_start + length)
        self.offset = dest_start - source_start

    def map(self, input: int, inverse: bool) -> int:
        if inverse and input in self.dest:
            return input - self.offset
        elif not inverse and input in self.source:
            return input + self.offset
        return input


@dataclass
class Map:
    mappings: list[Mapping]

    def map(self, input: int, inverse: bool) -> int:
        for mapping in self.mappings:
            if not inverse and input in mapping.source:
                return mapping.map(input, False)
            elif inverse and input in mapping.dest:
                return mapping.map(input, True)
        return input


class Game:
    def __init__(self, seeds: list[int], maps: list[Map]):
        self.seeds = seeds
        self.maps = maps

        seed_ranges: list[Range] = []
        for i in range(0, len(self.seeds), 2):
            start, length = self.seeds[i:i+2]
            seed_ranges.append(Range(start, start + length))
        self.seed_ranges = seed_ranges

    def is_seed_range_location(self, location: int) -> bool:
        value = location
        for map in reversed(self.maps):
            value = map.map(value, inverse=True)
        for seed_range in self.seed_ranges:
            if value in seed_range:
                return True
        return False

    def location_for_seed(self, seed: int) -> int:
        value = seed
        for map in self.maps:
            value = map.map(value, inverse=False)
        return value

    def optimal_location(self) -> int:
        lowest = 10**10
        for seed in self.seeds:
            location = self.location_for_seed(seed)
            lowest = min(location, lowest)
        return lowest

    def optimal_location_ranges(self) -> int:
        # Start at 20_000_000 for time-saving purposes
        for i in range(20_000_000, 10**10):
            if i % 100000 == 0:
                print("still going", i)
            if self.is_seed_range_location(i):
                return i
        raise Exception("How did I get here?")


def main():
    with open('2023/05/input.txt') as f:
        seeds = list(map(int, f.readline().split(': ')[-1].strip().split()))
        f.readline()
        lines = f.read().splitlines()

    mappings: list[Mapping] = []
    maps: list[Map] = []
    for line in lines:
        if line == '':
            maps.append(Map(mappings))
            mappings = []
        elif not line[0].isdigit():
            # skip map names
            continue
        else:
            mappings.append(Mapping(*map(int, line.split())))
    maps.append(Map(mappings))

    game = Game(seeds, maps)
    p1 = game.optimal_location()
    print(f"Lowest location for discrete numbers: {p1}")
    p2 = game.optimal_location_ranges()
    print(f"Lowest location for range: {p2}")


if __name__ == '__main__':
    main()
