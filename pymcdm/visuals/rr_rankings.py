import numpy as np
import matplotlib.pyplot as plt
import pymcdm as pm


def calculate_rr_rankings(method, matrix, weights, types,
                          corr_function=pm.correlations.weighted_spearman,
                          only_rr=True):
    pref = method(matrix, weights, types)
    true_rank = method.rank(pref)

    rr_ranks = [(None, true_rank)]
    corr_values = [1.0]

    for i in range(matrix.shape[0]):
        indices = list(range(i)) + list(range(i + 1, matrix.shape[0]))

        matrix1 = matrix[indices]

        pref = method(matrix, weights, types)[indices]
        pref1 = method(matrix1, weights, types)

        rank = method.rank(pref)
        rank1 = method.rank(pref1)

        cr = corr_function(rank, rank1)
        rank1 = list(rank1)
        rank1.insert(i, 0)

        if only_rr:
            if cr != 1:
                rr_ranks.append((i, rank1))
                corr_values.append(cr)
        else:
            rr_ranks.append((i, rank1))
            corr_values.append(cr)

    rr_ranks.append((None, true_rank))
    removed_alts, rankings = zip(*rr_ranks)
    labels = [f'w/o $A_{{{i + 1}}}$' if i is not None else 'None' for i in removed_alts]
    corr_values.append(1.0)

    return labels, corr_values, np.array(rankings)


def rr_rankins_flows(rankings,
                     labels,
                     alt_indices=None,
                     spacing=0.1,
                     colors=None,
                     ax=None):
    if ax is None:
        ax = plt.gca()

    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    color_picker = np.zeros(rankings.shape[1], dtype='int')
    color_picker[np.argsort(rankings[0])] = np.arange(rankings.shape[1], dtype='int')

    rankings = np.array(rankings)

    if alt_indices is None:
        alt_indices = range(rankings.shape[1])

    for ai in range(rankings.shape[1]):
        lines_before = []
        lines_after = []
        markers = []
        lines = lines_before

        for i in range(rankings.shape[0]):
            if rankings[i, ai] != 0:
                lines.append((i - spacing, rankings[i, ai]))
                lines.append((i + spacing, rankings[i, ai]))
                markers.append((i, rankings[i, ai]))
            else:
                lines = lines_after

        c = colors[color_picker[ai] % len(colors)]
        if lines_before:
            ax.plot(*zip(*lines_before), c=c)

        if lines_after:
            ax.plot(*zip(*lines_after), c=c)

        if lines_before and lines_after:
            ax.plot(*zip(*[lines_before[-1], lines_after[0]]),
                        linestyle='--', alpha=0.7, zorder=10, c=c)

        ax.plot(*zip(*markers), c=c, linestyle=' ', marker='o')

        ax.text(- spacing * 1.5,
                rankings[0, ai],
                f'$A_{{{alt_indices[ai] + 1}}}$',
                color=c,
                ha='right', va='center', fontsize=9)
        ax.text(rankings.shape[0] - 1 + spacing * 1.5,
                rankings[-1, ai],
                f'$A_{{{alt_indices[ai] + 1}}}$',
                color=c,
                ha='left', va='center', fontsize=9)

    ax.grid(alpha=0.5, linestyle='--')
    ax.set(
        xticks=range(rankings.shape[0]),
        xticklabels=labels,
        ylabel='Position in ranking',
        yticks=range(1, rankings.shape[1] + 1)
    )


def correlation_plot(cors, labels, ax=None):
    ax.plot(range(len(labels)), cors, lw=1, ls='--', marker='*', markersize=8, color='green')
    ax.fill_between(range(len(labels)), [np.min(cors) - 0.5] * len(labels), cors, color='green', alpha=0.2)

    spacing = max((np.max(cors) - np.min(cors)) * 0.05, 0.05)
    for i, c in enumerate(cors):
        ax.text(i, c - spacing, f'{c:0.3f}', color='green', ha='center', va='top')

    ax.set_ylabel('$r_w$')
    # ax.set_yticks([0.9, 0.95, 1.0])
    # ax.set_ylim([0.9, 1.01])

    ax.grid(ls='--', alpha=0.5)
    ax.set_axisbelow(True)

    ax.tick_params(bottom=False)




if __name__ == '__main__':
    matrix = np.array([
        [3, 2, 4, 5, 1],
        [0, 2, 4, 3, 1],
        [1, 0, 3, 4, 2],
        [3, 2, 0, 6, 1],
        [4, 6, 3, 0, 1],
        [1, 2, 3, 4, 0],
        [3, 2, 4, 5, 1]
    ]).T

    topsis = pm.methods.TOPSIS()
    weights = np.ones(7)/7
    types = np.ones(7)

    labels, cors, rankings = calculate_rr_rankings(topsis, matrix, weights, types, only_rr=True)

    fig, axes = plt.subplots(2, 1, figsize=(5, 3), dpi=200,
                             gridspec_kw={
                                 'height_ratios': [1, 5],
                                 'hspace': 0.01
                             },
                             sharex=True, constrained_layout=True)

    correlation_plot(cors, labels, ax=axes[0])
    rr_rankins_flows(rankings, labels, ax=axes[1])

    plt.show()

    #Przykład 2
    matrix = np.array([
        [1, 2, 3, 4, 5],
        [2, 1, 3, 4, 5],
        [3, 2, 1, 4, 5],
        [4, 2, 3, 1, 5],
        [5, 2, 3, 4, 1]
    ])

    fig, axes = plt.subplots(2, 1, figsize=(5, 3), dpi=200,
                             gridspec_kw={
                                 'height_ratios': [1, 5],
                                 'hspace': 0.01
                             },
                             sharex=True, constrained_layout=True)

    labels = [f'$R_{{{i+1}}}$' for i in range(5)]
    cors = [pm.correlations.rank_similarity_coef(matrix[0], matrix[i])
            for i in range(matrix.shape[0])]

    correlation_plot(cors, labels, ax=axes[0])
    rr_rankins_flows(matrix, labels, ax=axes[1])
    plt.show()

    #Przykład 3
    matrix = np.array([
        [1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4],
        [0, 0, 1, 2, 3],
        [0, 0, 0, 1, 2],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 2],
        [0, 0, 1, 2, 3],
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
    ])

    fig, axes = plt.subplots(2, 1, figsize=(5, 3), dpi=200,
                             gridspec_kw={
                                 'height_ratios': [1, 5],
                                 'hspace': 0.01
                             },
                             sharex=True, constrained_layout=True)

    labels = [f'$R_{{{i+1}}}$' for i in range(matrix.shape[0])]
    cors = [pm.correlations.rank_similarity_coef(matrix[0], matrix[i])
            for i in range(matrix.shape[0])]

    correlation_plot(cors, labels, ax=axes[0])
    rr_rankins_flows(matrix, labels, ax=axes[1])
    plt.show()
