# Copyright (c) 2023 Andrii Shekhovtsov

import warnings
import numpy as np

class ESPExpert:
    """ Create an object which will rate characteristic objects using Expected
        Solution Points (ESPs) provided by an expert to rate the characteristic
        objects.

        Parameters
        ----------
            esps : ndarray
                Numpy 2d matrix which defines chosed Expected Solution Points.
                Each row should define one ESP, number of the colums should be
                equal to the number of criteria.

            bounds : ndarray
                Each row should contain min and max values for each criterion.
                Min and max should be different values!

            distance_function : Callable or None
                Function which will be used to calculate the distance between
                two numpy array a and b. Signature of the function is d(a, b).
                If None, ESPExpert._euclides function is used and the Euclides
                distance is calculated between vectors.

            distance_aggregation : Callable
                Function which is used to aggregate distances to several ESP
                for each characteristic object. Default is np.min().

            cvalues_psi : float or None
                Float in range (0, 1). This value determines location of the
                additional ESP-guided characteristic values. E.g. criteria
                domain bounds are [0, 10] and ESP is 3. Then if we chose
                psi = 0.2 we will get following characteristic values for
                such criterion: [0, 2.4, 3, 4.4, 10] (the psi part of the
                distance between bound and ESP is substracted and added).

            full_domain_psi : bool
                Determines if additional characteristic values will be
                generated using full domain (True) or distance between ESP
                and bounds (False). E.g. if full_domain_psi=True, criteria
                domain bounds are [0, 10] and ESP is 3. If we chose
                psi = 0.2 we will get following characteristic values for
                such criterion: [0, 1, 3, 5, 10] (the psi part of the
                distance between all domain is substracted and added).

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> import pymcdm as pm
            >>> # Define criteria bounds for the decision problem
            >>> bounds = np.array([[0, 1]] * 2, dtype=float)
            >>> # Define the Expected Solution Point (or Points) for this problem
            >>> esps = np.array([[0.4, 0.4]])
            >>> # Create the expert function using ESPExpert class
            >>> expert = pm.methods.comet_tools.ESPExpert(esps,
            ...                                           bounds,
            ...                                           cvalues_psi=0.2)
            >>> # Generate ESP-guided cvalues based on provided ESP and psi
            >>> cvalues = expert.make_cvalues()
            >>> # Create and identify COMET model
            >>> comet = pm.methods.COMET(cvalues, expert)
            >>> # Create a visualization of the characteriscic values,
            >>> # ESP and preference function
            >>> fig, ax = plt.subplots(figsize=(4, 3.5), dpi=200)
            >>> ax, cax = pm.visuals.comet_2d_esp_plot(comet, esps, bounds)
            >>> plt.tight_layout()
            >>> plt.show()
    """

    def __init__(self,
                 esps,
                 bounds,
                 distance_function=None,
                 distance_aggregation=np.min,
                 cvalues_psi=None,
                 full_domain_psi=False
                 ):
        self.esps = esps
        self.bounds = bounds
        if distance_function is None:
            distance_function = self._euclides
        self.distance_function = distance_function
        self.distance_aggregation = distance_aggregation
        self.psi = cvalues_psi
        self.full_domain_psi = full_domain_psi
        self._validate_input()

    def _validate_input(self):
        esps, bounds, cvalues_psi = self.esps, self.bounds, self.psi
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
        """ Evaluate characteristic objects using provided expected solution
            points.

            Parameters
            ----------
            co : np.array
                Characteristic objects which should be compared.

            Returns
            -------
                sj : np.array
                    SJ vector (see the COMET procedure for more info).

                mej : np.array
                    Identified MEJ matrix.
        """
        co = self._normalize(co)
        nesps = self._normalize(self.esps)

        distances = []
        for nesp in nesps:
            distances.append(self.distance_function(co, nesp))
        distances = self.distance_aggregation(distances, axis=0)

        try:
            result = self._call_mej(distances)
        except MemoryError:
            warnings.warn('Optimized version is used,'
                          ' MEJ will be not created.')
            result = self._call_optimized(distances)

        return result

    def _call_mej(self, distances):
        mej = np.zeros((distances.shape[0], distances.shape[0]),
                       dtype=np.float16)
        mask_better = distances[:, None] < distances
        mask_ties = distances[:, None] == distances
        mej[mask_better] = 1
        mej[~mask_better] = 0
        mej[mask_ties] = 0.5

        return mej.sum(axis=1).astype(np.float32), mej

    def _call_optimized(self, distances):
        sj = np.zeros(distances.shape[0], dtype=np.float16)
        for dist_i in distances:
            mask_better = distances < dist_i
            mask_ties = distances == dist_i
            sj[mask_better] += 1
            sj[mask_ties] += 0.5

        return sj.astype(np.float32), None

    def make_cvalues(self):
        """ Generate the characteristic values array based on provided
            ESPs and psi values. Usually using COMET with such cvalues will
            provide better results, however it is not mandatory.

            Returns
            -------
                cvalues : np.array
                    Characteristic values created based on ESPs and psi.
        """
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
