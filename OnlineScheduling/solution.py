from OnlineScheduling.job import Job
from heapq import heappush, heappop
import logging


class Solution:
    def __init__(self, m: int, jobs=None, max_time=0):
        self.number_of_jobs = 0
        self.max_time = max_time
        self.m = m
        self.up_to_date = False
        self.sorted_jobs = list()
        self.jobs = [set() for _ in range(m)]
        if jobs is not None:
            for j in jobs:
                self.add_job(j)
            self.get_sorted_jobs()

    def add_job(self, j: Job):
        self.number_of_jobs += 1
        self.up_to_date = False
        self.max_time = max(self.max_time, j.arrival+j.duration)
        self.jobs[j.fare_class].add(j)

    def get_lowest_class_solution(self, i):
        return Solution(self.m, [set() for _ in range(self.m-i)] + self.jobs[-i:], self.max_time)

    def get_sorted_jobs(self, fare_class=None) -> list:
        if self.up_to_date and fare_class is None:
            return self.sorted_jobs  # cache of all sorted jobs
        result = list()
        if fare_class is None:
            for fc in self.jobs:
                result.extend(list(fc))
        else:
            sorted_jobs = sorted(list(self.jobs[fare_class]))
            result.extend(sorted_jobs)
        result.sort()
        if fare_class is None:
            self.up_to_date = True
            self.sorted_jobs = result
        return list(result)

    def get_value(self, fares) -> float:
        return sum([fares[j.fare_class] * j.duration for j in self.get_sorted_jobs()])

    def verify_solution(self, capacity):
        current_time = 0
        running = list()
        for job in self.get_sorted_jobs():
            current_time = max(current_time, job.arrival)  # Update the time only when it advances
            while running and running[0][0] <= current_time:
                heappop(running)  # Remove jobs that have finished from the running list
            heappush(running, (job.arrival + job.duration, job))
            if len(running) > capacity:
                return False
        return True

    def overlap_times(self, capacity):
        current_time = 0
        over_capacity = False
        overlapping_jobs = set()
        running_jobs_id = set()
        running = list()

        for job in self.get_sorted_jobs():
            current_time = max(current_time, job.arrival)  # Update the time only when it advances
            if over_capacity and running and running[0][0] <= current_time:  # Add jobs to constraint only at peak (before removing)
                running_jobs_id_list = list(running_jobs_id)
                running_jobs_id_list.sort()
                overlapping_jobs.add(tuple(running_jobs_id_list))
            while running and running[0][0] <= current_time:
                to_remove = heappop(running)[1]  # Remove jobs that have finished from the running list
                running_jobs_id.remove(to_remove.index)
            heappush(running, (job.arrival + job.duration, job))
            running_jobs_id.add(job.index)
            over_capacity = len(running) > capacity
        if over_capacity:  # Check if last timestep is a peak
            running_jobs_id_list = list(running_jobs_id)
            running_jobs_id_list.sort()
            overlapping_jobs.add(tuple(running_jobs_id_list))
        logging.info("Computed overlaps when n_jobs > capacity. {} constraints found".format(len(overlapping_jobs)))
        return overlapping_jobs

    def __len__(self):
        return self.number_of_jobs
