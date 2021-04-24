# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/11


import re
def secure(pw):
    condition1 = len([pw[i]+pw[i+1]+pw[i+2] for i in range(len(pw)-2) if ord(pw[i])+2 == ord(pw[i+1])+1 == ord(pw[i+2])]) > 0
    condition2 = len(re.findall('[iol]',pw)) == 0
    condition3 = len(re.findall(r'(\w)\1.*(\w)\2',pw)) > 0
    return condition1 and condition2 and condition3

def increment(pw):
    new_pw = ''
    carry_flag = True
    for i in range(len(pw)-1,-1,-1):
        if carry_flag:
            new_char = chr(ord(pw[i])+1) if pw[i] < 'z' else 'a'
            if len(re.findall('[iol]',new_char)) != 0:
                new_char = chr(ord(new_char[0])+1)
            new_pw = new_char + new_pw
            if pw[i] != 'z':
                carry_flag = False
        else:
            new_pw = pw[i] + new_pw
    return new_pw

pw = 'cqjxxyzz'
while not secure(pw):
    pw = increment(pw)
    
new_pw = increment(pw)
while not secure(new_pw):
    new_pw = increment(new_pw)

print('Santa\'s next secure password is {}, then {} after that'.format(pw,new_pw))