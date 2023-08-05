'''
Erin Carrier
Nathan Bowman
fftFilters.py
Updated: 02/03/13

Library of frequency filters for the results of the FFT.
'''


def highpass(transformed, samplingFreq, cutoff):
    """Performs highpass filtering on result of fourier transform.

    Any frequencies less than the cutoff frequency are removed.
    This is done by setting the coefficients of these frequencies to zero.
    Sampling frequency and cutoff frequency must have same units.

    :param transformed: transformed signal
    :param samplingFreq: sampling frequency
    :param cutoff: cutoff frequency
    :type signal: numpy array
    :type samplingFreq: double
    :type cutoff: double
    :returns: thresholded transformed signal
    :rtype: numpy array
    """

    return bandpass(transformed, samplingFreq, cutoff, -1)


def lowpass(transformed, samplingFreq, cutoff):
    """Performs lowpass filtering on result of fourier transform.

    Any frequencies greater than the cutoff frequency are removed.
    This is done by setting the coefficients of these frequencies to zero.
    Sampling frequency and cutoff frequency must have same units (e.g Hz).

    :param transformed: transformed signal
    :param samplingFreq: sampling frequency
    :param cutoff: cutoff frequency
    :type signal: numpy array
    :type samplingFreq: double
    :type cutoff: double
    :returns: thresholded transformed signal
    :rtype: numpy array
    """

    return bandpass(transformed, samplingFreq, -1, cutoff)


def bandpass(transformed, samplingFreq, cutoffLow, cutoffHigh):
    """Performs bandpass filtering on result of fourier transform.

    Any frequencies not between cutoffLow and cutoffHigh are removed.
    This is done by setting the coefficients of these frequencies to zero.
    Sampling frequency and cutoff frequencies must have same units (e.g. Hz).

    :param transformed: transformed signal
    :param samplingFreq: sampling frequency
    :param cutoffLow: low cutoff frequency
    :param cutoffHigh: high cutoff frequency
    :type signal: numpy array
    :type samplingFreq: double
    :type cutoffLow: double
    :type cutoffHigh: double
    :returns: thresholded transformed signal
    :rtype: numpy array
    """

    minFreq = cutoffLow*len(transformed)/samplingFreq
    maxFreq = cutoffHigh*len(transformed)/samplingFreq
    N = len(transformed)
    for i in range(N/2):
        if i >= minFreq:
            if maxFreq == -1:
                transformed[i] = 1
                transformed[N-i] = 1
            elif i <= maxFreq:
                transformed[i] = 1
                transformed[N-i] = 1
            else:
                transformed[i] = 0
                transformed[N-i] = 0
    return transformed
