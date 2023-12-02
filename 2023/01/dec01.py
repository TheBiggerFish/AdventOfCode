import re

one_number = re.compile(r'^\D*(\d)\D*$')
two_numbers = re.compile(r'^\D*(\d).*(\d)\D*$')

# Replace word with respective digit. Readd letters that may interact with another word
# Ex: tw(one)ight -> tw(o1e)ight -> (two)1(eight)
# Is there a better way? Probably
replacement = {
    'one': 'o1e',
    'two': 't2',
    'three': 't3e',
    'four': '4',
    'five': '5e',
    'six': '6',
    'seven': '7n',
    'eight': 'e8t',
    'nine': 'n9e',
}


def getNumber(line: str) -> int:
    match = one_number.match(line)
    if match is not None:
        return int(match[1] + match[1])
    match = two_numbers.match(line)
    return int(match[1] + match[2])


def preprocess(line: str) -> str:
    processed = line
    for word, digit in replacement.items():
        processed = processed.replace(word, digit)
    return processed


def main():
    with open('2023/01/input.txt') as f:
        lines = f.read().splitlines()
    preprocessed = map(preprocess, lines)
    sum_1 = sum(map(getNumber, lines))
    sum_2 = sum(map(getNumber, preprocessed))
    print(sum_1)
    print(sum_2)


if __name__ == '__main__':
    main()
