# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/5


from fishpy.structures import Range

def get_id(string,low_char,high_char):
    r = Range(0,2**len(string))
    for char in string:
        if char == low_char:
            r = r.division(2,0)
        if char == high_char:
            r = r.division(2,1)
    return r.lower

def get_seat_id(string):
    row_str = string[:7]
    row = get_id(row_str,'F','B')

    col_str = string[7:]
    col = get_id(col_str,'L','R')
    
    return row * 8 + col

with open('2020/05/input.txt') as f:
    highest = 0
    found = set()
    for line in f:
        id = get_seat_id(line.strip())
        found.add(id)
        if id > highest:
            highest = id


    your_seat = 0
    seats = sorted(found)
    for i in range(0,len(seats)-1):
        if seats[i]+1 != seats[i+1]:
            your_seat = seats[i]+1
            break

    print(f'The highest seat ID is {highest}')
    print(f'The ID of your seat is {your_seat}')