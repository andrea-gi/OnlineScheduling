from abc import ABC, abstractmethod


class TaskGenerator(ABC):
    @abstractmethod
    def generate_jobs(self):
        pass
