import numpy as np
from pymcdm import methods

body = methods.TOPSIS()

matrix = np.array([[1, 2, 5],
                   [3000, 3750, 4500]]).T

weights = np.array([0.5, 0.5])

types = np.array([-1, 1])

output = [0.500, 0.617, 0.500]
output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

res = body(matrix, weights, types, explained_call=True)

for name, array in res:
    print(name, '\n', array, '\n')
