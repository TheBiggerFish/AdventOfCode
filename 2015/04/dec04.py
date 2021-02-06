# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/4


from hashlib import md5
SECRET = 'bgvyzdsv'

i = 0
while str(md5((SECRET + str(i)).encode()).hexdigest())[:6] != '000000':
    i += 1
print('Santa\'s MD5 hash secret key is {}'.format(SECRET + str(i)))