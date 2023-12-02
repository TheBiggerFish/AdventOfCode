import re


class Game:
    def __init__(self, id: int):
        self.id: int = id
        self.cubes: dict[str, int] = {}

    def round(self, cubes: dict[str, int]):
        for color, count in cubes.items():
            self.cubes[color] = max(count, self.cubes.get(color, 0))

    def possible(self, cubes: dict[str, int]) -> bool:
        for color, count in cubes.items():
            if self.cubes.get(color, 0) > count:
                return False
        return True

    def power(self) -> int:
        return self.cubes.get('red', 0) * self.cubes.get('green', 0) * self.cubes.get('blue', 0)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, cubes={self.cubes})'


def main():
    with open('2023/02/input.txt') as f:
        lines = f.read().splitlines()

    games: list[Game] = []
    cube_regex = re.compile(r'\s*(\d+)\s*(\w+)\s*')

    for line in lines:
        id_str, line = line.split(':')

        id = int(id_str.split()[-1])
        game = Game(id)

        for round in line.split(';'):
            # For each round, map the color to the count
            cubes = {match[2]: int(match[1])
                     for match in map(cube_regex.match, round.split(','))}
            game.round(cubes)
        games.append(game)

    required = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    possible = filter(lambda game: game.possible(required), games)
    total_sum = sum([game.id for game in possible])
    print(total_sum)

    total_power = sum([game.power() for game in games])
    print(total_power)


if __name__ == '__main__':
    main()
