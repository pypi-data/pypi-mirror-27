import math
import numpy as np


def fft(signal):
    """Performs a fft on a given signal.

    :param signal: signal
    :type signal: list, numpy array
    :returns:Frequency domain representation of signal
    :rtype: numpy array
    """

    return _fftHelper(signal, 1)


def ifft(transformed):
    """Performs an inverse fft on a given transformed signal.

    :param trasnformed: transformed signal
    :type transformed: list, numpy array
    :returns: Inverted signal
    :rtype: numpy array
    """

    return _fftHelper(transformed, -1)/len(transformed)


def fft2(image):
    """Performs a 2-dimensional fft on a given image.

    :param image: image
    :type image: 2-dimensional list, numpy array
    :returns: Frequency domain representation of image
    :rtype: 2-dimensional numpy array
    """

    return _fft2Helper(image, 1)


def ifft2(image):
    """Performs an inverse 2-dimensional fft on a given transformed image.

    :param image: transformed image
    :type image: 2-dimensional list, numpy array
    :returns: Inverted image
    :rtype: 2-dimensional numpy array
    """

    return _fft2Helper(image, -1)/image.size


def _fft2Helper(image, direction):
    transformed = np.empty(image.shape, dtype=complex)
    for k in range(len(image)):
        transformed[k] = _fftHelper(image[k], direction)
    for k in range(len(image[0])):
        transformed[:, k] = _fftHelper(transformed[:, k], direction)

    return transformed


def _bit_reverse_order(signal):
    N = len(signal)
    numBits = int((N-1).bit_length())
    log2 = int(math.log(N, 2))
    newSignal = np.empty_like(signal)
    for i in range(N):
        binary = bin(i).replace('0b', '').replace('0B', '').zfill(numBits)
        reverseBinary = binary[::-1]
        newSignal[int(reverseBinary, 2)] = signal[i]

    return newSignal


def _fftHelper(signal, direction=1):
    N = len(signal)
    log2 = math.log(N, 2)
    if int(log2) != log2:
        print "Signal length must be a power of 2"

    signal = _bit_reverse_order(signal).astype(complex)

    for level in range(1, int(log2+1)):
        n = 2**level
        omega = np.power(np.exp(direction*-2*np.pi*1j/n), np.arange(n/2.0))
        for i in range(0, N, n):
            first = signal[i:i + n/2]
            second = omega*signal[i + n/2:i + n]
            (signal[i:i + n/2], signal[i + n/2:i + n]) = (
                first + second, first - second)

    return signal
