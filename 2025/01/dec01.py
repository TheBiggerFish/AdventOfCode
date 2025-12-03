


DIAL_SIZE = 100
current = 50
password_1 = 0
password_2 = 0

def have_different_sign(a, b):
    return (a < 0 and b > 0) or (a > 0 and b < 0)

with open('input.txt') as f:
    lines = f.read().splitlines()
    turns = map(lambda line: int(line.replace('L', 'L-')[1:]), lines)

for turn in turns:
    prev = current
    current += turn

    if current <= 0:
        password_2 += -current // 100 + (1 if prev != 0 else 0)
    elif current >= 100:
        password_2 += current // 100

    current %= DIAL_SIZE
    if current == 0:
        password_1 += 1

    print(f'Turn performed: {turn}, Current position: {current}, Passwords so far: {password_1}, {password_2}')

print(f'Final Passwords: {password_1}, {password_2}')
