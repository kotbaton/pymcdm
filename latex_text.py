import numpy as np
import pandas as pd
import pymcdm as pm

df = pd.read_csv('examples/vans.csv')
print(df.columns)

# alts = np.array([
#     [7.6, 46, 18, 390, 0.1, 11],
#     [5.5, 32, 21, 360, 0.05, 11],
#     [5.3, 32, 21, 290, 0.05, 11],
#     [5.7, 37, 19, 270, 0.05, 9],
#     [4.2, 38, 19, 240, 0.1, 8],
#     [4.4, 38, 19, 260, 0.1, 8],
#     [3.9, 42, 16, 270, 0.1, 5],
#     [7.9, 44, 20, 400, 0.05, 6],
#     [8.1, 44, 20, 380, 0.05, 6],
#     [4.5, 46, 18, 320, 0.1, 7],
#     [5.7, 48, 20, 320, 0.05, 11],
#     [5.2, 48, 20, 310, 0.05, 11],
#     [7.1, 49, 19, 280, 0.1, 12],
#     [6.9, 50, 16, 250, 0.05, 10]
# ])
#
# weights = np.array([0.21, 0.16, 0.26, 0.17, 0.12, 0.08])
# types = np.array([1, 1, 1, 1, -1, -1])
# xopt = np.array([15, 50, 24.5, 400, 0.05, 5])

alts = np.array([[660, 1000, 1600, 18, 1200],
                 [800, 1000, 1600, 24, 900],
                 [980, 1000, 2500, 24, 900],
                 [920, 1500, 1600, 24, 900],
                 [1380, 1500, 1500, 24, 1150],
                 [1230, 1000, 1600, 24, 1150],
                 [680, 1500, 1600, 18, 1100],
                 [960, 2000, 1600, 12, 1150]])

weights = np.array([0.1061, 0.3476, 0.3330, 0.1185, 0.0949])
types = np.array([-1, 1, 1, 1, 1])
xopt = None

# alts = df[df.columns[3:]].to_numpy()
# weights = pm.weights.equal_weights(alts)
# types = [1, 1, 1, 1, 1, -1, -1, 1, -1]
bounds = pm.methods.SPOTIS.make_bounds(alts)
expert = pm.methods.comet_tools.MethodExpert(pm.methods.TOPSIS(), weights, types)
cvalues = pm.methods.COMET.make_cvalues(alts, 3)

# TODO add T to Table??
# TODO make symbols and formulas same in docs and in verbose results
tested_methods = [
    pm.methods.ARAS(esp=xopt),
    pm.methods.MARCOS(),
    pm.methods.COCOSO(),
    pm.methods.CODAS(),
    pm.methods.COMET(cvalues, expert),
    pm.methods.COPRAS(),
    pm.methods.EDAS(),
    pm.methods.ERVD(np.mean(alts, axis=0)),
    pm.methods.MABAC(),
    pm.methods.MAIRCA(),
    pm.methods.MOORA(),
    pm.methods.OCRA(),  # TODO mistakes in the documentation
    pm.methods.PROBID(),  # TODO mistakes in the documentation
                          # TODO add a way to support custom symbols in some tables instead of only A and C
    pm.methods.PROMETHEE_I('usual'),
    pm.methods.PROMETHEE_II('usual'),
    pm.methods.RAM(),
    pm.methods.RIM(bounds),  # TODO support of the custom symbols (for ref ideal) and proper order
    pm.methods.SPOTIS(bounds),
    pm.methods.TOPSIS(),
    pm.methods.VIKOR(),
    pm.methods.WSM(),
    pm.methods.WPM(),
    pm.methods.WASPAS()
]

for tm in tested_methods:
    results = tm(alts, weights, types, verbose=True)
    if tm.__class__.__name__ == 'PROMETHEE_I':
        s = results.to_string(group_tables=True, float_fmt='%0.4f', label_prefix=True, ranking=False)
    else:
        s = results.to_string(group_tables=True, float_fmt='%0.4f', label_prefix=True)
    with open(f'output/{results.method_name}.txt', 'w') as f:
        f.write(s)
