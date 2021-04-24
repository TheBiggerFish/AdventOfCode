# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/16


input = '11011110011011101'
length = 272
length2 = 35651584

def bitswap(string):
    new_string = ''
    for char in string:
        new_string += '1' if char == '0' else '0'
    return new_string


def gen_data(string,target_length):
    a = string
    while len(a) < target_length:
        b = bitswap(a[::-1])
        a = a + '0' + b
        pass
    return a[:target_length]

def checksum(string):
    while len(string) % 2 == 0:
        temp = ''
        for i in range(0,len(string),2):
            if string[i] == string[i+1]:
                temp += '1'
            else:
                temp += '0'
        string = temp
    return string


data = gen_data(input,length)
print(f'The first checksum is {checksum(data)}')


data2 = gen_data(input,length2)
print(f'The second checksum is {checksum(data2)}')

