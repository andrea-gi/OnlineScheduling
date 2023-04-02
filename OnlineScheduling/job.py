class Job:
    def __init__(self, index: int, arrival: int, duration: int, fare_class: int):
        self.index = index
        self.arrival = arrival
        self.duration = duration
        self.fare_class = fare_class

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Job):
            return self.index == other.index and self.arrival == other.arrival and \
                self.duration == other.duration and self.fare_class == other.fare_class
        return False

    def __lt__(self, other):
        return self.index < other.index

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return "({},{},{},{})".format(self.index, self.arrival, self.duration, self.fare_class)

    def overlap(self, other):
        return self.arrival < other.arrival + other.duration and self.arrival + self.duration > other.arrival
