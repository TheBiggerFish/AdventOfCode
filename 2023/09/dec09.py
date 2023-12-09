class OASIS:
    def __init__(self, values = list[int]):
        self.values = values
            
    @staticmethod
    def diff_list(values: list[int]):
        new = []
        for i, value in enumerate(values):
            if i+1 >= len(values):
                break
            new.append(values[i+1] - value)
        return new
    
    @staticmethod
    def extrapolate_next_value(values: list[int]) -> int:
        if values.count(0) == len(values):
            return 0
        
        diff_list = OASIS.diff_list(values)
        return values[-1] + OASIS.extrapolate_next_value(diff_list)
    
    @staticmethod
    def extrapolate_previous_value(values: list[int]) -> int:
        if values.count(0) == len(values):
            return 0
        
        diff_list = OASIS.diff_list(values)
        return values[0] - OASIS.extrapolate_previous_value(diff_list)
        
        

def main():
    with open('2023/09/input.txt') as f:
        oases = [OASIS(list(map(int, line.split()))) for line in f.read().splitlines()]
    
    print(sum(OASIS.extrapolate_next_value(oasis.values) for oasis in oases))
    print(sum(OASIS.extrapolate_previous_value(oasis.values) for oasis in oases))


if __name__ == '__main__':
    main()
