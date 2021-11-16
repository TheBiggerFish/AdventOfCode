# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/16


from fishpy.structures import Range
import re


target_field_names = 'departure'

def find_column(field,tickets):
    viable = set()
    for i in range(len(your_ticket)):
        found = True
        for ticket in tickets:
            if ticket[i] not in field[0] and ticket[i] not in field[1]:
                found = False
                break
        if found:
            viable.add(i)
    return viable

ranges = {}
column_names = set()
with open('2020/16/input.txt') as input_file:
    for line in input_file:
        if line == '\n':
            break
        results = re.findall(r'([\s\w]+): (\d+-\d+) or (\d+-\d+)',line)
        column_names.add(results[0][0])
        ranges[results[0][0]] = [Range.from_string(results[0][1],True,True)]
        ranges[results[0][0]].append(Range.from_string(results[0][2],True,True))

    input_file.readline()
    your_ticket = [int(n) for n in input_file.readline().strip().split(',')]
    input_file.readline()
    input_file.readline()

    tickets = []
    for line in input_file:
        tickets.append([int(n) for n in line.strip().split(',')])


invalids = []
i = 0
while i < len(tickets):
    skip = False
    for item in tickets[i]:
        found = False
        for pair in ranges.values():
            for rng in pair:
                if item in rng:
                    found = True
                    break
            if found:
                break
        if not found:
            invalids += [item]
            skip = True
    if skip:
        tickets = tickets[:i] + tickets[i+1:]
    else:
        i += 1

print('Result 1:',sum(invalids))

viable_columns,final_columns = {},{}
for field in ranges:
    viable_columns[field] = find_column(ranges[field],tickets)

for _ in range(len(column_names)):
    for field in column_names:
        if field in viable_columns and len(viable_columns[field]) == 1:
            final_columns[field] = list(viable_columns[field])[0]
            del viable_columns[field]

            for field2 in viable_columns:
                if final_columns[field] in viable_columns[field2]:
                    viable_columns[field2].remove(final_columns[field])

prod = 1
for field in final_columns:
    if target_field_names in field:
        prod *= your_ticket[final_columns[field]]
print('Result 2:',prod)
