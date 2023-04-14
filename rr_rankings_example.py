import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pymcdm as pm

def rankings_flow_correlation(rankings,
                              correlations,
                              labels,
                              correlation_name='Correlation',
                              correlation_ax_size="25%",
                              correlation_plot_kwargs=dict(),
                              ranking_flows_kwargs=dict(),
                              ax=None):
    if ax is None:
        ax = plt.gca()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("top", size=correlation_ax_size, pad=0.05)

    pm.visuals.correlation_plot(correlations, ylabel=correlation_name, labels=labels, **correlation_plot_kwargs, ax=cax)
    cax.tick_params(bottom=False, labelbottom=False)

    pm.visuals.ranking_flows(rankings, labels, **ranking_flows_kwargs, ax=ax)

    return ax, cax


matrix = np.array([
    [3, 2, 4, 5, 1],
    [1, 9, 3, 4, 2],
    [5, 2, 3, 6, 1],
    [4, 6, 3, 7, 1],
    [3, 5, 4, 5, 1]
])

topsis = pm.methods.TOPSIS()
weights = np.ones(5)/5
types = np.ones(5)

args = pm.helpers.leave_one_out_rr(topsis, matrix, weights, types, pm.correlations.weighted_spearman, only_rr=False)

fig, ax = plt.subplots(figsize=(8, 4))
rankings_flow_correlation(*args,
                          ax=ax)
plt.tight_layout()
plt.show()
