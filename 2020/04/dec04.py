# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/4


from fishpy.structures import Range
import re

EXPECTED_FIELDS = {'byr','iyr','eyr','hgt','hcl','ecl','pid'}
def validate1(passport) -> bool:
    for field in EXPECTED_FIELDS:
        if field not in passport:
            return False
    return True

def validate2(passport) -> bool:
    if not validate1(passport):
        return False
    if int(passport['byr']) not in Range(1920,2002,upper_inclusive=True):
        #print('byr')
        return False
    if int(passport['iyr']) not in Range(2010,2020,upper_inclusive=True):
        #print('iyr')
        return False
    if int(passport['eyr']) not in Range(2020,2030,upper_inclusive=True):
        #print('eyr')
        return False
    if not (match := re.search(r'(\d+)(in|cm)',passport['hgt'])):
        #print('No unit')
        return False
    if match.group(2) == 'cm' and int(match.group(1)) not in Range(150,193,upper_inclusive=True):
        #print('CM')
        return False
    if match.group(2) == 'in' and int(match.group(1)) not in Range(59,76,upper_inclusive=True):
        #print('IN')
        return False
    if not re.fullmatch(r'\#[0-9a-f]{6}',passport['hcl']):
        #print('hcl')
        return False
    if passport['ecl'] not in {'amb','blu','brn','gry','grn','hzl','oth'}:
        #print('ecl')
        return False
    if not re.fullmatch(r'\d{9}',passport['pid']):
        #print('pid')
        return False
    print(passport)
    return True


with open('2020/04/input.txt') as f:
    count1,count2 = 0,0
    for pp_string in f.read().split('\n\n'):
        passport = {prop.split(':')[0]:prop.split(':')[1] for prop in pp_string.split()}
        if validate1(passport):
            count1 += 1
        if validate2(passport):
            count2 += 1
            
    print(count1)
    print(count2)

