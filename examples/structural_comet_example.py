# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from pymcdm.methods import TOPSIS
from pymcdm.comet_tools import StructuralCOMET, Submodel, MethodExpert

# This is simplified example from the followed paper:
# Shekhovtsov, A., Kołodziejczyk, J., & Sałabun, W. (2020). Fuzzy model
# identification using monolithic and structured approaches in decision
# problems with partially incomplete data. Symmetry, 12(9), 1541.

# Suppose we want to evaluate some electric vechcles
# and define four criteria for them:
criteria_names = ['C_1 Max velocity', 'C_2 Travel range',
                  'C_3 Charging time', 'C_4 Price']

cvalues = [
        [57, 107.3, 150],
        [100, 144, 180],
        [4, 7, 10],
        [12.9, 43.3, 120]
        ]

# We want to group C_1 and C_2 into submodel P_1 and then group P_1 with C_3
# in order to create submodel P_2 and then group P_2 with C_4 to evaluate final
# preferene P.

# Define equal weights for all submodels
weights = np.array([0.5, 0.5])

# For this puprpose we can define StructuralCOMET object in the following way:
model = StructuralCOMET(
        submodels=[
            Submodel(
                name='P_1', # Name the submodel so we could refer to it later
                structure=(0, 1), # We could use indexes to refer to criteria
                cvalues=[0.0, 0.5, 1.0], # Because normally output of the COMET
                                         # is in range [0, 1] it is good idea
                                         # to put cvalues in this range here.
                expert_function=MethodExpert(TOPSIS(), weights, [1, 1])
                ),
            Submodel(
                name='P_2',
                structure=('P_1', 'C_3 Charging time'), # Names also allowed
                cvalues=[0.0, 0.5, 1.0],
                expert_function=MethodExpert(TOPSIS(), weights, [1, -1])
                ),
            Submodel(
                name='P',
                structure=('P_2', 'C_4 Price'),
                cvalues=None, # This is the final model
                              # so we don't need cvalues
                expert_function=MethodExpert(TOPSIS(), weights, [1, -1])
                )
            ],
        cvalues=cvalues,
        criteria_names=criteria_names
        )

# And now we can evaluate some alternatives
alts = np.array([
    [120, 130, 5, 40],
    [100, 180, 8, 60],
    ])

print(model(alts))

# Consider more complex example (full example from the referenced paper)
# This one is used as test case for the StructuralCOMET
cvalues = [
        [340, 909.3, 3000],
        [57, 107.3, 150],
        [100, 144, 180],
        [10, 87.9, 200],
        [80, 325.8, 610],
        [4, 7, 10],
        [10, 54, 120],
        [10.5, 37.57, 99],
        [12.9, 43.3, 120]
        ]

criteria_names = [f'C_{i+1}' for i in range(len(cvalues))]

matrix = np.array([
    [3000,  96, 145, 200, 610, 10.0, 120, 99.0, 120.0],
    [2000, 100, 145, 200, 610, 10.0, 120, 99.0,  90.0],
    [ 705, 120, 170,  80, 270,  4.0,  30, 24.0,  25.0],
    [ 613, 140, 180, 140, 400,  8.0,  40, 24.2,  50.0],
    [ 350, 100, 110,  30, 196,  4.5,  15, 10.5,  12.9],
    [ 350, 100, 100,  30, 196,  4.5,  15, 10.5,  15.5],
    [ 350, 100, 150,  30, 196,  7.0,  35, 16.0,  18.7],
    [ 635, 110, 170,  49, 200,  8.0,  35, 22.5,  31.5],
    [ 340, 150, 160, 110, 500,  6.0,  10, 35.0,  45.0],
    [ 750,  57, 110,  10,  80,  8.0, 120, 35.0,  24.4]
    ], dtype='float')

model = StructuralCOMET(
        submodels=[
            Submodel((0, 1, 2),
                     [8.24041444e-02, 4.53869580e-01, 7.85105159e-01],
                     MethodExpert(
                         TOPSIS(),
                         np.ones(3)/3, [1, 1, 1]),
                     'P_1'),
            Submodel((3, 4),
                     [0.00000000e+00, 4.43071484e-01, 1.00000000e+00],
                     MethodExpert(
                         TOPSIS(),
                         np.ones(2)/2, [1, 1]),
                     'P_2'),
            Submodel((5, 6, 7),
                     [1.49566750e-01, 4.81255932e-01, 7.15106856e-01],
                     MethodExpert(
                         TOPSIS(),
                         np.ones(3)/3, [-1, -1, 1]),
                     'P_3'),
            Submodel(('P_1', 'P_3', 'P_2', 'C_9'),
                     None,
                     MethodExpert(
                         TOPSIS(),
                         np.ones(4)/4, [1, 1, 1, -1]),
                     'P Final')
            ],
        cvalues=cvalues,
        criteria_names=criteria_names
        )

res = model(matrix)

print(res)
