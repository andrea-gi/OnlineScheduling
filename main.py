import sys

from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import logging
from OnlineScheduling.plot import plot_competitive_ratio, plot_revenue
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
        print(v[0], v[1], v[0] / v[1])
    return values, solutions


def competitive_ratio_job_number(job_number: tuple,
                                 fares=(100, 80, 60, 40, 20),
                                 capacity=50,
                                 sequences_number=10,
                                 min_l=262800,
                                 max_l=525600,
                                 arrival=2102400,
                                 time='0',
                                 title='Competitive ratio as a function of $N$'):
    npl = GreedyAlgorithm.npl_optimal(capacity, fares)
    greedy = GreedyAlgorithm(capacity, npl)
    opt = OptimalSolver(capacity, fares)
    values = list()
    print_input = dict()
    for i in range(len(job_number)):
        my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l),
                               fare_class=(numpy_generator.integers, 0, len(fares)))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number[i])
        values.append(compare_algorithms(random_jobs_sequences, fares, greedy, opt))
        print_input["{} jobs".format(job_number[i])] = values[-1][0]

    file = open("solution_data_" + date_time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_competitive_ratio(print_input,
                           GreedyAlgorithm.cr_lower_bound(fares, min_l, max_l),
                           time,
                           title)


def revenue_fares(job_number: int,
                  fares=((100, 80, 60, 40, 20),),
                  capacity=50,
                  sequences_number=10,
                  min_l=262800,
                  max_l=525600,
                  arrival=2102400,
                  time='0',
                  title='Competitive ratio as a function of $N$'):
    greedy = list()
    # opt = list()
    for fare in fares:
        greedy.append(GreedyAlgorithm(capacity, GreedyAlgorithm.npl_optimal(capacity, fare)))
        # opt.append(OptimalSolver(capacity, fare))
    values = list()
    print_input = dict()
    for i in range(len(fares)):
        values.append(list())
        my_gen = TaskGenerator(len(fares[i]), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l),
                               fare_class=(numpy_generator.integers, 0, len(fares[i])))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number)
        for input_seq in random_jobs_sequences:
            sol = greedy[i].process_input(input_seq)
            values[-1].append(sol.get_value(fares[i]))
        print_input["{}".format(fares[i])] = values[-1]

    file = open("solution_data_fares" + date_time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_revenue(print_input,
                 time,
                 title)


def revenue_fares_different_demand(job_number: int,
                  fares=((100, 80, 60, 40, 20),),
                  capacity=50,
                  sequences_number=10,
                  min_l=262800,
                  max_l=525600,
                  arrival=2102400,
                  time='0',
                  title='Competitive ratio as a function of $N$'):
    greedy = list()
    # opt = list()
    for fare in fares:
        greedy.append(GreedyAlgorithm(capacity, GreedyAlgorithm.npl_optimal(capacity, fare)))
        # opt.append(OptimalSolver(capacity, fare))
    values = list()
    print_input = dict()
    for i in range(len(fares)):
        values.append(list())
        my_gen = TaskGenerator(len(fares[i]), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l),
                               fare_class=(numpy_generator.integers, 0, len(fares[i])))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number)
        for input_seq in random_jobs_sequences:
            sol = greedy[i].process_input(input_seq)
            values[-1].append(sol.get_value(fares[i]))
        print_input["{}".format(fares[i])] = values[-1]

    file = open("solution_data_fares" + date_time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_revenue(print_input,
                 time,
                 title)

if __name__ == '__main__':
    now = datetime.now()
    date_time = now.strftime("%d%m%Y-%H%M%S")
    logging.basicConfig(filename='OnlineScheduling.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    numpy_generator = random.default_rng()

    ex_fares = [100, 80, 60, 40, 20]
    ex_capacity = (50, 50, 50)
    ex_job_number = (1000, 2000, 8000)
    ex_sequences_number = 50
    ex_min_l = 262800
    ex_max_l = 525600
    ex_arrival = 4 * 525600

    # competitive_ratio_job_number((100, 200, 300, 400, 500), time=date_time)
    revenue_fares(400, ((100,), (100, 20), (100, 60, 20), (100, 80, 60, 40, 20), (100, 90, 80, 70, 60, 50, 40, 30, 20)))
