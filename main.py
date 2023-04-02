from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.job import Job
from OnlineScheduling.solution import Solution

if __name__ == '__main__':
    jobs = [(0, 5, 1),
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
            (4, 5, 1),
            (4, 5, 1),
            (4, 5, 1),
            (4, 5, 1),
            (4, 5, 1),
            (4, 5, 0),
            (4, 5, 0),
            (4, 5, 0),
            (4, 5, 0),
            ]

    input_jobs = [Job(i, a[0], a[1], a[2]) for i, a in enumerate(jobs)]
    sequence = Solution(2, input_jobs)
    greedy = GreedyAlgorithm(10, (10, 6))
    solution = greedy.process_input(sequence)
    print(solution)
