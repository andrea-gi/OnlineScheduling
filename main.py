from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.job import Job
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import pickle
import logging


if __name__ == '__main__':
    logging.basicConfig(filename='OnlineScheduling.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # logging.getLogger().addHandler(logging.StreamHandler())

    # sequence = open("sequence", "rb")
    # greedy_file = open("greedy", "rb")
    # optimal_file = open("opt", "rb")
    numpy_generator = random.default_rng()

    # random_jobs = pickle.load(sequence)
    # greedy_solution = pickle.load(greedy_file)
    # opt_solution = pickle.load(optimal_file)

    # fares = list(numpy_generator.integers(low=10, high=100, size=5))
    # fares.sort(reverse=True)
    fares = [100, 80, 60, 40, 20]
    npl = GreedyAlgorithm.npl_optimal(30, fares)
    min_l = 262800
    max_l = 525600

    my_gen = TaskGenerator(5, arrival=(numpy_generator.integers, 0, 10*525600),
                           length=(numpy_generator.integers, min_l, max_l),
                           fare_class=(numpy_generator.integers, 0, 5))
    random_jobs = my_gen.generate_jobs(1000)

    greedy = GreedyAlgorithm(npl[0], npl)
    greedy_solution = greedy.process_input(random_jobs)

    opt = OptimalSolver(npl[0], fares)
    opt_solution = opt.process_input(random_jobs)

    print("Greedy value: {}\n"
          "Opt value: {}\n"
          "Ratio: {}\n".format(greedy_solution.get_value(fares),
                               opt_solution.get_value(fares),
                               greedy_solution.get_value(fares) / opt_solution.get_value(fares)))

    # pickle.dump(random_jobs, sequence)
    # pickle.dump(greedy_solution, greedy_file)
    # pickle.dump(opt_solution, optimal_file)
