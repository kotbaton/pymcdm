import numpy as np
import pandas as pd
import pymcdm as pm

df = pd.read_csv('examples/vans.csv')
print(df.columns)

alts = df[df.columns[3:]].to_numpy()
weights = pm.weights.equal_weights(alts)
types = [1, 1, 1, 1, 1, -1, -1, 1, -1]
bounds = pm.methods.SPOTIS.make_bounds(alts)
expert = pm.methods.comet_tools.MethodExpert(pm.methods.TOPSIS(), weights, types)
cvalues = pm.methods.COMET.make_cvalues(alts, 3)


tested_methods = [
    pm.methods.ARAS(),  # TODO rewrite ARAS so the additional element will be out of extended matrix, + maybe add esp
                        # TODO ARAS has wrong description in the documentation
                        # TODO ARAS check the tests
    # pm.methods.MARCOS(),  # TODO return to this method later, extended matrix
    pm.methods.COCOSO(),
    pm.methods.CODAS(),
    pm.methods.COMET(cvalues, expert),
    # pm.methods.COPRAS(),
    pm.methods.EDAS(),
    pm.methods.ERVD(np.mean(alts, axis=0)),
    pm.methods.MABAC(),
    pm.methods.MAIRCA(),
    # pm.methods.MOORA(),
    pm.methods.OCRA(),  # TODO mistakes in the documentation
    pm.methods.PROBID(),  # TODO mistakes in the documentation
                          # TODO add a way to support custom symbols in some tables instead of only A and C
    pm.methods.PROMETHEE_I('usual'),  # TODO think how to return data or maybe not return at all
    pm.methods.PROMETHEE_II('usual'),  # TODO think how to return data or maybe not return at all
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
        s = results.to_latex(group_tables=True, float_fmt='%0.4f', label_prefix=True, ranking=False)
    else:
        s = results.to_latex(group_tables=True, float_fmt='%0.4f', label_prefix=True)
    with open(f'output/{results.method_name}.txt', 'w') as f:
        f.write(s)
