import matplotlib.pyplot as plt
import numpy as np

from OnlineScheduling.greedy_algorithm import GreedyAlgorithm
from OnlineScheduling.solution import Solution


def plot_revenue(values_per_scenario: dict[str, list[int]], time, title, x_label_ticks=None, x_label=None):
    mean_ratio = {k: np.mean(v) for k, v in values_per_scenario.items()}
    std_dev_ratio = {k: np.std(v) for k, v in values_per_scenario.items()}
    x_pos = np.arange(len(mean_ratio))

    # Build the plot
    fig, ax = plt.subplots()
    ax.bar(x_pos, list(mean_ratio.values()), yerr=list(std_dev_ratio.values()), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Revenue of $v_{\mathcal{A}}$')
    ax.set_xlabel('Fares')
    ax.set_xticks(x_pos)
    ax.set_title(title)
    ax.yaxis.grid(True)
    if x_label_ticks:
        ax.set_xticklabels(x_label_ticks)
    else:
        ax.set_xticklabels(list(mean_ratio.keys()))
    if not x_label_ticks and max([len(x) for x in mean_ratio.keys()]) > 10:
        plt.setp(ax.get_xticklabels(), rotation=15, horizontalalignment='right')
    plt.tight_layout()
    # Save the figure and show
    fig.savefig('{}{}.pdf'.format(title.replace(' ', '_'), time))
    plt.show()


def plot_competitive_ratio(values_per_scenario: dict[str, list[tuple]], lower_bound, time, title, x_label_ticks=None, x_label=None):
    computed_ratio_per_scenario = {k: list(map(lambda x: x[0]/x[1], v)) for k, v in values_per_scenario.items()}
    mean_ratio = {k: np.mean(v) for k, v in computed_ratio_per_scenario.items()}
    std_dev_ratio = {k: np.std(v) for k, v in computed_ratio_per_scenario.items()}
    x_pos = np.arange(len(mean_ratio))

    # Build the plot
    fig, ax = plt.subplots()
    ax.bar(x_pos, list(mean_ratio.values()), yerr=list(std_dev_ratio.values()), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Ratio between ($v_{\mathcal{A}}$) and ($v_{Opt}$)')
    if x_label:
        ax.set_xlabel(x_label)
    ax.set_xticks(x_pos)
    ax.set_ylim([0, 1])
    if x_label_ticks:
        ax.set_xticklabels(x_label_ticks)
    else:
        ax.set_xticklabels(list(mean_ratio.keys()))
    ax.set_title(title)
    if lower_bound:
        ax.axhline(y=lower_bound, color='red', label="Theoretical lower bound")
        ax.legend()
    if not x_label_ticks and max([len(x) for x in mean_ratio.keys()]) > 10:
        plt.setp(ax.get_xticklabels(), rotation=15, horizontalalignment='right')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    fig.savefig('{}_{}.pdf'.format(title.replace(' ', '_'), time))
    plt.show()


def plot_jobs_per_time(solution: Solution, capacity: int, time_step):
    load = solution.load_per_time()
    time, n_jobs = zip(*load.items())

    fig, ax = plt.subplots()
    ax.step(time, n_jobs)
    ax.set_ylabel('Number of jobs')
    ax.set_xlabel('Time step')
    ax.axhline(y=capacity, label="Capacity $n$", color='red')
    ax.set_title('Number of jobs per time step')
    ax.legend()

    plt.ylim(ymax=480)
    plt.xlim(xmin=-0.05 * 262800, xmax=3.5 * 262800)

    plt.tight_layout()
    fig.savefig("n_jobs_time_step_{}.pdf".format(time_step))
    fig.show()


def plot_lb_cr(min_fare: float, max_fare: float, min_l: int, max_l: int, x_points: int):
    x = [i for i in range(1, x_points + 2)]
    D = min(min_l/max_l, (min_l+1)/(min_l+max_l))
    y = [GreedyAlgorithm.cr_lower_bound([D], min_l, max_l)]
    for i in range(1, x_points + 1):
        fare = [max_fare - x * (max_fare - min_fare) / i for x in range(i + 1)]
        y.append(GreedyAlgorithm.cr_lower_bound(fare, min_l, max_l))
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.axhline(y=D, label="Length ratio", color='red')
    ax.set_ylabel('Competitive ratio')
    ax.set_xlabel('Number of fare classes')
    ax.set_title('Theoretical lower bound of competitive ratio')
    ax.legend()

    plt.tight_layout()
    fig.savefig("theoretical_lb_{}_{}_{}.pdf".format(min_fare, max_fare, x_points))
    fig.show()


def plot_length_ratio_comparison():
    x = [i/10000 for i in range(1, 10001)]
    y_1 = list(x)
    y_2 = [i/(i+1) for i in x]
    fig, ax = plt.subplots()
    ax.plot(x, y_1, label="$r$")
    ax.plot(x, y_2, label="$\\frac{r}{r+1}$")
    ax.set_ylabel('Length ratio')
    ax.set_xlabel('r')
    ax.set_title('Approximation of length ratio')
    ax.legend()

    plt.tight_layout()
    fig.savefig("lr_comparison.pdf")
    fig.show()
