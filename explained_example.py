import numpy as np
import pymcdm as pm

matrix = np.array([
    [5, 0.5, 80],
    [1, 0.2, 30],
    [3, 0.8, 40],
    [4, 0.3, 50]
    ])

weights = pm.weights.equal_weights(matrix)
types = [1, 1, -1]

topsis = pm.methods.TOPSIS()

results = topsis(matrix, weights, types, explained_call=True)

print(results.to_latex(group_tables=False))

