# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

class ESPExpert:
    """ Create an object which will rate characteristic objects using Expected
        Solution Points (ESPs) provided by an expert to rate the characteristic
        objects.
    """

    def __init__(self,
                 esps,
                 bounds,
                 distance_function=None,
                 distance_aggregation=np.min,
                 cvalues_psi=None,
                 full_domain_psi=False
                 ):
        self._validate_input(esps, bounds, cvalues_psi)
        self.esps = esps
        self.bounds = bounds
        if distance_function is None:
            distance_function = self._euclides
        self.distance_function = distance_function
        self.distance_aggregation = distance_aggregation
        self.psi = cvalues_psi
        self.full_domain_psi = full_domain_psi

    @staticmethod
    def _validate_input(esps, bounds, cvalues_psi):
        if len(esps.shape) != 2:
            raise ValueError('esps should be a two dimensional array '
                             'with one ESP in each row.')

        if len(bounds.shape) != 2:
            raise ValueError('bounds should be a two dimensional array '
                             'with one row define lower and upper bound of '
                             'the criteria domain.')

        if esps.shape[1] != bounds.shape[0]:
            raise ValueError('Number of criteria should be the same in esps '
                             '(columns) and bounds (rows) arrays.')

        if cvalues_psi is not None and not (0 < cvalues_psi < 1):
            raise ValueError('psi should be in range (0, 1) or None.')

    @staticmethod
    def _euclides(a, b):
        return np.sqrt(np.sum((a - b) ** 2, axis=1))

    def _normalize(self, x):
        return (x - self.bounds[:, 0]) / (self.bounds[:, 1] - self.bounds[:, 0])

    def __call__(self, co):
        co = self._normalize(co)
        nesps = self._normalize(self.esps)

        distances = []
        for nesp in nesps:
            distances.append(self.distance_function(co, nesp))
        distances = self.distance_aggregation(distances, axis=0)

        mej = np.zeros((co.shape[0], co.shape[0]), dtype=np.float32)
        mask_better = distances[:, None] < distances
        mask_ties = distances[:, None] == distances
        mej[mask_better] = 1
        mej[~mask_better] = 0
        mej[mask_ties] = 0.5

        return mej.sum(axis=1), mej

    def make_cvalues(self):
        psi = self.psi
        if psi is None:
            new_cvalues = np.array([
                sorted(set([b[0], *esp, b[-1]]))
                for b, esp in zip(self.bounds, self.esps.T)
            ], dtype='object')
        else:
            new_cvalues = []
            for i, (lb, ub) in enumerate(self.bounds):
                cvalues_for_crit = [lb, ub]
                for esp in self.esps[:, i]:
                    if self.full_domain_psi:
                        l = u = psi*(ub - lb)
                    else:
                        l, u = psi*(esp - lb), psi*(ub - esp)

                    cvalues_for_crit.extend((
                        esp - l,
                        esp,
                        esp + u,
                        ))
                uniq_cvalues = set(cv
                                   for cv in cvalues_for_crit
                                   if lb <= cv <= ub)
                new_cvalues.append(sorted(uniq_cvalues))

        return new_cvalues

