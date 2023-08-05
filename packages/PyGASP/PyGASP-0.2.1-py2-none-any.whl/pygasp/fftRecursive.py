import cmath
import math
import numpy as np


def fft(signal):
    """Performs a fft on a given signal recursively.

    :param signal: signal
    :type signal: list, numpy array
    :returns:Frequency domain representation of signal
    :rtype: numpy array
    """
    return _fftHelper(signal, 1)


def ifft(signal):
    """Performs an inverse fft on a given transformed signal recursively.

    :param trasnformed: transformed signal
    :type transformed: list, numpy array
    :returns: Inverted signal
    :rtype: numpy array
    """
    return _fftHelper(signal, -1)/len(signal)


def fft2(image):
    """Performs a 2-dimensional fft on a given image recursively.

    :param image: image
    :type image: 2-dimensional list, numpy array
    :returns: Frequency domain representation of image
    :rtype: 2-dimensional numpy array
    """
    return _fft2Helper(image, 1)


def ifft2(image):
    """Performs an inverse 2-dimensional fft on a given transformed image
    recursively.

    :param image: transformed image
    :type image: 2-dimensional list, numpy array
    :returns: Inverted image
    :rtype: 2-dimensional numpy array
    """
    return _fft2Helper(image, -1)


def _fft2Helper(image, direction):
    transformed = np.empty(image.shape, dtype=complex)
    for k in range(len(image)):
        transformed[k] = _fftHelper(image[k], direction)
    for k in range(len(image[0])):
        transformed[:, k] = _fftHelper(transformed[:, k], direction)

    return transformed


def _fftHelper(signal, direction):
    n = len(signal)

    if n == 1:
        return signal
    else:
        OMEGA = cmath.exp(direction*-2*cmath.pi*1J/n)
        omega = 1

        evens = _fftHelper(signal[:n:2], direction)
        odds = _fftHelper(signal[1:n:2], direction)

        p = np.empty(n, dtype=complex)
        for k in range(n/2):
            p[k] = evens[k] + omega*odds[k]
            p[k+n/2] = evens[k] - omega*odds[k]
            omega = OMEGA*omega

        return p
