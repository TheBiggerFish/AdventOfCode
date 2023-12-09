History = list[int]


def diff_list(values: History):
    new = []
    for i, _ in enumerate(values[:-1]):
        new.append(values[i+1] - values[i])
    return new


def extrapolate_next_value(values: History) -> int:
    if values.count(0) == len(values):
        return 0   
    return values[-1] + extrapolate_next_value(diff_list(values))


def extrapolate_previous_value(values: History) -> int:
    if values.count(0) == len(values):
        return 0
    return values[0] - extrapolate_previous_value(diff_list(values))


def main():
    with open('2023/09/input.txt') as f:
        histories = [list(map(int, line.split())) for line in f.read().splitlines()]
    
    print(sum(extrapolate_next_value(history) for history in histories))
    print(sum(extrapolate_previous_value(history) for history in histories))


if __name__ == '__main__':
    main()
