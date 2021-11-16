# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/13


from fishpy.modulo import chinese_remainder_theorem

with open('2020/13/input.txt','r') as input_file:
    departure_time = int(input_file.readline().strip())
    all_buses = input_file.readline().strip().split(',')
    running_buses,indices = [],[]
    for i, bus in enumerate(all_buses,start=0):
        if bus != 'x':
            running_buses.append(int(bus))
            indices.append((-i)%int(bus))

time = departure_time
while True:
    done = False
    for bus in running_buses:
        if time % bus == 0:
            done = True
            break
    if done:
        break
    time += 1

print('Result 1:',(time-departure_time)*bus)
print('Result 2:',chinese_remainder_theorem(a=indices,m=running_buses))
