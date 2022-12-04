from fishpy.structures import Range

with open('2022/04/input.txt') as f:
    pairs = [[Range.from_string(range, True)
              for range in line.split(',')]
             for line in f.read().splitlines()]
    contained = filter(lambda p: p[0] in p[1] or p[1] in p[0], pairs)
    overlapping = filter(lambda p: p[0].overlap(p[1]), pairs)
    print(len(list(contained)))
    print(len(list(overlapping)))
