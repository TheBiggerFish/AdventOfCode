# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/7


import re

def super_bags(bag_rules:dict,bag_color:str):
    if bag_color not in bag_rules:
        return set()
        
    seen = set()
    for holder in bag_rules[bag_color]:
        seen |= {holder} | super_bags(bag_rules,holder)
    return seen

def sub_bags(bag_rules:dict,root_bag:str):
    if not bag_rules[root_bag]:
        return 1
    count = 0
    for sub_bag in bag_rules[root_bag]:
        count += sub_bags(bag_rules,sub_bag) * bag_rules[root_bag][sub_bag]
    return count + 1

containers,subcontainers = {},{}
with open('2020/07/input.txt','r') as input_file:
    for line in input_file:
        rule = line.strip()
        color = ' '.join(rule.split()[:2]) #  Get first 2 words
        subcontainers[color] = {}
        if 'no' in rule:
            continue
        matches = re.findall(r'(\d+) (\w+ \w+)',rule)
        for match in matches:
            subcontainers[color][match[1]] = int(match[0])
            if match[1] in containers:
                containers[match[1]].add(color)
            else:
                containers[match[1]] = {color}

print('First Result:',len(super_bags(containers,'shiny gold')))
print('Second Result:',sub_bags(subcontainers,'shiny gold')-1)  # Subtract one to not count the shiny gold bag