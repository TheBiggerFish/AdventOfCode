from dataclasses import dataclass, field
from math import lcm
from queue import Queue


@dataclass
class Pulse:
    """Represents a single pulse going out to multiple targets"""
    high: bool
    source: str
    targets: list[str]


@dataclass
class Module:
    """Represents a base Module component"""
    label: str
    targets: list[str]
    
    def pulse(self, pulse: Pulse) -> Pulse:
        """Forward input pulses to all targets"""
        return Pulse(pulse.high, self.label, self.targets)


@dataclass
class FlipFlop(Module):
    """Represents a flip-flop module component"""
    state: bool = False

    def pulse(self, pulse: Pulse) -> Pulse:
        """Toggle state and send pulse to all targets on lows, send empty pulse on highs"""
        if pulse.high:
            return Pulse(False, self.label, [])
        self.state = not self.state
        return Pulse(self.state, self.label, self.targets)


@dataclass
class Conjunction(Module):
    """Represents a conjunction module component"""
    memory: dict[str, bool] = field(default_factory=dict)

    def add_input(self, label: str):
        """Add an input to memory during setup phase"""
        self.memory[label] = False

    def pulse(self, pulse: Pulse) -> Pulse:
        """
            Update memory for input and pulse to all targets, 
            Output low if all inputs in memory are high, otherwise high
        """
        if pulse.source not in self.memory:
            raise KeyError
        self.memory[pulse.source] = pulse.high
        if all(self.memory.values()):
            return Pulse(False, self.label, self.targets)
        return Pulse(True, self.label, self.targets)

MODULE_MAPPING: dict[str, Module] = {
    '!': Module,
    '%': FlipFlop,
    '&': Conjunction,
}
        
@dataclass
class ModuleManager:
    """Solver for part 1 of AoC 2023.20"""
    modules: dict[str, Module]

    @staticmethod
    def parse_lines(lines: list[str]) -> 'ModuleManager':
        """Parse and store input"""
        modules: dict[str, Module] = {}
        for line in lines:
            typelabel, targets = line.split(' -> ')
            targets = targets.replace(' ','').split(',')
            
            # Give type indicator to broadcaster
            if typelabel == 'broadcaster':
                typelabel = '!broadcaster'

            type_, label = typelabel[0], typelabel[1:]
            module_type = MODULE_MAPPING[type_]
            modules[label] = module_type(label, targets)
        
        manager = ModuleManager(modules)
        manager.set_conjunction_inputs()
        return manager

    def set_conjunction_inputs(self):
        """
            Set inputs for conjunction module. Can't be done at declaration as
            we don't know conjunction inputs until after all modules have 
            already been parsed and declared
        """
        for label, module in self.modules.items():
            for target in module.targets:
                m = self.modules.get(target, None)
                if isinstance(m, Conjunction):
                    m.add_input(label)

    def press_button(self, watched: dict[str, bool]) -> tuple[int, int]:
        q: Queue[Pulse] = Queue()
        pulse = Pulse(high=False, source='Button', targets=['broadcaster'])
        lows, highs = 0, 0
        
        q.put(pulse)
        while not q.empty():
            pulse = q.get()

            # Marked when certain watched modules are pulsed high
            if watched is not None and pulse.high and pulse.source in watched:
                watched[pulse.source] = True

            # Count the number of pulses sent of each type
            if pulse.high:
                highs += len(pulse.targets)
            else:
                lows += len(pulse.targets)

            # Propogate pulse to downstream modules
            for target in pulse.targets:
                if target not in self.modules:
                    continue
                q.put(self.modules[target].pulse(pulse))
        
        return lows, highs


def main():
    with open('2023/20/input.txt') as f:
        lines = f.read().splitlines()

    # Solution for part 1, press button 1000 times
    manager1 = ModuleManager.parse_lines(lines)
    low, high = 0, 0
    for _ in range (1000):
        l, h = manager1.press_button({})
        low, high = low + l, high + h
    print(f'The product of low and high pulses is: {low * high}')

    # Soluton for part 2, press button a bunch to find lowest number required for each conjunction module
    manager2 = ModuleManager.parse_lines(lines)
    factors = {'sr': 0, 'sn': 0, 'rf': 0, 'vq': 0}
    for i in range (1, 10**10):
        watch = {factor: False for factor in factors}
        manager2.press_button(watch)
        
        # If any of the watched modules were activated with a high signal, save the index
        for found in filter(watch.get, watch):
            if factors[found] == 0:
                factors[found] = i
        
        # Break out if we found all of the factors
        if all(factors.values()):
            break
    lowest = lcm(*factors.values())
    print(f'The fewest number of button presses to send a low signal to rx is {lowest}')

if __name__ == '__main__':
    main()
