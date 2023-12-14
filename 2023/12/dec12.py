import re
from itertools import product

# Used for part 1, abandoned in part 2

class Spring:
    def __init__(self, state: str, condition: list[int]):
        self.state = re.sub(r'\.+', '.', state)
        self.condition = condition
        
        expr_list = ['#{' + str(cond) + '}' for cond in self.condition]
        expr_str = r'\.*' + r'\.+'.join(expr_list) + r'\.*'
        self.regex = re.compile(expr_str)
        
        self.missing = sum(self.condition) - self.state.count('#')
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(state={self.state}, condition={str(self.condition)})'
    
    def unfolded(self, count: int) -> 'Spring':
        return Spring('?'.join(self.state for _ in range(count)), self.condition * count)
    
    def arrangements(self) -> int:
        unknowns = self.state.count('?')
        valid_arrangements: set[str] = set()
        for arrangement in product('.#', repeat=unknowns):
            if self.missing != arrangement.count('#'):
                continue
            state = list(self.state)
            i = 0
            for j, char in enumerate(state):
                if char == '?':
                    state[j] = arrangement[i]
                    i += 1
            state = ''.join(state)
            if self.valid_arrangement(state):
                valid_arrangements.add(state)
        return len(valid_arrangements)

    def valid_arrangement(self, state: str) -> bool:
        """Test if arrangement is valid"""
        return self.regex.match(state)

def main():
    with open('2023/12/input.txt') as f:
        lines = f.read().splitlines()
        
    springs: list[Spring] = []
    for line in lines:
        state, condition = line.split()
        conditions = list(map(int, condition.split(',')))
        springs.append(Spring(state, conditions))
        
    # unfolded: list[Spring] = [spring.unfolded(5) for spring in springs]
    
    print(sum([print(spring.arrangements()) for spring in springs]))

if __name__ == '__main__':
    main()
