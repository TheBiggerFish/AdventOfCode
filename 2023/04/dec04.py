from dataclasses import dataclass
from functools import cached_property, lru_cache


@dataclass
class Card:
    id: int
    winning: set[int]
    numbers: set[int]

    @cached_property
    def overlap(self) -> int:
        return len(self.winning.intersection(self.numbers))

    @cached_property
    def points(self) -> int:
        if self.overlap > 0:
            return 2**(self.overlap-1)
        return 0


@lru_cache
def part_two(index: int) -> int:
    card = cards[index-1]
    count = 1
    for next_index in range(index + 1, index + card.overlap + 1):
        count += part_two(next_index)
    return count


if __name__ == '__main__':
    with open('2023/04/input.txt') as f:
        lines = f.read().splitlines()

    total_points = 0
    cards: list[Card] = []
    for line in lines:
        id_str, numbers_str = line.split(':')
        winning_str, numbers_str = numbers_str.split('|')

        id = int(id_str.split()[-1])
        winning = set(map(int, winning_str.split()))
        numbers = set(map(int, numbers_str.split()))
        card = Card(id, winning, numbers)
        cards.append(card)
        total_points += card.points
    print(total_points)

    total_cards = 0
    for card in cards:
        total_cards += part_two(card.id)
    print(total_cards)
