from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.job import Job
from OnlineScheduling.optimal_solver import OptimalSolver
from OnlineScheduling.solution import Solution
from OnlineScheduling.task_generator import TaskGenerator
from numpy import random
import pickle

if __name__ == '__main__':
    # sequence = open("sequence", "rb")
    # greedy_file = open("greedy", "rb")
    # optimal_file = open("opt", "rb")
    numpy_generator = random.default_rng()

    # random_jobs = pickle.load(sequence)
    # greedy_solution = pickle.load(greedy_file)
    # opt_solution = pickle.load(optimal_file)

    fares = list(numpy_generator.integers(low=10, high=100, size=5))
    fares.sort(reverse=True)
    npl = GreedyAlgorithm.npl_converter((8, 4, 6, 10, 2))
    min_l = 262800
    max_l = 525600

    my_gen = TaskGenerator(5, arrival=(numpy_generator.integers, 0, 525600),
                           length=(numpy_generator.integers, min_l, max_l),
                           fare_class=(numpy_generator.integers, 0, 5))
    random_jobs = my_gen.generate_jobs(1000)

    greedy = GreedyAlgorithm(npl[0], npl)
    greedy_solution = greedy.process_input(random_jobs)

    opt = OptimalSolver(npl[0], fares)
    opt_solution = opt.process_input(random_jobs)

    is_sol = greedy_solution.verify_solution(npl[0])
    is_opt = opt_solution.verify_solution(npl[0])
    print(is_sol, is_opt)
    print("Greedy value: {}\n"
          "Opt value: {}\n"
          "Ratio: {}\n".format(greedy_solution.get_value(fares),
                                opt_solution.get_value(fares),
                                greedy_solution.get_value(fares)/opt_solution.get_value(fares)))

    # pickle.dump(random_jobs, sequence)
    # pickle.dump(greedy_solution, greedy_file)
    # pickle.dump(opt_solution, optimal_file)

    jobs = [
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 5, 1),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
        (0, 10, 0),
    ]

    # input_jobs = [Job(i, a[0], a[1], a[2]) for i, a in enumerate(jobs)]
    # sequence = Solution(2, input_jobs)
    # greedy = GreedyAlgorithm(10, (10, 6))
    # solution = greedy.process_input(sequence)
    # opt = OptimalSolver(10, [10, 8])
    # opt_sol = opt.process_input(sequence)
