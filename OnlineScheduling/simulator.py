from abc import ABC, abstractmethod
from OnlineScheduling.solution import Solution


class Simulator(ABC):
    def __init__(self, capacity):
        self.capacity = capacity

    @abstractmethod
    def process_input(self, input_sequence: Solution) -> Solution:
        pass

