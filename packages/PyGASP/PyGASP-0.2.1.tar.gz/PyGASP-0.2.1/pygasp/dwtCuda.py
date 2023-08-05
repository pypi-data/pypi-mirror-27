'''
This contains forward and reverse 1D and 2D transforms.
'''
import math
import numpy as np
import copy
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule


# ----------------------Begin CUDA device code-----------------------

mod = SourceModule("""
__global__ void cuDWT(double *signal, double *yLow, double *yHigh, double *h, double *g, const int filterLen)
{
    const int k = threadIdx.x + blockIdx.x*512;
    double sumH = 0;
    double sumG = 0;
    double element;

    for (int n = 0; n < filterLen; n++)
    {
       element = signal[2*k + n];
       sumH += element*h[n];
       sumG += element*g[n];
    }

    yHigh[k] = sumG;
    yLow[k] = sumH;

}

__global__ void cuIDWT(double *low, double *high, double *newAvgs, double *h, double *g, const int filterLen)
{
    const int k = threadIdx.x + blockIdx.x*512;
    double odd = 0;
    double even = 0;
    double lowElement, highElement;

    for (int j = 0; j < filterLen; j++)
    {
        lowElement = low[k+j];
        highElement = high[k+j];
        odd += h[1+2*j]*lowElement + g[1+2*j]*highElement;
        even += h[2*j]*lowElement + g[2*j]*highElement;
    }

    newAvgs[2*k] = odd;
    newAvgs[2*k+1] = even;

}
""")


# ----------------------Begin forward transform functions----------------------

def _chooseWavelet(wav):
    if wav == 'haar':
        h = (1.0/math.sqrt(2), 1.0/math.sqrt(2))
        g = (1.0/math.sqrt(2), -1.0/math.sqrt(2))
    elif wav == 'db2':
        bot = 4*2**.5
        h = [(1.0+3**.5)/bot, (3.0 + 3**.5)/bot, (3.0-3**.5)/bot,
             (1.0-3**.5)/bot]
        g = [(1.0-3**.5)/bot, -1*(3.0-3**.5)/bot, (3.0 + 3**.5)/bot,
             -1*(1.0+3**.5)/bot]
    elif wav == 'db3':
        outer = (2**.5)/32
        inner = (5 + 2*10**.5)**.5
        h = [outer*(1 + 10**.5 + inner),
             outer*(5 + 10**.5 + 3*inner),
             outer*(10 - 2*10**.5 + 2*inner),
             outer*(10 - 2*10**.5 - 2*inner),
             outer*(5 + 10**.5 - 3*inner),
             outer*(1 + 10**.5 - inner)]
        g = []
        for i in range(len(h)):
            g.append(((-1)**i)*h[5-i])
    elif wav == 'db4':
        h = [0.23037781330885523, 0.71484657055254153,
             0.63088076792959036, -0.027983769416983849,
             -0.18703481171888114, 0.030841381835986965,
             0.032883011666982945, -0.010597401784997278]
        g = [-0.010597401784997278, -0.032883011666982945,
             0.030841381835986965, 0.18703481171888114,
             -0.027983769416983849, -0.63088076792959036,
             0.71484657055254153, -0.23037781330885523]
    else:
        print 'Wavelet \'%s\' not found.  Using haar.' % (wav)
        return _chooseWavelet('haar')

    '''elif wav == 'db3':
        h = [0.3326705530, 0.8068915093, 0.4598775021, -0.1350110200,
             -0.0854412739, 0.0352262919]
        g = [0.0352262919, 0.0854412739, -0.1350110200, -0.4598775021,
             0.8068915093, -0.3326705530]'''

    return h, g


# Max signal length of approximately 2^27 due to memory limit of
# python list
def dwt(signal, wav='haar', levels=-1, mode='zpd'):
    """Performs a dwt on a given signal.

    This function performs a dwt on signal using CUDA GPU.

    :param signal: signal
    :param wav: Wavelet to use while performing dwt.
        Full list of available wavelets can be found ...
    :param levels: Number of levels of dwt to perform.
        If levels=-1, full decomposition is done, equivalent to
        levels = floor(log(len(signal), 2))
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type signal: list, numpy array
    :type wav: string
    :type levels: int
    :type mode: string
    :returns: transformed signal
    :rtype: list of arrays
    """

    if levels == -1:
        levels = math.floor(math.log(len(signal), 2))
    h, g = _chooseWavelet(wav)

    return _dwt_rec(signal, h, g, wav, levels, mode)


