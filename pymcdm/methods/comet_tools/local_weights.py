import numpy as np

def get_local_weights(comet, alt, percent_step=0.01):
    """
    Calculates local weights for alternative `alt` for each criterion
    using the algorithm presented in [#lw1]_ and [#lw2]_.

    Parameters
    ----------
        comet : COMET
            Identified COMET object to evaluate alternatives.
        alt : np.ndarray
            Single alternative in form of 1d numpy array.
        percent_step: float, optional
            Step for changing values in alternative for different criteria (see [#lw2]_). Default is 0.01.

    References
    ----------
    .. [#lw1] Więckowski, J., Kizielewicz, B., Paradowski, B., Shekhovtsov, A., & Sałabun, W. (2023). Application of
        Multi-Criteria Decision Analysis to Identify Global and Local Importance Weights of Decision Criteria.
        International Journal of Information Technology & Decision Making, 22(06), 1867–1892.
        https://doi.org/10.1142/S0219622022500948
    .. [#lw2] Shekhovtsov, A. and Sałabun, W. (2024). Comparing Global and Local Weights in Multi-Criteria
        Decision-Making: A COMET-Based Approach. In Proceedings of the 16th International Conference on Agents and
        Artificial Intelligence - Volume 3: ICAART; ISBN 978-989-758-680-4; ISSN 2184-433X, SciTePress,
        pages 470-477. DOI: 10.5220/0012360700003636
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
