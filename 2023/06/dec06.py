from dataclasses import dataclass


@dataclass
class Race:
    time: int
    currentRecord: int

    def records(self) -> int:
        count = 0
        for speed in range(self.time):
            if speed * (self.time-speed) > self.currentRecord:
                # There are time + 1 possible seconds to hold the button down
                # The distances are symmetric so when the first record is found,
                #   subtract all non-records from both ends
                return (self.time + 1) - (speed * 2)
        return count


def main():
    with open('2023/06/input.txt') as f:
        time, distance = f.read().splitlines()

        times = list(map(int, time.split(':')[-1].split()))
        distances = list(map(int, distance.split(':')[-1].split()))

        true_time = int(time.split(':')[-1].replace(' ', ''))
        true_dist = int(distance.split(':')[-1].replace(' ', ''))

        races = [Race(time, dist) for time, dist in zip(times, distances)]
        true_race = Race(true_time, true_dist)

    prod = 1
    for race in races:
        prod *= race.records()
    print(prod)
    print(true_race.records())


if __name__ == '__main__':
    main()
