import sys

from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.job import Job
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.simulator import Simulator
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import logging
from OnlineScheduling.plot import plot_competitive_ratio, plot_revenue, plot_lb_cr, plot_length_ratio_comparison, \
    plot_jobs_per_time
from datetime import datetime
import pickle


def find_fares_scenarios(min_f, max_f, parts):
    if parts == 2:
        t = [max_f, min_f]
        return tuple(t), tuple(t), tuple(t)
    mid = (min_f + max_f) / 2
    parts -= 2
    high_skewed = tuple(reversed([min_f] + [mid + x * (max_f - mid) / parts for x in range(parts + 1)]))
    uniform = tuple(reversed([min_f + x * (max_f - min_f) / (parts + 1) for x in range(parts + 2)]))
    low_skewed = tuple(reversed([min_f + x * (mid - min_f) / parts for x in range(parts + 1)] + [max_f]))
    return high_skewed, uniform, low_skewed


def compare_algorithms(input_sequences: list[Solution],
                       fare_values: tuple[float],
                       simulator_1: Simulator,
                       simulator_2: Simulator):
    solutions = list()
    for idx, input_sequence in enumerate(input_sequences):
        logging.info("Comparing {} and {}, input sequence {}".format(simulator_1, simulator_2, idx))
        sol_1 = simulator_1.process_input(input_sequence)
        sol_2 = simulator_2.process_input(input_sequence)
        solutions.append((sol_1, sol_2))

    values = list(map(lambda x: (x[0].get_value(fare_values), x[1].get_value(fare_values)), solutions))
    for v in values:
        print(v[0], v[1], v[0] / v[1])
    return values, solutions


