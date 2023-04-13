import matplotlib.pyplot as plt
import numpy as np

from OnlineScheduling.solution import Solution


def plot_revenue(values_per_scenario: dict[str, list[int]], time, title):
    mean_ratio = {k: np.mean(v) for k, v in values_per_scenario.items()}
    std_dev_ratio = {k: np.std(v) for k, v in values_per_scenario.items()}
    x_pos = np.arange(len(mean_ratio))

    # Build the plot
    fig, ax = plt.subplots()
    ax.bar(x_pos, list(mean_ratio.values()), yerr=list(std_dev_ratio.values()), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Revenue of ($v_{\mathcal{A}}$)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(list(mean_ratio.keys()))
    ax.set_title(title)
    ax.yaxis.grid(True)

    # Save the figure and show
    fig.savefig('{}{}.pdf'.format(title.replace(' ', '_'), time))
    plt.show()


def plot_competitive_ratio(values_per_scenario: dict[str, list[tuple]], lower_bound, time, title):
    computed_ratio_per_scenario = {k: list(map(lambda x: x[0]/x[1], v)) for k, v in values_per_scenario.items()}
    mean_ratio = {k: np.mean(v) for k, v in computed_ratio_per_scenario.items()}
    std_dev_ratio = {k: np.std(v) for k, v in computed_ratio_per_scenario.items()}
    x_pos = np.arange(len(mean_ratio))

    # Build the plot
    fig, ax = plt.subplots()
    ax.bar(x_pos, list(mean_ratio.values()), yerr=list(std_dev_ratio.values()), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Ratio between ($v_{\mathcal{A}}$) and ($v_{Opt}$)')
    ax.set_xticks(x_pos)
    ax.set_ylim([0, 1])
    ax.set_xticklabels(list(mean_ratio.keys()))
    ax.set_title(title)
    ax.axhline(y=lower_bound, color='red')
    ax.yaxis.grid(True)

    # Save the figure and show
    fig.savefig('{}_{}.pdf'.format(title.replace(' ', '_'), time))
    plt.show()


def plot_jobs_per_time(solution: Solution, capacity: int):
    load = solution.load_per_time()
    time, n_jobs = zip(*load.items())

    fig, ax = plt.subplots()
    ax.step(time, n_jobs)
    ax.set_ylabel('Number of jobs')
    ax.set_xlabel('Time step')
    ax.axhline(y=capacity, label="Capacity $n$", color='red')
    ax.set_title('Number of jobs per time step')
    ax.legend()

    fig.savefig("n_jobs_time_step.pdf")
    fig.show()