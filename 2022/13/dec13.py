import json
from math import prod
from typing import Union


class Packet:
    def __init__(self, string: str):
        self.packet = json.loads(string)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(packet={self.packet})'

    def __lt__(self, other: 'Packet') -> bool:
        return Packet.compare(self.packet, other.packet)[0]

    @staticmethod
    def compare(left: Union[list, int], right: Union[list, int]) -> tuple[bool, int]:
        if isinstance(left, int) and isinstance(right, int):
            return left <= right, left - right
        if isinstance(left, list) and isinstance(right, list):
            for i, left_i in enumerate(left):
                if i >= len(right):
                    return False, 1
                ordered, difference = Packet.compare(left_i, right[i])
                if difference != 0:
                    return ordered, difference
            if len(left) < len(right):
                return True, -1
            return True, 0
        if isinstance(left, list) and isinstance(right, int):
            return Packet.compare(left, [right])
        if isinstance(left, int) and isinstance(right, list):
            return Packet.compare([left], right)

    @staticmethod
    def decoder_key(packets: list['Packet'], keys: list['Packet']):
        packets += keys
        packets = sorted(packets)
        indexes = map(lambda key: packets.index(key)+1, keys)
        return prod(indexes)


with open('2022/13/input.txt') as f:
    total = 0
    packet_pairs = f.read().split('\n\n')
    for i, pair in enumerate(packet_pairs, 1):
        packet_1, packet_2 = map(Packet, pair.splitlines())
        if packet_1 < packet_2:
            total += i
    print(total)

    packets = [Packet(packet)
               for pair in packet_pairs
               for packet in pair.splitlines()]
    keys = [Packet('[[2]]'), Packet('[[6]]')]
    print(Packet.decoder_key(packets, keys))
