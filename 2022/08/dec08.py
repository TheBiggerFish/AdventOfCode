from fishpy.geometry import LatticePoint, Vector2D
from fishpy.geometry.d2.vector2d import DOWN, LEFT, RIGHT, UP
from fishpy.pathfinding.grid import Grid


class Forest(Grid):
    def __init__(self, trees: list[list[int]]):
        grid = Grid.from_list_of_strings(trees).grid
        super().__init__(grid)

    def view_line(self, pos: LatticePoint, direction: Vector2D, steps: int) -> tuple[bool, int]:
        for step in range(1, steps+1):
            value = self[pos + direction * step].rep
            if value >= self[pos].rep:
                return False, step
        return True, steps

    def tree_visible(self, pos: LatticePoint) -> bool:
        directions = [(self.width-pos.x-1, RIGHT), (pos.x, LEFT),
                      (self.height-pos.y-1, UP), (pos.y, DOWN)]
        for steps, direction in sorted(directions):
            # Sort list of directions to go to nearest side first

            clear, _ = self.view_line(pos, direction, steps)
            if clear:
                return True
        return False

    def scenic_score(self, pos: LatticePoint) -> int:
        directions = [(self.width-pos.x-1, RIGHT), (pos.x, LEFT),
                      (self.height-pos.y-1, UP), (pos.y, DOWN)]
        total = 1
        for steps, direction in directions:
            _, view = self.view_line(pos, direction, steps)
            total *= view
        return total


with open('2022/08/input.txt') as f:
    trees = [[int(c) for c in line] for line in f.read().splitlines()]

forest = Forest(trees)
print(forest)

visible_trees = sum(map(forest.tree_visible, forest))
print(visible_trees)

best_score = max(map(forest.scenic_score, forest))
print(best_score)
