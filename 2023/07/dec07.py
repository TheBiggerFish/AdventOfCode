from dataclasses import dataclass
from enum import Enum
from functools import cached_property


class HandClass(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


@dataclass
class Hand:
    CARD_VALUE = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8,
        '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, '1': 1,
    }

    cards: str
    bid: int

    @cached_property
    def occurances(self) -> dict[str, int]:
        return {card: self.cards.count(card) for card in set(self.cards)}

    @cached_property
    def hand_class(self) -> HandClass:
        if self.is_five_of_a_kind():
            return HandClass.FIVE_OF_A_KIND
        if self.is_four_of_a_kind():
            return HandClass.FOUR_OF_A_KIND
        if self.is_full_house():
            return HandClass.FULL_HOUSE
        if self.is_three_of_a_kind():
            return HandClass.THREE_OF_A_KIND
        if self.is_two_pair():
            return HandClass.TWO_PAIR
        if self.is_one_pair():
            return HandClass.ONE_PAIR
        return HandClass.HIGH_CARD

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(cards={self.cards}, bid={self.bid})'

    def winnings(self, rank: int) -> int:
        return self.bid * rank

    def is_five_of_a_kind(self) -> bool:
        return self.occurances[self.cards[0]] == 5

    def is_four_of_a_kind(self) -> bool:
        for card in set(self.cards):
            if self.occurances[card] == 4:
                return True
        return False

    def is_full_house(self) -> bool:
        seenTwo = seenThree = False
        for card in set(self.cards):
            if self.occurances[card] == 2:
                if seenTwo == False:
                    seenTwo = True
            if self.occurances[card] == 3:
                if seenThree == False:
                    seenThree = True
        return seenTwo and seenThree

    def is_three_of_a_kind(self) -> bool:
        for card in set(self.cards):
            if self.occurances[card] == 3:
                return True
        return False

    def is_two_pair(self) -> bool:
        seen = False
        for card in set(self.cards):
            if self.occurances[card] == 2:
                if seen == False:
                    seen = True
                else:
                    return True
        return False

    def is_one_pair(self) -> bool:
        for card in set(self.cards):
            if self.occurances[card] == 2:
                return True
        return False

    def wins_tiebreak(self, other: 'Hand') -> bool:
        for i, card in enumerate(self.cards):
            diff = Hand.CARD_VALUE[card] - Hand.CARD_VALUE[other.cards[i]]
            if diff != 0:
                return diff > 0
        raise Exception('Identical hands?')

    def __lt__(self, other: 'Hand') -> bool:
        if self.hand_class == other.hand_class:
            return other.wins_tiebreak(self)
        return self.hand_class.value > other.hand_class.value

    def __eq__(self, other: 'Hand') -> bool:
        return self.cards == other.cards


class JokerHand(Hand):
    CARD_VALUE = {
        'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7,
        '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, '1': 1, 'J': 0,
    }

    @cached_property
    def hand_class(self) -> HandClass:
        if 'J' not in self.cards:
            return super().hand_class
        replacement_hands: list[str] = []
        for value in JokerHand.CARD_VALUE.keys():
            if value == 'J':
                continue
            # Best placement always comes from changing all Jokers to the same face value card
            replacement_hands.append(self.cards.replace('J', value))

        hands = map(lambda cards: Hand(cards, self.bid), replacement_hands)
        return max(hands).hand_class

    def wins_tiebreak(self, other: 'JokerHand') -> bool:
        for i, card in enumerate(self.cards):
            diff = JokerHand.CARD_VALUE[card] - \
                JokerHand.CARD_VALUE[other.cards[i]]
            if diff != 0:
                return diff > 0
        raise Exception('Identical hands?')


def main():
    with open('2023/07/input.txt') as f:
        lines = f.read().splitlines()
        hands: list[Hand] = []
        hands_joker: list[JokerHand] = []
        for line in lines:
            cards, bid = line.split()
            hands.append(Hand(cards, int(bid)))
            hands_joker.append(JokerHand(cards, int(bid)))

    hands = sorted(hands)
    winnings = sum([hand.winnings(rank)
                    for rank, hand in enumerate(hands, 1)])
    print(winnings)

    hands_joker = sorted(hands_joker)
    winnings_joker = sum([hand.winnings(rank)
                         for rank, hand in enumerate(hands_joker, 1)])
    print(winnings_joker)


if __name__ == '__main__':
    main()
