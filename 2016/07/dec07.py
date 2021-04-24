# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/7


import re

def tls(string):
    if re.findall(r'\[\w*(\w)(\w)\2\1\w*\]',string) == [] and (result := re.findall(r'(\w)(\w)\2\1',string)) != []:
        for item in result:
            if item[0] != item[1]:
                return True
    return False

def ssl(string):
    if (result := re.findall(r'\[\w*(\w)(\w)\1.*\]\w*\2\1\2',string)) != []:
        for item in result:
            if item[0] != item[1]:
                return True
    if (result := re.findall(r'(\w)(\w)\1\w*\[.*\2\1\2\w*\]',string)) != []:
        for item in result:
            if item[0] != item[1]:
                return True
    return False


count_tls,count_ssl = 0,0
with open('2016/07/input.txt') as in_file:
    for line in in_file:
        if tls(line.strip()):
            count_tls += 1
        if ssl(line.strip()):
            count_ssl += 1

print(f'The number of IPs that support TLS is {count_tls} and the number of IPs that support SSL is {count_ssl}')