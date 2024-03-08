import numpy as np

def get_local_weights(comet, alt, percent_step=0.01):
    """ Calculates local weights for alternative `alt` for each criterion
        using the algorithm presented in [1].

    References
    ----------
    [1] Więckowski, J., Kizielewicz, B., Paradowski, B., Shekhovtsov, A., & Sałabun, W. (2023). Application of Multi-Criteria Decision Analysis to Identify Global and Local Importance Weights of Decision Criteria. International Journal of Information Technology & Decision Making, 22(06), 1867–1892. https://doi.org/10.1142/S0219622022500948

    """

    cvalues = comet.cvalues
    n = len(cvalues) # Number of the criteria
    ranges = np.zeros(n)
    for i in range(n):
        min_, *_, max_ = cvalues[i]
        step = (max_ - min_) * percent_step
        changed_values = np.arange(min_, max_, step)
        calts = np.tile(alt, (changed_values.shape[0], 1))
        calts[:, i] = changed_values
        pref = comet(calts)
        ranges[i] = max(pref) - min(pref)
    return ranges / np.sum(ranges)
