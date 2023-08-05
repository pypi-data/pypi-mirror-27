import numpy as np
import math


def dct(signal):
    """Performs a dct on a given signal.

    This function performs a dct on signal.

    :param signal: signal
    :type signal: list, numpy array
    :returns: transformed signal
    :rtype: numpy array
    """

    N = len(signal)
    inds = np.arange(N)

    coefs = np.cos(math.pi/N*(inds+.5)*inds.reshape(-1, 1)).dot(signal)

    coefs[0] *= 1/math.sqrt(2)
    coefs *= math.sqrt(2.0/N)

    return coefs


def idct(transformed):
    """Performs an inverse dct on a given signal.

    This function performs an inverse dct on signal.

    :param transformed: transformed signal
    :type signal: list, numpy array
    :returns: inverted signal
    :rtype: numpy array
    """

    N = len(transformed)
    inds = np.arange(N)

    first = transformed[0]/math.sqrt(N)

    signal = np.cos(math.pi/N*inds[1:]*(inds.reshape(-1, 1) + 0.5)).dot(
                transformed[1:])
    signal *= math.sqrt(2.0/N)
    signal += first

    return signal


def dct2(signal):
    """Performs a 2-dimensional dct on a given signal.

    This function performs a 2-dimensional dct on signal.

    :param signal: signal
    :type signal: 2-dimensional numpy array
    :returns: transformed signal
    :rtype: 2-dimensional numpy array
    """
    N = len(signal)
    transformed = np.empty_like(signal)
    for k1 in range(N):
        transformed[k1] = dct(signal[k1])
    for k2 in range(N):
        transformed[:, k2] = dct(transformed[:, k2])

    return transformed


def idct2(transformed):
    """Performs a 2-dimensional inverse dct on a given signal.

    This function performs a 2-dimensional inverse dct on signal.

    :param transformed: transformed signal
    :type signal: 2-dimensional numpy array
    :returns: inverted signal
    :rtype: 2-dimensional numpy array
    """

    M = len(transformed)
    N = len(transformed[0])

    signal = np.empty_like(transformed)
    for x in range(M):
        signal[x] = idct(transformed[x])
    for y in range(N):
        signal[:, y] = idct(signal[:, y])

    return signal