def dwt2(image, wav='haar', mode='zpd'):
    """Performs a 2-dimensional dwt on an image.

    This function performs a 2-dimensional dwt on an image using CUDA GPU.

    :param image: image
    :param wav: Wavelet to use while performing 2-dimensional dwt.
        Full list of available wavelets can be found ...
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type image: list of lists, 2-d numpy array
    :type wav: string
    :type mode: string
    :returns: transformed image
    :rtype: 2-tuple containing (cA, (cH, cV, cD))
    """

    ONE_LEVEL = 1
    h, g = _chooseWavelet(wav)
    temp = np.array(image)

    transLow = []
    transHigh = []
    m = len(temp)
    for i in range(m):
        trans = _dwt_rec(temp[i], h, g, wav, ONE_LEVEL, mode)
        transLow.append(trans[0])
        transHigh.append(trans[1])

    transLow = np.array(transLow)
    transHigh = np.array(transHigh)

    transLowL = []
    transLowH = []
    m = len(transLow[0])
    for i in range(m):
        trans = _dwt_rec(transLow[:, i], h, g, wav, ONE_LEVEL, mode)
        transLowL.append(trans[0])
        transLowH.append(trans[1])

    transHighL = []
    transHighH = []
    m = len(transHigh[0])
    for i in range(m):
        trans = _dwt_rec(transHigh[:, i], h, g, wav, ONE_LEVEL, mode)
        transHighL.append(trans[0])
        transHighH.append(trans[1])

    transLowL = np.transpose(transLowL)
    transLowH = np.transpose(transLowH)
    transHighL = np.transpose(transHighL)
    transHighH = np.transpose(transHighH)

    transformed = (transLowL, (transLowH, transHighL, transHighH))

    return transformed


def _extend(signal, length, mode='zpd'):
    pad = length-2
    if mode == 'zpd':
        for i in range(pad):
            signal = np.concatenate(([0], signal, [0]))
        if len(signal) % 2 != 0:
            signal = np.concatenate((signal, [0]))
    elif mode == 'ppd':
        for i in range(pad):
            signal = np.concatenate(([signal[-(1+2*i)]], signal,
                                     [signal[2*i]]))
        if len(signal) % 2 != 0:
            signal = np.concatenate((signal, [signal[2*pad]]))
    else:
        print 'Padding not understood. Returning zero-padding.'
        return _extend(signal, length, 'zpd')

    return signal


