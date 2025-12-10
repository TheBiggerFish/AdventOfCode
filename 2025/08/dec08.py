from fishpy.geometry import LatticePoint3D as Point
from itertools import count
from queue import PriorityQueue
from math import prod

TARGET_CONNECTIONS = 1000

circuit_name = (f'circuit_{i}' for i in count())

with open('input.txt') as f:
    lines = f.read().splitlines()
    boxes = sorted(map(lambda s: Point(*map(int, s.split(','))), lines))
    circuit = {box: next(circuit_name) for box in boxes}
    circuits = {circuit[box]: {box} for box in boxes}
    pq = PriorityQueue()
    for i, b1 in enumerate(boxes):
        for b2 in boxes[i+1:]:
            dist = b1.euclidean_distance(b2)
            pq.put((dist, b1, b2))

connections = 0
while not pq.empty() and len(circuits) > 1:
    if connections == TARGET_CONNECTIONS:
        top_circuits_by_size = sorted(circuits.values(), key=len, reverse=True)[:3]
        print('Part 1:', prod(map(len, top_circuits_by_size)))

    connections += 1
    _, box1, box2 = pq.get()
    if circuit[box1] == circuit[box2]:
        continue

    if len(circuits) == 2:
        print(f'Part 2: {box1.x * box2.x}')

    smaller_circuit, larger_circuit = (circuit[box1], circuit[box2]) if len(circuits[circuit[box1]]) < len(circuits[circuit[box2]]) else (circuit[box2], circuit[box1])
    circuits[larger_circuit].update(circuits[smaller_circuit])
    for box in circuits[smaller_circuit]:
        circuit[box] = larger_circuit
    del circuits[smaller_circuit]

