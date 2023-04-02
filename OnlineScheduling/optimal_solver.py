from pulp import *

from OnlineScheduling.job import Job
from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution


class OptimalSolver(Simulator):
    @staticmethod
    def find_overlaps(input_sequence: Solution) -> dict[Job, list[Job]]:
        """ Only finds overlap in the future. """
        jobs = input_sequence.get_sorted_jobs()
        overlaps = dict()
        for idx, job in enumerate(jobs):
            overlaps[job] = list()
            for other in jobs[idx+1:]:
                if job.overlap(other):
                    overlaps[job].append(other)
                else:
                    break
        return overlaps

    def process_input(self, input_sequence: Solution) -> Solution:
        model = LpProblem("OnlineScheduling", LpMaximize)
