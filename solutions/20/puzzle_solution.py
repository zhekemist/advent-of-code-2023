from collections import deque
from typing import Any

import math

import adventofcode as aoc
from .modules import *


def parse_modules(puzzle_input: aoc.PuzzleInput) -> tuple[dict[str, Module], Counter[Any]]:
    pulse_counter = Counter({pulse_type: 0 for pulse_type in PulseType})
    modules = {}
    module_outputs = {}

    for line in puzzle_input.get_lines():
        module_id, outputs = line.split(' -> ')
        outputs = outputs.split(', ')

        if module_id == 'broadcaster':
            modules[module_id] = Broadcaster(module_id, pulse_counter, outputs)
        if module_id[0] == '%':
            module_id = module_id[1:]
            modules[module_id] = FlipFlop(module_id, pulse_counter, outputs)
        elif module_id[0] == '&':
            module_id = module_id[1:]
            modules[module_id] = Conjunction(module_id, pulse_counter, outputs)

        module_outputs[module_id] = outputs

    for module_id, outputs in module_outputs.items():
        for output in outputs:
            if output not in modules:
                modules[output] = Module(output, pulse_counter, [])
            modules[output].register_input(module_id)

    return modules, pulse_counter


def press_button(modules: dict[str, Module]) -> None:
    pulse_queue = deque()
    pulse_queue.append(Pulse('button', 'broadcaster', PulseType.LOW))

    while len(pulse_queue) > 0:
        pulse = pulse_queue.popleft()
        answered_pulses = modules[pulse.receiver].receive_pulse(pulse.pulse_type, pulse.sender)
        pulse_queue.extend(answered_pulses)


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    modules, pulse_counter = parse_modules(puzzle_input)
    for _ in range(1000):
        press_button(modules)
    return math.prod(pulse_counter.values())


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    print('WARNING: This solution is not general and uses hardcoded assumptions about my personal input.')
    modules, pulse_counter = parse_modules(puzzle_input)

    monitors = []
    for monitor_id in ['tf', 'vq', 'db', 'ln']:
        modules[monitor_id] = monitor = Monitor.from_conjunction(modules[monitor_id])
        monitors.append(monitor)

    button_presses = 0
    activated_after = {}
    while len(activated_after) != len(monitors):
        button_presses += 1
        press_button(modules)
        for monitor in monitors:
            if monitor.id not in activated_after and monitor.received_low_pulse:
                activated_after[monitor.id] = button_presses

    return math.lcm(*activated_after.values())
