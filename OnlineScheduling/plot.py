import matplotlib.pyplot as plt
import numpy as np


def print_competitive_ratio_different_scenarios(values_per_scenario: dict[str, list[tuple]], lower_bound):

    computed_ratio_per_scenario = {k: list(map(lambda x: x[0]/x[1], v)) for k, v in values_per_scenario.items()}
    mean_ratio = {k: np.mean(v) for k, v in computed_ratio_per_scenario.items()}
    std_dev_ratio = {k: np.std(v) for k, v in computed_ratio_per_scenario.items()}
    x_pos = np.arange(len(mean_ratio))

    # Build the plot
    fig, ax = plt.subplots()
    ax.bar(x_pos, list(mean_ratio.values()), yerr=list(std_dev_ratio.values()), align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Mean ratio between ($v_{\mathcal{A}}$) and ($v_{Opt}$)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(list(mean_ratio.keys()))
    ax.set_title('Competitive ratio')
    ax.axhline(y=lower_bound)
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')
    plt.show()

