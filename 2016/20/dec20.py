# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/20


from EulerLib.structures import Range

with open('2016/20/input.txt') as f:
    ranges = []
    for line in f:
        line = line.strip().split('-')
        lower = int(line[0])
        upper = int(line[1])
        ranges.append(Range(lower,upper,lower_inclusive=True,upper_inclusive=True))
    

    ranges = sorted(ranges)
    answer1 = 0
    answer2 = 0
    cur = 0
    found = False
    while len(ranges) > 0:
        i = 0
        while i < len(ranges):
            skip = 1
            while i + skip < len(ranges) and ranges[i+skip].upper < ranges[i].upper:
                skip += 1
            skip -= 1
            if cur in ranges[i]:
                cur = ranges[i].upper+1
                i += 1 + skip
            else:
                break

        if not found:
            found = True
            answer1 = cur
        ranges = list(filter(lambda r: r.upper >= cur,ranges))
        if len(ranges) > 0:
            answer2 += min(ranges).lower - cur
            cur = min(ranges).lower

    print(f'The lowest-valued IP that is not blocked is {answer1}')
    print(f'There are {answer2} IPs allowed by the blacklist')


        