import pandas as pd
import pymcdm as pm

df = pd.read_csv('examples/vans.csv')
print(df.columns)

alts = df[df.columns[3:]].to_numpy()
weights = pm.weights.equal_weights(alts)
types = [1, 1, 1, 1, 1, -1, -1, 1, -1]

tested_methods = [
    pm.methods.TOPSIS(),
    pm.methods.VIKOR(),
    pm.methods.ARAS(),  # TODO rewrite ARAS so the additional element will be out of extended matrix, + maybe add esp
                        # TODO ARAS has wrong description in the documentation
                        # TODO ARAS check the tests
    pm.methods.COCOSO(),
    pm.methods.CODAS(),

]

for tm in tested_methods:
    results = tm(alts, weights, types, verbose=True)
    s = results.to_string(group_tables=True)
    with open(f'output/{results.method_name}.txt', 'w') as f:
        f.write(s)