def worst_case(job_number: tuple, fares: tuple, capacity: int, min_l: int, max_l: int, arrival: int,
               sequences_number: int, time: str, title="Difficult input sequence"):
    m = len(fares)
    npl = GreedyAlgorithm.npl_optimal(capacity, fares)
    greedy = GreedyAlgorithm(capacity, npl)
    opt = OptimalSolver(capacity, fares)

    values = list()
    print_input = dict()
    for job_n in job_number:
        input_sequences = [Solution(m) for _ in range(sequences_number)]
        for i in range(3 * m):
            if i < m:
                my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers,
                                                            3000 * i, 3000 * (i + 1)),
                                       length=(numpy_generator.integers, min_l + 5000, min_l + 20000),
                                       fare_class=(numpy_generator.integers, m - i - 1, m - i))
                sequences = my_gen.generate_jobs(sequences_number, job_n)
            elif i < 2 * m:
                my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers,
                                                            3000 * i, 3000 * (i + 1)),
                                       length=(numpy_generator.integers, min_l + 50, min_l + 200),
                                       fare_class=(numpy_generator.integers, 2 * m - i - 1, 2 * m - i))
                sequences = my_gen.generate_jobs(sequences_number, job_n)
            else:
                my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers,
                                                            min_l + 700 * (i - m), min_l + 700 * (i - m + 1)),
                                       length=(numpy_generator.integers, max_l - 10000, max_l + 1),
                                       fare_class=(numpy_generator.integers, 3 * m - i - 1, 3 * m - i))
                sequences = my_gen.generate_jobs(sequences_number, job_n)
            for j in range(sequences_number):
                input_sequences[j] = Solution.merge_solutions(input_sequences[j], sequences[j])
                # if j == sequences_number - 1 and i == (3 * m) - 1:
                #     plot_jobs_per_time(input_sequences[j], capacity, time)
        values.append(compare_algorithms(input_sequences, fares, greedy, opt))
        print_input[str(job_n * m * 3)] = values[-1][0]

    file = open("solution_data_difficult_input" + time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_competitive_ratio(print_input,
                           GreedyAlgorithm.cr_lower_bound(fares, min_l, max_l),
                           time,
                           title,
                           x_label="Number of jobs")


def competitive_ratio_job_number(job_number: tuple,
                                 fares=(100, 80, 60, 40, 20),
                                 capacity=50,
                                 sequences_number=10,
                                 min_l=262800,
                                 max_l=525600,
                                 arrival=2102400,
                                 time='0',
                                 title='Competitive ratio as a function of N, uniform distribution'):
    npl = GreedyAlgorithm.npl_optimal(capacity, fares)
    greedy = GreedyAlgorithm(capacity, npl)
    opt = OptimalSolver(capacity, fares)
    values = list()
    print_input = dict()
    for i in range(len(job_number)):
        my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l + 1),
                               fare_class=(numpy_generator.integers, 0, len(fares)))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number[i])
        values.append(compare_algorithms(random_jobs_sequences, fares, greedy, opt))
        print_input[str(job_number[i])] = values[-1][0]

    file = open("solution_data_" + time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_competitive_ratio(print_input,
                           GreedyAlgorithm.cr_lower_bound(fares, min_l, max_l),
                           time,
                           title,
                           x_label="Number of jobs")


def competitive_ratio_fare_distribution(job_number: tuple,
                                        fares=(100, 80, 60, 40, 20),
                                        capacity=50,
                                        sequences_number=10,
                                        min_l=262800,
                                        max_l=525600,
                                        arrival=2102400,
                                        time='0',
                                        title='Competitive ratio as a function of N, non uniform distribution'):
    def choice_wrapper(size):
        return numpy_generator.integers(low=0, high=len(fares), size=size)
        p = [0.0 for _ in range(len(fares))]
        p[0] = 1 / ((len(fares) * (len(fares) + 1)) / 2)
        for idx in range(1, len(p)):
            p[idx] = p[0] * (idx + 1)
        p = p[::-1]
        return numpy_generator.choice(a=len(fares), p=p, size=size)

    npl = GreedyAlgorithm.npl_optimal(capacity, fares)
    greedy = GreedyAlgorithm(capacity, npl)
    opt = OptimalSolver(capacity, fares)
    values = list()
    print_input = dict()
    for i in range(len(job_number)):
        my_gen = TaskGenerator(len(fares), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l + 1),
                               fare_class=(choice_wrapper,))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number[i])
        values.append(compare_algorithms(random_jobs_sequences, fares, greedy, opt))
        print_input[str(job_number[i])] = values[-1][0]

    file = open("solution_data_distribution" + time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_competitive_ratio(print_input,
                           GreedyAlgorithm.cr_lower_bound(fares, min_l, max_l),
                           time,
                           title,
                           x_label="Number of jobs")


def revenue_fares(job_number: int,
                  fares=((100, 80, 60, 40, 20),),
                  capacity=50,
                  sequences_number=10,
                  min_l=262800,
                  max_l=525600,
                  arrival=2102400,
                  time='0',
                  title='Revenue with different fares',
                  x_label_ticks=None):
    def choice_wrapper(idx, size):
        fare = fares[idx]
        return numpy_generator.integers(low=0, high=len(fare), size=size)
        p = [0.0 for _ in range(len(fare))]
        p[0] = 1 / ((len(fare) * (len(fare) + 1)) / 2)
        for idx in range(1, len(p)):
            p[idx] = p[0] * (idx + 1)
        # p = p[::-1]
        return numpy_generator.choice(a=len(fare), p=p, size=size)

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
                               length=(numpy_generator.integers, min_l, max_l + 1),
                               fare_class=(choice_wrapper, i))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number)
        for input_seq in random_jobs_sequences:
            sol = greedy[i].process_input(input_seq)
            values[-1].append(sol.get_value(fares[i]))
        print_input["{}".format(fares[i])] = values[-1]

    file = open("solution_data_fares" + date_time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_revenue(print_input,
                 time,
                 title,
                 x_label_ticks=x_label_ticks)


def cr_fares(job_number: int,
             fares=((100, 80, 60, 40, 20),),
             capacity=50,
             sequences_number=10,
             min_l=262800,
             max_l=525600,
             arrival=2102400,
             time='0',
             title='Revenue with different fares',
             x_label_ticks=()):
    def choice_wrapper(idx, size):
        fare = fares[idx]
        return numpy_generator.integers(low=0, high=len(fare), size=size)
        p = [0.0 for _ in range(len(fare))]
        p[0] = 1 / ((len(fare) * (len(fare) + 1)) / 2)
        for idx in range(1, len(p)):
            p[idx] = p[0] * (idx + 1)
        # p = p[::-1]
        return numpy_generator.choice(a=len(fare), p=p, size=size)

    greedy = list()
    opt = list()
    for fare in fares:
        greedy.append(GreedyAlgorithm(capacity, GreedyAlgorithm.npl_optimal(capacity, fare)))
        opt.append(OptimalSolver(capacity, fare))
    values = list()
    print_input = dict()
    for i, fare in enumerate(fares):
        values.append(list())
        my_gen = TaskGenerator(len(fare), arrival=(numpy_generator.integers, 0, arrival),
                               length=(numpy_generator.integers, min_l, max_l + 1),
                               fare_class=(choice_wrapper, i))
        random_jobs_sequences = my_gen.generate_jobs(sequences_number, job_number)
        for input_seq in random_jobs_sequences:
            sol = greedy[i].process_input(input_seq)
            sol_opt = opt[i].process_input(input_seq)
            values[-1].append((sol.get_value(fares[i]), sol_opt.get_value(fare)))
        print_input["{}".format(fare)] = values[-1]

    file = open("solution_data_fares" + date_time + ".simdata", "wb")
    pickle.dump(values, file)

    plot_competitive_ratio(print_input,
                           None,
                           time,
                           title,
                           x_label_ticks=x_label_ticks,
                           x_label="Fares")


if __name__ == '__main__':
    now = datetime.now()
    date_time = now.strftime("%d%m%Y-%H%M%S")
    logging.basicConfig(filename='OnlineScheduling.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    numpy_generator = random.default_rng()

    ex_fares = (100, 80, 60, 40, 20)
    ex_capacity = (50, 50, 50)
    ex_job_number = (1000, 2000, 8000)
    ex_sequences_number = 50
    ex_min_l = 262800
    ex_max_l = 525600
    ex_arrival = 4 * 525600
    find_fares_scenarios(40, 200, 5)
    # plot_length_ratio_comparison()
    plot_lb_cr(40, 400, ex_min_l, ex_max_l, 30)
    job_numbers = (300, 600, 900, 1200, 1500, 1800, 2100)
    # worst_case((3, 4, 5, 6, 15, 20, 30, 50, 150, 250, 500), ex_fares, 50, ex_min_l, ex_max_l, ex_arrival, 25, date_time)
    # competitive_ratio_fare_distribution(job_numbers, time=date_time)
    # competitive_ratio_job_number(job_numbers, fares=(10, 7.5, 5), sequences_number=2, time=date_time)
    # competitive_ratio_job_number(job_numbers, fares=(10, 5), sequences_number=2, time=date_time)
    # competitive_ratio_job_number(job_numbers, fares=(10,), capacity=50, min_l=ex_min_l, max_l=ex_min_l*2, arrival=(ex_min_l*3), sequences_number=20, time=date_time)
    #
    # revenue_fares(1000, ((200, 40),
    #                      (200, 120, 40),
    #                      (200, 160, 120, 80, 40),
    #                      (200, 180, 160, 140, 120, 100, 80, 60, 40)
    #                      ), sequences_number=10, time=date_time, x_label_ticks=(2, 3, 5, 9))

    fares_input = {"skewed low": list(), "uniform": list(), "skewed high": list()}

    for i in (2, 3, 5, 9):
        scenario_high, scenario_uniform, scenario_low = find_fares_scenarios(40, 400, i)
        fares_input["skewed high"].append(scenario_high)
        fares_input["uniform"].append(scenario_uniform)
        fares_input["skewed low"].append(scenario_low)
    fares_input["skewed high"] = tuple(fares_input["skewed high"])
    fares_input["uniform"] = tuple(fares_input["uniform"])
    fares_input["skewed low"] = tuple(fares_input["skewed low"])

    for input_type in fares_input:
        cr_fares(600, fares_input[input_type], capacity=50,
                 sequences_number=50, title="Value ratio with different fares, {}".format(input_type), time=date_time,
                 x_label_ticks=(2, 3, 5, 9))

    # cr_fares(1000, ((200, 40),
    #                 (200, 120, 40),
    #                 (200, 160, 120, 80, 40),
    #                 (200, 180, 160, 140, 120, 100, 80, 60, 40)
    #                 ), time=date_time, x_label_ticks=(2, 3, 5, 9))
