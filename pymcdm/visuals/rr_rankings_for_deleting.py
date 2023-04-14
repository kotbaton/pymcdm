import numpy as np
import matplotlib.pyplot as plt
import pymcdm as pm

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
