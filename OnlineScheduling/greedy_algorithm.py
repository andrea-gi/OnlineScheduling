from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from heapq import heappush, heappop
import logging
from iteround import saferound


class GreedyAlgorithm(Simulator):
    def __init__(self, capacity, npl):
        super().__init__(capacity)
        self.npl = npl

    def process_input(self, input_sequence: Solution) -> Solution:
        logging.debug("Starting {}".format(self))
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
                # Only need to check classes up to job's class
                if current_load >= self.npl[idx]:
                    satisfies_npl = False
                    break
                current_load -= partial

            if satisfies_npl:
                solution.add_job(job)
                heappush(running, (job.arrival + job.duration, job))
                jobs_running_per_class[job.fare_class] += 1

        is_sol = solution.verify_solution(self.capacity)
        if is_sol:
            logging.debug("Solution found by {} is valid.".format(self))
        else:
            logging.error("Solution found by {} does not satisfy the capacity constraint {}"
                          .format(self, self.capacity))
        return solution

    @staticmethod
    def npl_converter(npl_distinct):
        npl_cumulative = [0 for _ in range(len(npl_distinct))]
        npl_cumulative[0] = sum(npl_distinct)
        for i in range(1, len(npl_distinct)):
            npl_cumulative[i] = npl_cumulative[i-1] - npl_distinct[i-1]
        return npl_cumulative

    @staticmethod
    def npl_optimal(capacity, fares):
        fares = list(fares)
        if len(fares) == 1:
            return [capacity]
        m = len(fares)
        fares.append(0)
        npl = [0 for _ in range(m)]
        delta = m
        for i in range(1, m):
            delta -= fares[i]/fares[i-1]
        for i in range(m):
            npl[i] = capacity/delta * (1 - fares[i+1]/fares[i])
        npl = saferound(npl, 0, topline=capacity)
        for i in range(m):
            npl[i] = int(npl[i])
        assert(sum(npl) == capacity)
        return GreedyAlgorithm.npl_converter(npl)

    @staticmethod
    def cr_lower_bound(fares, min_length, max_length):
        delta = len(fares)
        for i in range(1, len(fares)):
            delta -= fares[i] / fares[i - 1]
        length_ratio = min(min_length/max_length, (min_length+1)/(min_length+max_length))
        return length_ratio/delta

    def __str__(self):
        return "GreedyAlgorithm"
