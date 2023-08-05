'''
Erin Carrier
Nathan Bowman
dwtFilters.py
Updated: 02/03/13

Library for performing thresholding on the output of the wavelet transform.
'''


def hardThreshold(transformed, threshold, minLevel, maxLevel):
    """Performs hard thresholding on result of wavelet transform.

    The wavelet transform must have been called with at least maxLevel levels.
    Thresholding performed on detail coefficients at levels minLevel to
    maxLevel, inclusive.
    All coefficients such that abs(coeff) < threshold are set equal to zero.

    :param transformed: transformed signal
    :param threshold: threshold level
    :param minLevel: minimum detail level to threshold
    :param maxLevel: maximum detail level to threshold
    :type signal: list of numpy arrays
    :type threshold: double
    :type minLevel: int
    :type maxLevel: int
    :returns: thresholded transformed signal
    :rtype: list of numpy arrays
    """
    return _threshold_helper(transformed, threshold, minLevel, maxLevel, False)


def softThreshold(transformed, threshold, minLevel, maxLevel):
    """Performs soft thresholding on result of wavelet transform.

    The wavelet transform must have been called with at least maxLevel levels.
    Thresholding performed on detail coefficients at levels minLevel to
    maxLevel, inclusive.
    Same as hard thresholding, but all coefficients not set equal to zero are
    adjusted by threshold.

    :param transformed: transformed signal
    :param threshold: threshold level
    :param minLevel: minimum detail level to threshold
    :param maxLevel: maximum detail level to threshold
    :type signal: list of numpy arrays
    :type threshold: double
    :type minLevel: int
    :type maxLevel: int
    :returns: thresholded transformed signal
    :rtype: list of numpy arrays
    """

    return _threshold_helper(transformed, threshold, minLevel, maxLevel, True)


def _threshold_helper(transformed, threshold, minLevel, maxLevel, soft):
    numElements = len(transformed)
    for i in range(minLevel, maxLevel+1):
        details = transformed[numElements - i]
        for j in range(len(details)):
            if abs(details[j]) <= threshold:
                details[j] = 0
            if soft:
                if details[j] < -1*threshold:
                    details[j] = details[j] + threshold
                else:
                    details[j] = details[j] - threshold
        transformed[numElements - i] = details

    return transformed
