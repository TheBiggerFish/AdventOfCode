# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/15


from functools import reduce

class Cookie:
    MAX_INGREDIENTS = 100
    def __init__(self,ingredients:list):
        self.ingredients = ingredients

    def add_ingredient(self,ingredient):
        self.ingredients.append(ingredient)

    def mix(self):
        return reduce(Ingredient.__add__,self.ingredients).mix()

    def __gt__(self,other):
        return self.mix() > other.mix()   

    def __lt__(self,other):
        return self.mix() < other.mix()
    
    def __str__(self):
        return '\n'.join(str(i) for i in self.ingredients)
    


class Ingredient:
    def __init__(self,capacity:int,durability:int,flavor:int,texture:int,calories:int,amount:int=0):
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories
        self.amount = amount

    def __add__(self,other):
        capacity = (self.capacity * self.amount) + (other.capacity * other.amount)
        durability = (self.durability * self.amount) + (other.durability * other.amount)
        flavor = (self.flavor * self.amount) + (other.flavor * other.amount)
        texture = (self.texture * self.amount) + (other.texture * other.amount)
        calories = (self.calories * self.amount) + (other.calories * other.amount)
        amount = 1
        return Ingredient(capacity,durability,flavor,texture,calories,amount)

    def mix(self):
        return max(self.capacity,0) * max(self.durability,0) * max(self.flavor,0) * max(self.texture,0)

    def with_amount(self,amount:int):
        return Ingredient(self.capacity,self.durability,self.flavor,self.texture,self.calories,amount)

    @staticmethod
    def from_string(string):
        split = string.strip().split(' ')
        split = ' '.join([word.strip(',:') for word in split]).split(' ')
        return Ingredient(int(split[2]),int(split[4]),int(split[6]),int(split[8]),int(split[10]))

    def __str__(self):
        return 'capacity {}, durability {}, flavor {}, texture {}, calories {}'.format(self.capacity,self.durability,self.flavor,self.texture,self.calories) + '' if self.amount == 0 else ', amount ' + str(self.amount)


from itertools import chain, combinations
def powerset(s):
    return set(chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1)))


ingredients = []
best = 0
cookie = None
with open('2015/15/input.txt') as f:
    for line in f:
        ingredients.append(Ingredient.from_string(line))
    for i in range(Cookie.MAX_INGREDIENTS+1):
        print('Run',i)
        for j in range(Cookie.MAX_INGREDIENTS+1-i):
            for k in range(Cookie.MAX_INGREDIENTS+1-i-j):
                l = Cookie.MAX_INGREDIENTS - i - j - k
                ing = [ingredients[0].with_amount(i),ingredients[1].with_amount(j),ingredients[2].with_amount(k),ingredients[3].with_amount(l)]
                if best >= (new := Cookie(ing)).mix():
                    best = new.mix()
                    cookie = new

print('The best cookie has a final score of {}.'.format(best))
print(cookie)