import numpy as np
import pandas as pd
import pymcdm as pm

df = pd.read_csv('examples/vans.csv')
print(df.columns)

# MAIRCA example
alts = np.array([[70, 245, 16.4, 19],
                   [52, 246, 7.3, 22],
                   [53, 295, 10.3, 25],
                   [63, 256, 12, 8],
                   [64, 233, 5.3, 17]])
weights = np.array([0.04744, 0.02464, 0.51357, 0.41435])
types = np.array([1, 1, 1, 1])

# alts = df[df.columns[3:]].to_numpy()
# weights = pm.weights.equal_weights(alts)
# types = [1, 1, 1, 1, 1, -1, -1, 1, -1]
bounds = pm.methods.SPOTIS.make_bounds(alts)

tested_methods = [
    pm.methods.ARAS(),  # TODO rewrite ARAS so the additional element will be out of extended matrix, + maybe add esp
                        # TODO ARAS has wrong description in the documentation
                        # TODO ARAS check the tests
    pm.methods.COCOSO(),
    pm.methods.CODAS(),
    # pm.methods.COMET(),  # TODO rewrite call to support verbose here
    # pm.methods.COPRAS(),
    pm.methods.EDAS(),
    pm.methods.ERVD(np.mean(alts, axis=0)),
    pm.methods.MABAC(),
    pm.methods.MAIRCA(),  # TODO verify the algorithm. Tr should be 2d?
    # pm.methods.MARCOS(),  # TODO return to this method later
    # pm.methods.MOORA(),
    pm.methods.OCRA(),  # TODO mistakes in the documentation
    pm.methods.PROBID(),  # TODO mistakes in the documentation
                          # TODO add a way to support custom symbols in some tables instead of only A and C
    # pm.methods.PROMETHEE_I(),  # TODO think how to return data or maybe not return at all
    # pm.methods.PROMETHEE_II(),  # TODO think how to return data or maybe not return at all
    pm.methods.RAM(),
    pm.methods.RIM(bounds),  # TODO support of the custom symbols (for ref ideal) and proper order
    pm.methods.SPOTIS(bounds),
    pm.methods.TOPSIS(),
    pm.methods.VIKOR(),
    pm.methods.WSM(), # TODO Sprawdzić wzory? Pytanie czy ma być taki sam wynik jak w WASPAS czy nie
    pm.methods.WPM(), # TODO Sprawdzić wzory? Pytanie czy ma być taki sam wynik jak w WASPAS czy nie
    pm.methods.WASPAS()
]

for tm in tested_methods:
    results = tm(alts, weights, types, verbose=True)
    s = results.to_string(group_tables=True, float_fmt='%0.6f')
    with open(f'output/{results.method_name}.txt', 'w') as f:
        f.write(s)
