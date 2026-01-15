# Copyright (c) 2026 Andrii Shekhovtsov
# Copyright (c) 2026 Bartłomiej Kizielewicz

from functools import wraps
import numpy as np

__all__ = [
    'draWS',
    'kemeny',
    'frobenius'
]

def _distance_decorator(func):
    @wraps(func)
    def wrapped(x, y):
        x = np.array(x)
        y = np.array(y)
        # Validate non-empty inputs
        if x.size == 0 or y.size == 0:
            raise ValueError("Input arrays must be non-empty for distance computation.")
        return func(x, y)
    return wrapped

def _r_to_psm(r: np.ndarray) -> np.ndarray:
    """
    Convert ranking vector to Preference Score Matrix.
    Rankings should be presented as indices, i.e. for the given
    objects [A1, A2, A3] and ordering A2 > A1 > A3,
    the ranking vector should be [2, 1, 3].

    Parameters
    ----------
    r : ndarray
        Ranking vector in indices format.

    Returns
    -------
    psm : ndarray
        Preference Score Matrix.
    """
    n = len(r)
    psm = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            if r[i] < r[j]:
                val = 1
            elif r[i] > r[j]:
                val = -1
            else:
                val = 0

            psm[i, j] = val
            psm[j, i] = -val
    return psm


@_distance_decorator
def draWS(x, y):
    """ Calculate drastic WS distance between the ranking vectors.
        Rankings should be presented as indices, i.e. for the ranking
        A2 > A1 > A3 the ranking vector should be [2, 1, 3].

        Parameters
        ----------
            x : ndarray | list | tuple
                First vector of ranks.

            y : ndarray | list | tuple
                Second vector of ranks.

        Returns
        -------
            float
                Drastic distance between two rankings vectors.

        References
        ----------
        .. [1] Sałabun, W., & Shekhovtsov, A. (2023, September). An innovative drastic metric for ranking similarity
               in decision-making problems.
               In 2023 18th Conference on Computer Science and Intelligence Systems (FedCSIS) (pp. 731-738). IEEE.
    """
    return sum(2 ** -i * int(xi != yi)
               for i, (xi, yi) in enumerate(zip(x, y), 1)) / (1 - 2**(-len(x)))


@_distance_decorator
def kemeny(r1, r2):
    """
    Calculate Kemeny distance between two ranking vectors.
    Rankings should be presented as indices, i.e. for the given
    objects [A1, A2, A3] and ordering A2 > A1 > A3,
    the ranking vector should be [2, 1, 3].

    Parameters
    ----------
    r1 : ndarray | list | tuple
        First ranking vector in indices format.
    r2 : ndarray | list | tuple
        Second ranking vector in indices format.

    Returns
    -------
    float
        Kemeny distance between two ranking vectors.
    """
    m1 = _r_to_psm(r1)
    m2 = _r_to_psm(r2)
    return 0.5 * np.sum(np.abs(m1 - m2))


@_distance_decorator
def frobenius(r1, r2):
    """
    Calculate Frobenius distance between two ranking vectors.
    Rankings should be presented as indices, i.e. for the given
    objects [A1, A2, A3] and ordering A2 > A1 > A3,
    the ranking vector should be [2, 1, 3].

    Parameters
    ----------
    r1 : ndarray | list | tuple
        First ranking vector in indices format.
    r2 : ndarray | list | tuple
        Second ranking vector in indices format.

    Returns
    -------
    float
        Frobenius distance between two ranking vectors.
    """
    m1 = _r_to_psm(r1)
    m2 = _r_to_psm(r2)
    return np.sqrt(np.sum(np.abs(m1 - m2)**2))
