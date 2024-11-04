import pandas as pd
import numpy as np
import pymcdm as pm

df = pd.read_csv('examples/vans.csv')
print(df.columns)

alts = df[df.columns[3:]].to_numpy()
weights = pm.weights.equal_weights(alts)
types = [1, 1, 1, 1, 1, -1, -1, 1, -1]

topsis = pm.methods.TOPSIS()
results = topsis(alts, weights, types, verbose=True)

print(results.to_latex(group_tables=True))
