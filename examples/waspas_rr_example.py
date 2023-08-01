import numpy as np
import matplotlib.pyplot as plt
import pymcdm as pm

# Ensure the same result each time
np.random.seed(1)

# Generate random decision matrix with 10 alternatives and 4 criteria
matrix = np.random.rand(10, 4)
# Set equal weights for all of the criteria
weights = pm.weights.equal_weights(matrix)
# Types of the criteria: two profit and two cost criteria
types = np.array([1, 1, -1, -1])

# Create method's object
waspas = pm.methods.WASPAS()

# Use leave_one_out function to produce the input for the visualization
# in order to analyse rank reversal for this particular case
rankings, corr, labels = pm.helpers.leave_one_out_rr(
        method=waspas, matrix=matrix, weights=weights, types=types,
        corr_function=pm.correlations.weighted_spearman,
        only_rr=False)

# Create the visualization of the changes in the rankings.
# kwargs are used to tweak the appearense of the visualization.
fig, ax = plt.subplots(figsize=(8, 3.8))
ax, cax = pm.visuals.rankings_flow_correlation(
        rankings=rankings, correlations=corr, labels=labels,
        correlation_plot_kwargs=dict(space_multiplier=0.15),
        ranking_flows_kwargs=dict(better_grid=True),
        ax=ax)
cax.set_ylim(0.75, 1.05)
plt.tight_layout()
plt.show()