def _dwt_rec(signal, h, g, wav, levels, mode):

    if levels == 0:
        return [np.array(signal)]

    FIRST = 0
    MIDDLE = 1
    LAST = 2
    F = len(h)
    N = len(signal)
    position = FIRST

    signal = _extend(signal, F, mode)
    coefs = []
    lowList = []
    highList = []

    # signals that are too long must be broken up
    # for the moment, we are using 2^25 as our max
    # TODO: change the max to vary with the CUDA capabilities
    MAX_LEN = 2**25
    while len(signal) > 0:
        if len(signal) > MAX_LEN + F-2:
            remaining = signal[MAX_LEN:]
            signal = signal[:MAX_LEN+F-2]
            if position == FIRST:
                N = len(signal) - 2*(F-2)
                position = MIDDLE
                if len(remaining) <= MAX_LEN + F-2:
                    position = LAST
            elif position == MIDDLE:
                N = len(signal) - 2*(F-2)
                if len(remaining) <= MAX_LEN + F-2:
                    position = LAST
        else:
            if position == LAST:
                N = len(signal) - ((F-2) + N % 2)
            remaining = []

        # Put the lists into a form usable by CUDA
        h = np.float64(np.array(h))
        g = np.float64(np.array(g))
        signal = np.float64(np.array(signal))

        # Calculate the grid and block sizes
        # Create one thread for every 2 new coefficients
        size = int((N+1)/2.0+(F-2)/2.0)
        gridSize = int(size/512)
        if gridSize == 0:
            gridSize = 1
        elif size % 512 != 0:
            gridSize += 1
        blockSize = 512
        if N < 512:
            blockSize = size

        # Create the arrays to hold the new coefficients
        yHigh = np.float64(np.zeros(blockSize*gridSize))
        yLow = np.float64(np.zeros(blockSize*gridSize))

        # Allocate the necessary memory on the device
        signalD = cuda.mem_alloc(signal.nbytes)
        yHighD = cuda.mem_alloc(yHigh.nbytes)
        yLowD = cuda.mem_alloc(yLow.nbytes)
        hD = cuda.mem_alloc(h.nbytes)
        gD = cuda.mem_alloc(g.nbytes)
        # TODO: h, g, and signal should be moved to constant memory,
        # then maybe shared

        # Copy the signal and filters into device memory
        cuda.memcpy_htod(signalD, signal)
        cuda.memcpy_htod(hD, h)
        cuda.memcpy_htod(gD, g)

        # Get and execute the function
        func = mod.get_function("cuDWT")
        func(signalD, yLowD, yHighD, hD, gD, np.int32(F),
             grid=(gridSize, 1), block=(blockSize, 1, 1))

        # Copy the new coefficients back to the host
        cuda.memcpy_dtoh(yLow, yLowD)
        cuda.memcpy_dtoh(yHigh, yHighD)

        if position == LAST:
            size = (len(signal)-(F-2))/2

        lowList.append(yLow[:size])
        highList.append(yHigh[:size])

        signalD.free()
        yHighD.free()
        yLowD.free()
        hD.free()
        gD.free()

        signal = remaining

    coefs = _dwt_rec(np.concatenate(lowList), h, g, wav, levels-1, mode)
    coefs.append(np.concatenate(highList))
    return coefs


# ----------------------Begin inverse transform functions----------------------

def _chooseInverseWavelet(wav):
    if wav == 'haar':
        h = (1.0/math.sqrt(2), 1.0/math.sqrt(2))
        g = (-1.0/math.sqrt(2), 1.0/math.sqrt(2))
    elif wav == 'db2':
        h = [-0.1294095226, 0.224143868, 0.8365163037, 0.4829629131]
        g = [-0.4829629131, 0.8365163037, -0.224143868, -0.1294095226]
    elif wav == 'db3':
        h = [0.0352262919, -0.0854412739, -0.13501102, 0.4598775021,
             0.8068915093, 0.332670553]
        g = [-0.332670553, 0.8068915093, -0.4598775021, -0.13501102,
             0.0854412739, 0.0352262919]
    elif wav == 'db4':
        h = [-0.0105974018, 0.0328830117, 0.0308413818, -0.1870348117,
             -0.0279837694, 0.6308807679, 0.7148465706, 0.2303778133]
        g = [-0.2303778133, 0.7148465706, -0.6308807679, -0.0279837694,
             0.1870348117, 0.0308413818, -0.0328830117, -0.0105974018]
    else:
        print 'Wavelet \'%s\' not found.  Using haar.' % (wav)
        return _chooseInverseWavelet('haar')

    return h, g


def idwt(transformed, wav='haar', levels=-1, mode='zpd'):
    """Performs an inverse dwt on a given transformed signal.

    This function performs an inverse dwt on a transformed signal using CUDA
    GPU.

    :param transformed: transformed signal
    :param wav: Wavelet to use while performing inverse dwt.
        Full list of available wavelets can be found ...
    :param levels: Number of levels of inverse dwt to perform.
        If levels=-1, full decomposition is done, equivalent to
        levels = floor(log(len(signal), 2))
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type transformed: list, numpy array
    :type wav: string
    :type levels: int
    :type mode: string
    :returns: inverted signal
    :rtype: numpy array
    """

    h, g = _chooseInverseWavelet(wav)
    return _inverse_rec(copy.copy(transformed), h, g, levels, mode)


