# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/14


class Reindeer:
    def __init__(self,name:str,speed:int,sprint_time:int,rest_time:int):
        self.SPEED = speed
        self.NAME = name
        self.SPRINT_TIME = sprint_time
        self.REST_TIME = rest_time
        self.distance = 0
        self.state = 'sprinting'
        self.time_to_change = sprint_time+1
        self.score = 0
    
    @staticmethod
    def from_string(string):
        split = string.strip().strip('.').split(' ')
        return Reindeer(split[0],int(split[3]),int(split[6]),int(split[13]))

    def update(self):
        if self.time_to_change <= 1:
            if self.state == 'ready' or self.state == 'resting':
                self.distance += self.SPEED
                self.time_to_change = self.SPRINT_TIME
                self.state = 'sprinting'
            elif self.state == 'sprinting':
                self.time_to_change = self.REST_TIME
                self.state = 'resting'
        else:
            if self.state == 'sprinting':
                self.distance += self.SPEED
            self.time_to_change -= 1
    
    def __str__(self):
        return '{} can fly {} km/s for {} seconds, but then must rest for {} seconds.'.format(self.name,self.speed,self.sprint_time,self.rest_time)

deers = []
end_time = 2503
with open('2015/14/input.txt') as f:
    for line in f:
        deers.append(Reindeer.from_string(line))
    for time in range(1,end_time+1):
        for deer in deers:
            deer.update()
        leader = max([(deers[which].distance,which) for which in range(len(deers))])[1]
        deers[leader].score += 1
                # print('{} has changed state to {} at {} seconds, having travelled {} km.'.format(deer.NAME,deer.state,time,deer.distance))
    # for deer in deers:
    #     print('{} has travelled {} km after {} seconds, having run out of time while {}.'.format(deer.NAME,deer.distance,time,deer.state))
leader = max([(deer.distance,deer.NAME) for deer in deers])
winner = max([(deer.score,deer.NAME) for deer in deers])
print('The leading deer is {}, who has travelled {} km.'.format(leader[1],leader[0]))
print('The winning deer is {} with a score of {} points'.format(winner[1],winner[0]))