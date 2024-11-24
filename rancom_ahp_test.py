import pymcdm as pm
from pymcdm.weights.subjective import RANCOM, AHP

rancom = RANCOM(ranking=[1, 2, 2, 4])
print(rancom())
print(rancom.matrix)

rancom = RANCOM(scoring=[1, 2, 2, 4])
print(rancom())
print(rancom.matrix)

rancom.to_csv('test.csv', allow_overwrite=True)

rancom = RANCOM(filename='test.csv')
print(rancom())

rancom = RANCOM(object_names=['A', 'B', 'C', 'D'])
print(rancom())
print(rancom.matrix)