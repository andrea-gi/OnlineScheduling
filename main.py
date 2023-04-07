import sys

from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import logging
from OnlineScheduling.plot import print_competitive_ratio_different_scenarios
from datetime import datetime
import pickle


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

    values = list(map(lambda x: (x[0].get_value(fare_values), x[1].get_value(fare_values)), solutions))
    for v in values:
        print(v[0] / v[1])
    return values


if __name__ == '__main__':
    now = datetime.now()
    date_time = now.strftime("%d%m%Y-%H%M%S")
    logging.basicConfig(filename='OnlineScheduling.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    numpy_generator = random.default_rng()

    fares = [100, 80, 60, 40, 20]
    capacity = (50, 50, 50)
    job_number = (1000, 2000, 8000)
    sequences_number = (1, 1, 1)
    min_l = (262800, 262800, 262800)
    max_l = (525600, 525600, 525600)
    t = 2
    arrival = (t*525600, t*525600, t*525600)

    npl = GreedyAlgorithm.npl_optimal(capacity[0], fares)
    greedy = GreedyAlgorithm(capacity[0], npl)
    opt = OptimalSolver(capacity[0], fares)
    values = list()
    for i in range(len(min_l)):
        my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers, 0, arrival[i]),
                               length=(numpy_generator.integers, min_l[i], max_l[i]),
                               fare_class=(numpy_generator.integers, 0, len(fares)))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number[i], job_number[i])
        values.append(compare_algorithms(random_jobs_sequences, fares, greedy, opt))

    f = open("solution_data_"+date_time, "wb")
    pickle.dump(values, f)

    print_competitive_ratio_different_scenarios({"Few jobs": values[0], "Some jobs": values[1], "Many jobs": values[2]},
                                                GreedyAlgorithm.cr_lower_bound(fares, min_l[0], max_l[0]))
