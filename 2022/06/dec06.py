def find_marker(string: str, length: int) -> int:
    for i,_ in enumerate(string):
        if len(set(string[i-length:i])) == length:
            return i
    return -1

with open('2022/06/input.txt') as f:
    signal = f.read().strip()
    print(find_marker(signal, 4))
    print(find_marker(signal, 14))