def idwt2(transformed, wav='haar', mode='zpd'):
    """Performs a 2-dimensional inverse dwt on a transformed image.

    This function performs a 2-dimensional inverse dwt on a transformed image
    using CUDA GPU.

    :param transformed: transformed image
    :param wav: Wavelet to use while performing inverse 2-dimensional dwt.
        Full list of available wavelets can be found ...
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type transformed: list of lists, 2-d numpy array
    :type wav: string
    :type mode: string
    :returns: inverted image
    :rtype: 2-d numpy array
    """

    ONE_LEVEL = 1
    h, g = _chooseInverseWavelet(wav)

    temp = copy.copy(transformed)
    cA = temp[0]
    cH = temp[1][0]
    cV = temp[1][1]
    cD = temp[1][2]

    transLowL = np.transpose(cA)
    transLowH = np.transpose(cH)
    transHighL = np.transpose(cV)
    transHighH = np.transpose(cD)

    left = []  # transLow
    right = []  # transHigh
    # This will give all the columns in transLow
    for i in range(len(cA)):
        left.append(idwt([transLowL[:, i], transHighL[:, i]], wav, ONE_LEVEL,
                         mode))
        right.append(idwt([transLowH[:, i], transHighH[:, i]], wav, ONE_LEVEL,
                          mode))
    left = np.transpose(np.array(left))
    right = np.transpose(np.array(right))

    image = []
    for i in range(len(left)):
        image.append(idwt([left[i], right[i]], wav, ONE_LEVEL, mode))

    return np.transpose(np.array(image))


def _extendInverse(signal, length, mode='zpd'):
    pad = length - 1
    if mode == 'zpd':
        for i in range(pad):
            signal = np.concatenate((signal, [0]))
    elif mode == 'ppd':
        for i in range(pad):
            signal = np.concatenate((signal, [signal[i]]))
    else:
        print 'Padding not understood. Returning zero-padding.'
        return _extendInverse(signal, length, 'zpd')

    return signal, pad


# This function only works for 1 level (8/9/2012)
# which makes levels useless
def _inverse_rec(transformed, h, g, levels, mode):

    if len(transformed) <= 1:
        return transformed[0]

    F = len(h)
    startLen = len(transformed[1])

    # Pad the transformed coefficients
    low, pad = _extendInverse(transformed[0], F, mode)
    high, pad = _extendInverse(transformed[1], F, mode)

    # Calculate the grid and block sizes
    # Create one thread for every 2 new coefficients
    gridSize = int(len(low)/512)
    if gridSize == 0:
        gridSize = 1
    blockSize = 512
    if len(low) < 512:
        blockSize = len(low)

    # Create array to hold the new coefficients
    newAvgs = np.zeros(2*len(low))

    # Put the lists into a form usable by CUDA
    newAvgs = np.float64(newAvgs)
    h = np.float64(np.array(h))
    g = np.float64(np.array(g))
    low = np.float64(np.array(low))
    high = np.float64(np.array(high))

    # Allocate the necessary memory on the device
    newAvgsD = cuda.mem_alloc(newAvgs.nbytes)
    hD = cuda.mem_alloc(h.nbytes)
    gD = cuda.mem_alloc(g.nbytes)
    lowD = cuda.mem_alloc(low.nbytes)
    highD = cuda.mem_alloc(high.nbytes)
    # TODO: h, g, low and high should be moved to constant memory,
    # then maybe shared

    # Copy the arrays into device memory
    cuda.memcpy_htod(newAvgsD, newAvgs)
    cuda.memcpy_htod(hD, h)
    cuda.memcpy_htod(gD, g)
    cuda.memcpy_htod(lowD, low)
    cuda.memcpy_htod(highD, high)

    # Get and execute the function
    func = mod.get_function("cuIDWT")
    func(lowD, highD, newAvgsD, hD, gD, np.int32(F/2),
         grid=(gridSize, 1), block=(blockSize, 1, 1))

    # Copy the new coefficients back to the host
    cuda.memcpy_dtoh(newAvgs, newAvgsD)

    newAvgs = newAvgs[:startLen*2]

    transformed.pop(0)
    transformed.pop(0)
    if 1-pad != 0:
        transformed.insert(0, newAvgs[:-pad+1])
    else:
        transformed.insert(0, newAvgs)

    return transformed[0]
