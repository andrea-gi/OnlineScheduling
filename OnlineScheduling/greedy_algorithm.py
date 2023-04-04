from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from heapq import heappush, heappop


class GreedyAlgorithm(Simulator):
    def __init__(self, capacity, npl):
        super().__init__(capacity)
        self.npl = npl

    def process_input(self, input_sequence: Solution) -> Solution:
        input_jobs = input_sequence.get_sorted_jobs()
        solution = Solution(input_sequence.m)

        running = list()
        jobs_running_per_class = [0 for _ in range(len(self.npl))]
        current_time = 0

        for job in input_jobs:
            current_time = max(current_time, job.arrival)  # Update the time only when it advances
            while running and running[0][0] <= current_time:
                finished_job = heappop(running)[1]  # Remove jobs that have finished from the running list
                jobs_running_per_class[finished_job.fare_class] -= 1

            current_load = sum(jobs_running_per_class)
            satisfies_npl = True
            for idx, partial in enumerate(jobs_running_per_class[:job.fare_class+1]):
                if current_load >= self.npl[idx]:
                    satisfies_npl = False
                    break
                current_load -= partial

            if satisfies_npl:
                solution.add_job(job)
                heappush(running, (job.arrival + job.duration, job))
                jobs_running_per_class[job.fare_class] += 1

        return solution

    @staticmethod
    def npl_converter(npl_distinct):
        npl_cumulative = [0 for _ in range(len(npl_distinct))]
        npl_cumulative[0] = sum(npl_distinct)
        for i in range(1, len(npl_distinct)):
            npl_cumulative[i] = npl_cumulative[i-1] - npl_distinct[i-1]
        return npl_cumulative
