from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class MachineStatus(Enum):
    UP = "UP"
    DOWN = "DOWN"


@dataclass
class Machine:
    hostname: str
    status: MachineStatus


class Machines(ABC):
    @abstractmethod
    def get_machine(self, identifier: str) -> Machine:
        pass
