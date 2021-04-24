# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/5


from hashlib import md5
SECRET = 'uqwqemis'


i = 0
passwd1 = ''
for _ in range(8):
    while (enc := str(md5((SECRET + str(i)).encode()).hexdigest()))[:5] != '00000':
        i += 1
    passwd1 += enc[5]
    i += 1

i = 0
passwd2 = ' ' * 8
for _ in range(8):
    while (enc := str(md5((SECRET + str(i)).encode()).hexdigest()))[:5] != '00000' or not enc[5].isnumeric() or int(enc[5]) >= 8 or passwd2[int(enc[5])] != ' ':
        i += 1
    index = int(enc[5])
    passwd2 = passwd2[:index] + enc[6] + passwd2[index+1:]
    i += 1

print(f'Given the Easter Bunny\'s door id {SECRET}, the password to the first door is {passwd1}')
print(f'Given the same door id, the password to the second door is {passwd2}')