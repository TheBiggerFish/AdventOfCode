# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/4


class Room:
    def __init__(self,code):
        parts = code.strip(']').split('[')
        self.checksum = parts[1]
        self.id = int(parts[0].split('-')[-1])
        self.name = parts[0].split('-')[:-1]
    
    def __str__(self):
        return f'{"-".join(self.name)}-{self.id}[{self.checksum}]'

    @property
    def cat_name(self):
        return ''.join(self.name)

    @property
    def real_name(self):
        real = ''
        for part in self.name:
            for char in part:
                real += chr((((ord(char)-97) + self.id) % 26) + 97)
            real += '-'
        return real.strip('-')

    def gen_checksum(self):
        freq = {}
        name = ''.join(self.name)
        for char in name:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        sort = {k: v for k, v in sorted(freq.items(), key=lambda item: (0-item[1],item[0]))}
        return ''.join(list(sort.keys())[:5])

with open('2016/04/input.txt') as in_file:
    sum_ = 0
    room = 0
    for line in in_file:
        r = Room(line.strip())
        if r.checksum == r.gen_checksum():
            sum_ += r.id
            if r.real_name == 'northpole-object-storage':
                room = r.id
    print(f'The sum of the sector IDs of the real rooms is {sum_}')
    print(f'The sector ID of the room where North Pole objects are stored is {room}')