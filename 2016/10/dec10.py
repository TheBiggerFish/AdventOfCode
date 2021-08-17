# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/10


from fishpy.structures import ReversiblePriorityQueue

class Giver:
    def __init__(self,value,who):
        self.value = value
        self.who = who

    @staticmethod
    def from_string(string):
        spl = string.split()
        return Giver(int(spl[1]),int(spl[5]))

    def __str__(self):
        return f'Value {self.value} goes to bot {self.who}'

class Receiver:
    UNKNOWN = 0
    BOT = 1
    OUTPUT = 2

    def __init__(self,value,type=UNKNOWN):
        self.value = value
        self.type = type
        self.items = []

    def set_type(self,type):
        self.type = type

    def add_item(self,item):
        self.items.append(item)

    def __lt__(self,other):
        return self.value < other.value

class Bot:
    def __init__(self,id,lower,upper):
        self.id = id
        self.lower = lower
        self.upper = upper
        self.items = []

    def add_item(self,item):
        if len(self.items) >= 2:
            raise Exception(f'Bot {self.id} is holding too many items')
        self.items.append(item)

    def pop_low(self):
        low = min(self.items)
        if len(self.items) == 2:
            self.items = [max(self.items)]
        else:
            self.items = []
        return low

    def pop_high(self):
        high = max(self.items)
        if len(self.items) == 2:
            self.items = [min(self.items)]
        else:
            self.items = []
        return high


    @staticmethod
    def from_string(string):
        spl = string.split()
        lower = Receiver(int(spl[6]))
        if spl[5] == 'bot':
            lower.set_type(Receiver.BOT)
        else:
            lower.set_type(Receiver.OUTPUT)

        upper = Receiver(int(spl[11]))
        if spl[10] == 'bot':
            upper.set_type(Receiver.BOT)
        else:
            upper.set_type(Receiver.OUTPUT)
        return Bot(int(spl[1]),lower,upper)

    def __lt__(self,other):
        if len(self.items) != len(other.items):
            return len(self.items) < len(other.items)
        return self.id < other.id

    def __gt__(self,other):
        if len(self.items) != len(other.items):
            return len(self.items) > len(other.items)
        return self.id > other.id
    
    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self):
        return self.id



with open('2016/10/input.txt') as f:
    bots = []
    values = []
    outputs = []
    for line in f:
        line = line.strip()
        if line[:3] == 'bot':
            bots.append(Bot.from_string(line))
        else:
            values.append(Giver.from_string(line))

    bots = sorted(bots)

    holders = set()
    for value in values:
        bots[value.who].add_item(value.value)
    for bot in bots:
        if bot.items:
            holders.add(bot)
        if bot.lower.type == Receiver.OUTPUT:
            outputs.append(bot.lower)
        if bot.upper.type == Receiver.OUTPUT:
            outputs.append(bot.upper)
    outputs = sorted(outputs)

    while len(holders) > 0:
        bot = max(holders)
        holders.remove(bot)
        if len(bot.items) != 2:
            raise Exception(f'Current bot {bot.id} not holding 2 items when called')

        low = bot.pop_low()
        high = bot.pop_high()
        # print(f'Bot {bot.id} is comparing values {low} and {high}')

        if bot.lower.type == Receiver.BOT:
            # print(f'Bot {bot.lower.value} received value {low}')
            bots[bot.lower.value].add_item(low)
            holders.add(bots[bot.lower.value])
        else:
            outputs[bot.lower.value].add_item(low)

        if bot.upper.type == Receiver.BOT:
            # print(f'Bot {bot.upper.value} received value {high}')
            bots[bot.upper.value].add_item(high)
            holders.add(bots[bot.upper.value])
        else:
            outputs[bot.lower.value].add_item(low)

        if low == 17 and high == 61:
            print(f'Bot {bot.id} is comparing values 17 and 61')

    print(f'Final chip output is {outputs[0].items[0] * outputs[1].items[0] * outputs[2].items[0]}')
        