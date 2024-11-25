import pymcdm as pm
from pymcdm.weights.subjective import RANCOM, AHP
from pymcdm.weights import equal_weights

selected_method = AHP

method = selected_method(ranking=[1, 2, 2, 4])
print('Ranking', [1, 2, 2, 4])
weights = method()
print(weights)
print(method.matrix)

method = selected_method(scoring=[4, 2, 2, 1])
print('Scoring', [4, 2, 2, 1])
weights = method()
print(weights)
print(method.matrix)

method.to_csv('test.csv', allow_overwrite=True)

method = selected_method(filename='test.csv')
print(method())

method = selected_method(object_names=['A', 'B', 'C', 'D'])
print(method())
print(method.matrix)
if isinstance(method, AHP):
    print(method.get_cr())