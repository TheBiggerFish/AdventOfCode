from functools import reduce

operation_map = {
    '+': int.__add__,
    '*': int.__mul__,
}

with open('input.txt') as f:
    # numbers = [['123', '328', '51', '64'], ['45', '64', '387', '23'], ['6', '98', '215', '314']]
    # operators = ['*', '+', '*', '+']
    *numbers, operators = list(map(str.split, f.read().splitlines()))

    # operands = [[123, 45, 6], [328, 64, 98], [51, 387, 215], [64, 23, 314]]
    operands = zip(*(map(int, row) for row in numbers))

    # operations = [int.__mul__, int.__add__, int.__mul__, int.__add__]
    operations = map(operation_map.get, operators)

    # results = [33210, 490, 4243455, 401]
    results = map(reduce, operations, operands)

    print(f'Answer 1: {sum(results)}')