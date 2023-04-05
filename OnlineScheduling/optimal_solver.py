import logging

from pulp import LpProblem, LpVariable, LpMaximize, lpSum

from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution


class OptimalSolver(Simulator):
    def __init__(self, capacity, fares):
        super(OptimalSolver, self).__init__(capacity)
        self.fares = fares

    @staticmethod
    def find_overlaps(input_sequence: Solution) -> list[list[int]]:
        """ Finds indices of jobs that overlap with every job in the input sequence.
            Element i of output is a list of indices of jobs that have index j>i that overlap with job i. """
        jobs = input_sequence.get_sorted_jobs()
        overlaps = [list() for _ in range(len(jobs))]
        for idx, job in enumerate(jobs):
            for other in jobs[idx+1:]:
                if job.overlap(other) and job != other:
                    overlaps[job.index].append(other.index)
        return overlaps

    def process_input(self, input_sequence: Solution) -> Solution:
        logging.debug("Starting {}".format(self))
        overlaps = input_sequence.overlap_times(self.capacity)
        job_values = [self.fares[j.fare_class] * j.duration for j in input_sequence.get_sorted_jobs()]

        model = LpProblem("OnlineScheduling", LpMaximize)

        J = [LpVariable("j_{i}".format(i=idx), lowBound=0, upBound=1, cat="Integer") for idx in range(len(input_sequence))]
        overlaps_variables = [list() for _ in range(len(overlaps))]
        for idx, job in enumerate(overlaps):
            overlaps_variables[idx] = list(map(lambda x: J[x], job))  # Translate overlaps into LP variables

        model += lpSum([J[i]*job_values[i] for i in range(len(job_values))])  # Objective function

        logging.debug("Adding constraints to the model.")
        for idx, overlap in enumerate(overlaps_variables):
            model += lpSum(overlap) <= self.capacity  # LP constraints

        if overlaps:
            model.solve()

        solution = Solution(input_sequence.m)
        for idx, var in enumerate(J):
            if var.value() == 1 or not overlaps:
                solution.add_job(input_sequence.get_sorted_jobs()[idx])  # Add jobs found by LP to output solution

        is_sol = solution.verify_solution(self.capacity)
        if is_sol:
            logging.debug("Solution found by {} is valid.".format(self))
        else:
            logging.error("Solution found by {} does not satisfy the capacity constraint {}"
                          .format(self, self.capacity))
        return solution

    def __str__(self):
        return "OptimalSolver"
