from OnlineScheduling.job import Job


class Solution:
    def __init__(self, m: int, jobs=None, max_time=0):
        self.max_time = max_time
        self.m = m
        self.jobs = [set() for _ in range(m)]
        if jobs is not None:
            for j in jobs:
                self.add_job(j)

    def add_job(self, j: Job):
        self.max_time = max(self.max_time, j.arrival+j.duration)
        self.jobs[j.fare_class].add(j)

    def get_lowest_class_solution(self, i):
        return Solution(self.m, [set() for _ in range(self.m-i)] + self.jobs[-i:], self.max_time)

    def get_sorted_jobs(self, fare_class=None) -> list:
        result = list()
        if fare_class is None:
            for fare_class in self.jobs:
                result.extend(list(fare_class))
        else:
            sorted_jobs = sorted(list(self.jobs[fare_class]))
            result.extend(sorted_jobs)
        result.sort()
        return result
