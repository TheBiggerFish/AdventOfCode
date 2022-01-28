# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/16


from typing import List
from math import prod


def binary(integer):
    return bin(integer)[2:]

class Packet:
    def __init__(self,version:int,type:int):
        self.version = version
        self.type = type

    def __len__(self) -> int:
        return len(self.bin())

    @staticmethod
    def is_value_packet(version:int) -> bool:
        return version == 4
    
    def bin(self) -> str:
        return binary(self.version).rjust(3,'0') + binary(self.type).rjust(3,'0')

    def version_sum(self) -> int:
        return self.version

    def evaluate(self) -> int:
        raise NotImplementedError('Evaluate is not implemented for Packet class')

    @staticmethod
    def from_bin(binary_string:str) -> 'Packet':
        version = int(binary_string[:3],2)
        type = int(binary_string[3:6],2)
        if Packet.is_value_packet(type):
            value = 0
            for i in range(6,len(binary_string),5):
                value *= 16
                value += int(binary_string[i+1:i+5],2)
                if binary_string[i] == '0':
                    break
            return ValuePacket(version,type,value)
        else:
            subpackets = []
            length_type = binary_string[6] == '1'
            if length_type:
                next_index = 18
                length = int(binary_string[7:next_index],2)
                while len(subpackets) < length:
                    subpackets.append(Packet.from_bin(binary_string[next_index:]))
                    next_index += len(subpackets[-1])
            else:
                next_index = 22
                length = int(binary_string[7:next_index],2)
                while sum([len(subpacket) for subpacket in subpackets]) < length:
                    subpackets.append(Packet.from_bin(binary_string[next_index:]))
                    next_index += len(subpackets[-1])
            return OperatorPacket(version,type,length_type,length,subpackets)

class ValuePacket(Packet):
    def __init__(self,version:int,type:int,value:int):
        super().__init__(version,type)
        self.value = value

    def bin(self) -> str:
        body = super().bin()
        value_bin = binary(self.value)
        value_bin = value_bin.rjust(len(value_bin)+(4-len(value_bin))%4,'0')
        for i,_ in enumerate(value_bin):
            if i%4 == 0:
                body += '1' if len(value_bin) - i > 4 else '0'
            body += value_bin[i]
        return body

    def evaluate(self) -> int:
        return self.value

class OperatorPacket(Packet):
    def __init__(self,version:int,type:int,length_type:bool,length:int,subpackets:List[Packet]):
        super().__init__(version,type)
        self.length_type = length_type
        self.length = length
        self.subpackets = subpackets

    def version_sum(self) -> int:
        return self.version + sum([subpacket.version_sum() for subpacket in self.subpackets])

    def bin(self) -> str:
        body = super().bin()
        if self.length_type:
            body += '1' + binary(self.length).rjust(11,'0')
        else:
            body += '0' + binary(self.length).rjust(15,'0')
        for sub in self.subpackets:
            body += sub.bin()
        return body

    def evaluate(self) -> int:
        children = [subpacket.evaluate() for subpacket in self.subpackets]
        match self.type:
            case 0: return sum(children)
            case 1: return prod(children)
            case 2: return min(children)
            case 3: return max(children)
            case 4: raise ValueError('OperatorPacket cannot have type value of 4')
            case 5: return int(children[0] > children[1])
            case 6: return int(children[0] < children[1])
            case 7: return int(children[0] == children[1])

with open('2021/16/input.txt') as f:
    string = binary(int(f.readline(),16))
    packet:OperatorPacket = Packet.from_bin(string)
    
    print(packet.version_sum())
    print(packet.evaluate())
