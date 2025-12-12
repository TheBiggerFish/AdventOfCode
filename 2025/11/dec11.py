from functools import cache, partial

target = 'out'
waypoints = {'dac', 'fft'}

@cache
def number_of_paths(current_device: str, required_waypoints: int=0) -> int:
    if current_device == target and required_waypoints <= 0:
        return 1
    elif current_device == target or current_device not in devices:
        return 0

    if current_device in waypoints:
        required_waypoints -= 1

    recurse = partial(number_of_paths, required_waypoints=required_waypoints)
    return sum(map(recurse, devices[current_device]))

with open('input.txt') as f:
    devices = {line[:3]: line[4:].split() for line in f.read().splitlines()}

print(number_of_paths(current_device='you'))
print(number_of_paths(current_device='svr', required_waypoints=2))
