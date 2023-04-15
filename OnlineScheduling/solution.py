from OnlineScheduling.job import Job
from heapq import heappush, heappop
from numpy import random
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

    def get_sorted_jobs(self, fare_class=None) -> list[Job]:
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

    def verify_solution(self, capacity: int) -> bool:
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

    def overlap_times(self, capacity: int) -> set[tuple[int]]:
        """ Returns tuples of overlaps, with the indices of overlapping jobs at a certain timestep. """
        current_time = 0
        overlapping_jobs = set()
        running_jobs_id = set()
        running = list()

        for job in self.get_sorted_jobs():
            current_time = max(current_time, job.arrival)  # Update the time only when it advances
            if len(running) > capacity and running and running[0][0] <= current_time:
                # Add jobs to constraint only at peak (before removing)
                running_jobs_id_list = list(running_jobs_id)
                running_jobs_id_list.sort()
                overlapping_jobs.add(tuple(running_jobs_id_list))
            while running and running[0][0] <= current_time:
                to_remove = heappop(running)[1]  # Remove jobs that have finished from the running list
                running_jobs_id.remove(to_remove.index)
            heappush(running, (job.arrival + job.duration, job))
            running_jobs_id.add(job.index)
        if len(running) > capacity:  # Check if last timestep is a peak
            running_jobs_id_list = list(running_jobs_id)
            running_jobs_id_list.sort()
            overlapping_jobs.add(tuple(running_jobs_id_list))
        logging.info("Computed overlaps when n_jobs > capacity. {} constraints found".format(len(overlapping_jobs)))
        return overlapping_jobs

    def load_per_time(self) -> dict[int, int]:
        """ Returns number of jobs overlapping per unit of time. """
        current_time = 0
        overlapping_count = dict()
        jobs = list()
        running = set()

        for job in self.get_sorted_jobs():
            heappush(jobs, (job.arrival, True, job))

        while jobs:
            current_time = max(current_time, jobs[0][0])
            if not jobs[0][1]:  # jobs[0][1] is True if job is starting and False if finishing
                job = heappop(jobs)[2]
                running.remove(job)
            else:
                job = heappop(jobs)[2]
                running.add(job)
                heappush(jobs, (job.arrival + job.duration, False, job))
            overlapping_count[current_time] = len(running)
        return overlapping_count

    @staticmethod
    def merge_solutions(first, second):
        numpy_generator = random.default_rng()
        m = max(first.m, second.m)
        result = Solution(m)
        merged_sol = first.get_sorted_jobs()
        merged_sol.extend(second.get_sorted_jobs())
        jobs = [(j, numpy_generator.integers(0, 2)) for j in merged_sol]
        jobs.sort(key=lambda x: (x[0].arrival, x[0].index, x[1]))  # break ties between solutions randomly

        for idx, job in enumerate(jobs):
            result.add_job(Job(idx, job[0].arrival, job[0].duration, job[0].fare_class))
        return result

    def __len__(self):
        return self.number_of_jobs
