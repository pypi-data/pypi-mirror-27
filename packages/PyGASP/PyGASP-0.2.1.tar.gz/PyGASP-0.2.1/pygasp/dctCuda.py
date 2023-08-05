'''
This contains 1-dimensional and 2-dimensional, forward and inverse
Discrete Cosine Transforms (DCT).
Uses GPU acceleration via PyCUDA.
'''

import numpy as np
import math
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

mod = SourceModule("""
#include <math.h>
__global__ void cuDCT(double *signal, double *coefs, int N)
{
    int k = threadIdx.x + blockIdx.x*512;
    double tot = 0;
    for (int n = 0; n < N; n++) {
        tot += signal[n]*cos(M_PI/N*(n+.5)*k);
    }
    coefs[k] = tot;

}

__global__ void cuIDCT(double *transformed, double *signal, int N)
{
    int k = threadIdx.x + blockIdx.x*512;
    double tot = 0;
    double first = transformed[0]/sqrt((double)N);

    for (int n=1; n<N; n++) {
        tot += transformed[n]*cos(M_PI/N*n*(k+.5));
    }

    tot *= sqrt(2.0/(double)N);
    tot += first;

    signal[k] = tot;
}
""")


def dct(signal):
    """Performs a dct on a given signal.

    This function performs a dct on signal using CUDA GPU.

    :param signal: signal
    :type signal: list, numpy array
    :returns: transformed signal
    :rtype: numpy array
    """

    N = len(signal)

    # Create arrays
    signal = np.array(signal, dtype=np.float64)
    coefs = np.zeros(N, dtype=np.float64)

    # Allocate device space
    coefsD = cuda.mem_alloc(coefs.nbytes)
    signalD = cuda.mem_alloc(signal.nbytes)

    # Copy signal to device
    cuda.memcpy_htod(signalD, signal)

    # Calculate block/grid size
    gridSize = int(N/512)
    if gridSize == 0:
        gridSize = 1
    elif N % 512 != 0:
        gridSize += 1
    blockSize = 512
    if N < 512:
        blockSize = N

    # Execute
    func = mod.get_function("cuDCT")
    func(signalD, coefsD, np.int32(N),
         grid=(gridSize, 1),
         block=(blockSize, 1, 1))

    # Retrieve results
    cuda.memcpy_dtoh(coefs, coefsD)
    coefs = coefs[:N]
    coefs[0] *= 1/math.sqrt(2)
    coefs *= math.sqrt(2.0/N)

    return coefs


def idct(transformed):
    """Performs an inverse dct on a given signal.

    This function performs an inverse dct on signal using CUDA GPU.

    :param transformed: transformed signal
    :type signal: list, numpy array
    :returns: inverted signal
    :rtype: numpy array
    """

    N = len(transformed)

    # Create arrays
    signal = np.zeros(N, dtype=np.float64)
    transformed = np.array(transformed, dtype=np.float64)

    # Allocate device space
    signalD = cuda.mem_alloc(signal.nbytes)
    transformedD = cuda.mem_alloc(transformed.nbytes)

    # Copy to device
    cuda.memcpy_htod(transformedD, transformed)

    # Calculate block/grid size
    gridSize = int(N/512)
    if gridSize == 0:
        gridSize = 1
    elif N % 512 != 0:
        gridSize += 1
    blockSize = 512
    if N < 512:
        blockSize = N

    # Execute
    func = mod.get_function("cuIDCT")
    func(transformedD, signalD, np.int32(N),
         grid=(gridSize, 1),
         block=(blockSize, 1, 1))

    # Retrieve results
    cuda.memcpy_dtoh(signal, signalD)
    signal = signal[:N]

    return signal


def dct2(signal):
    """Performs a 2-dimensional dct on a given signal.

    This function performs a dct on signal using CUDA GPU.

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

    This function performs a 2-dimensional inverse dct on signal using
    CUDA GPU.

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
