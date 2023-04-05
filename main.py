import sys

from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import logging


def compare_algorithms(input_sequences: list[Solution],
                       fare_values: list[float],
                       task_generator_1: Simulator,
                       task_generator_2: Simulator):
    solutions = list()
    for idx, input_sequence in enumerate(input_sequences):
        logging.info("Comparing {} and {}, input sequence {}".format(task_generator_1, task_generator_2, idx))
        sol_1 = task_generator_1.process_input(input_sequence)
        sol_2 = task_generator_2.process_input(input_sequence)
        solutions.append((sol_1, sol_2))

    values = map(lambda x: (x[0].get_value(fare_values), x[1].get_value(fare_values)), solutions)
    for v in values:
        print(v[0]/v[1])


if __name__ == '__main__':
    logging.basicConfig(filename='OnlineScheduling.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    numpy_generator = random.default_rng()

    capacity = 10
    job_number = 5000
    sequences_number = 10
    fares = [100, 80, 60, 40, 20]
    min_l = 262800
    max_l = 525600

    npl = GreedyAlgorithm.npl_optimal(capacity, fares)
    my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers, 0, 525600),
                           length=(numpy_generator.integers, min_l, max_l),
                           fare_class=(numpy_generator.integers, 0, 5))
    random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number)

    greedy = GreedyAlgorithm(capacity, npl)
    opt = OptimalSolver(capacity, fares)

    compare_algorithms(random_jobs_sequences, fares, greedy, opt)
