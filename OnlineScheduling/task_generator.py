from OnlineScheduling.job import Job
from OnlineScheduling.solution import Solution


class TaskGenerator:
    def __init__(self, number_of_classes, arrival, length, fare_class):
        self.arrival_fun, self.arrival_params = None, None
        self.length_fun, self.length_params = None, None
        self.fare_class_fun, self.fare_class_params = None, None
        self.number_of_classes = number_of_classes
        self.set_arrival_dist(arrival[0], arrival[1:])
        self.set_length_dist(length[0], length[1:])
        self.set_fare_class_dist(fare_class[0], fare_class[1:])

    def generate_jobs(self, number_of_sequences: int, number_of_jobs: int) -> list[Solution]:
        sequences = list()
        for _ in range(number_of_sequences):
            solution = Solution(self.number_of_classes)
            jobs = list()
            arrival = self.arrival_fun(*self.arrival_params, size=number_of_jobs)
            length = self.length_fun(*self.length_params, size=number_of_jobs)
            fare_class = self.fare_class_fun(*self.fare_class_params, size=number_of_jobs)

            for idx in range(number_of_jobs):
                jobs.append((round(arrival[idx]), round(length[idx]), round(fare_class[idx])))

            jobs.sort(key=lambda x: x[0])
            for idx, job in enumerate(jobs):
                solution.add_job(Job(idx, *job))
            sequences.append(solution)

        return sequences

    def set_arrival_dist(self, arrival, params):
        self.arrival_fun = arrival
        self.arrival_params = params

    def set_length_dist(self, length, params):
        self.length_fun = length
        self.length_params = params

    def set_fare_class_dist(self, fare_class, params):
        self.fare_class_fun = fare_class
        self.fare_class_params = params
