from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from heapq import heappush, heappop


class GreedyAlgorithm(Simulator):
    def __init__(self, capacity, npl):
        super().__init__(capacity)
        self.npl = npl
        self.running = list()  # min heap of job still running, sorted by finishing time
        self.jobs_running_per_class = [0 for _ in range(len(npl))]
        self.currentTime = 0

    def process_input(self, input_sequence: Solution) -> Solution:
        input_jobs = input_sequence.get_sorted_jobs()
        solution = Solution(input_sequence.m)
        for job in input_jobs:
            self.currentTime = max(self.currentTime, job.arrival)
            while self.running and self.running[0][0] <= self.currentTime:
                finished_job = heappop(self.running)[1]
                self.jobs_running_per_class[finished_job.fare_class] -= 1

            current_load = sum(self.jobs_running_per_class)
            satisfies_npl = True
            for idx, partial in enumerate(self.jobs_running_per_class[:job.fare_class+1]):
                satisfies_npl = satisfies_npl and current_load < self.npl[idx]
                current_load -= partial

            if satisfies_npl:
                solution.add_job(job)
                heappush(self.running, (job.arrival + job.duration, job))
                self.jobs_running_per_class[job.fare_class] += 1

        return solution
