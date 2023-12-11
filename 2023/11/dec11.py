from fishpy.geometry import LatticePoint


def galactic_expansion(universe: list[str], expansion: int) -> list[LatticePoint]:
    """Take in a grid, return all galaxies (#) with positions offset by expansion"""
    expansion_offset = 0
    galaxies: list[LatticePoint] = []
    for y, line in enumerate(universe):
        empty_row = True
        for x, cell in enumerate(line):
            if cell == '#':
                galaxies.append(LatticePoint(x, y + expansion_offset))
                empty_row = False
        if empty_row:
            expansion_offset += expansion - 1

    empty_columns = set(range(len(universe[0]))).difference({galaxy.x for galaxy in galaxies})
    for galaxy in galaxies:
        preceding_empties = len(list(filter(lambda col: col < galaxy.x, empty_columns)))
        galaxy.x += preceding_empties * (expansion-1)
        
    return galaxies

def total_distances(galaxies: list[LatticePoint]) -> int:
    """Return the sum of manhattan distances between all pairs of galaxies (don't double count)"""
    galaxy_distances = 0    
    for i, galaxy in enumerate(galaxies):
        for j in range(i+1, len(galaxies)):
            galaxy_distances += galaxy.manhattan_distance(galaxies[j])
    return galaxy_distances
    


def main():
    with open('2023/11/input.txt') as f:
        lines = f.read().splitlines()
    
    galaxies = galactic_expansion(lines, 2)
    distances = total_distances(galaxies)
    print(f'The sum of distances between the galaxies with expansion 2 is: {distances}')
    
    galaxies = galactic_expansion(lines, 1_000_000)
    distances = total_distances(galaxies)
    print(f'The sum of distances between the galaxies with expansion 1,000,000 is: {distances}')
        
    
            


if __name__ == '__main__':
    main()
