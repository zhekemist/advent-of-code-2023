from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple, Self


class PulseType(Enum):
    LOW = 0
    HIGH = 1


class Pulse(NamedTuple):
    sender: str
    receiver: str
    pulse_type: PulseType


@dataclass
class Module:
    id: str
    pulse_counter: Counter[PulseType] = field(repr=False)
    outputs: list[str] = field(default_factory=list)

    def register_input(self, input_module: str) -> None:
        pass

    def receive_pulse(self, pulse_type: PulseType, sender: str) -> list[Pulse]:
        self.pulse_counter[pulse_type] += 1
        return []

    def _broadcast(self, pulse_type: PulseType) -> list[Pulse]:
        return [Pulse(self.id, output_module, pulse_type)
                for output_module in self.outputs]


@dataclass
class Broadcaster(Module):
    def receive_pulse(self, pulse_type: PulseType, sender: str) -> list[Pulse]:
        super().receive_pulse(pulse_type, sender)
        return self._broadcast(pulse_type)


@dataclass
class FlipFlop(Module):
    activated: bool = field(default=False)

    def receive_pulse(self, pulse_type: PulseType, sender: str) -> list[Pulse]:
        super().receive_pulse(pulse_type, sender)
        if pulse_type == PulseType.LOW:
            self.activated = not self.activated
            if self.activated:
                return self._broadcast(PulseType.HIGH)
            else:
                return self._broadcast(PulseType.LOW)
        else:
            return []


@dataclass
class Conjunction(Module):
    last_inputs: dict[str, PulseType] = field(default_factory=dict)

    def register_input(self, input_module: str) -> None:
        self.last_inputs[input_module] = PulseType.LOW

    def receive_pulse(self, pulse_type: PulseType, sender: str) -> list[Pulse]:
        super().receive_pulse(pulse_type, sender)
        self.last_inputs[sender] = pulse_type
        if all(saved_pulse == PulseType.HIGH for saved_pulse in self.last_inputs.values()):
            return self._broadcast(PulseType.LOW)
        else:
            return self._broadcast(PulseType.HIGH)


@dataclass
class Monitor(Conjunction):
    received_low_pulse: bool = field(default=False)

    def receive_pulse(self, pulse_type: PulseType, sender: str) -> list[Pulse]:
        if pulse_type == PulseType.LOW:
            self.received_low_pulse = True
        return super().receive_pulse(pulse_type, sender)

    @classmethod
    def from_conjunction(cls, conjunction: Conjunction) -> Self:
        return cls(conjunction.id, conjunction.pulse_counter, conjunction.outputs, conjunction.last_inputs)
