import math
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

mod = SourceModule("""
#include <pycuda-complex.hpp>
#define cmplx pycuda::complex<double>
__global__ void cuFFTHelp(cmplx *signal, cmplx OMEGA, int n)
{
    const int tid = blockIdx.x*512 + threadIdx.x;
    const int my_hop = tid/(n/2);
    const int my_place = tid - (n/2 * my_hop);

    cmplx first = signal[my_place + n*my_hop];
    cmplx second = pow(OMEGA, my_place)*signal[my_place + n*my_hop + n/2];
    signal[my_place + n*my_hop] = first + second;
    signal[my_place + n*my_hop + n/2] = first - second;
}
""")


def fft(signal):
    """Performs a fft on a given signal.

    This function performs a fft on signal using CUDA GPU.

    :param signal: signal
    :type signal: list, numpy array
    :returns:Frequency domain representation of signal
    :rtype: numpy array
    """
    return _fftHelper(signal, 1)


def ifft(transformed):
    """Performs an inverse fft on a given transformed signal.

    This function performs an ifft on a transformed signal using CUDA GPU.

    :param trasnformed: transformed signal
    :type transformed: list, numpy array
    :returns: Inverted signal
    :rtype: numpy array
    """
    return _fftHelper(transformed, -1)/len(transformed)


def fft2(image):
    """Performs a 2-dimensional fft on a given image.

    This function performs a fft on an image using CUDA GPU.

    :param image: image
    :type image: 2-dimensional list, numpy array
    :returns: Frequency domain representation of image
    :rtype: 2-dimensional numpy array
    """
    return _fft2Helper(image, 1)


def ifft2(image):
    """Performs an inverse 2-dimensional fft on a given transformed image.

    This function performs an ifft on a transformed 2-dimensional image using
    CUDA GPU.

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

    signal = np.complex128(_bit_reverse_order(signal))
    sigD = cuda.mem_alloc(signal.nbytes)
    cuda.memcpy_htod(sigD, signal)
    func = mod.get_function("cuFFTHelp")
    # these do not suffice, the function will not work on non multiples of 512
    bSize = int(min([512, N/2]))
    if N/2 <= 512:
        gSize = 1
    else:
        gSize = int(N/512)

    for level in range(1, int(log2+1)):
        n = 2**level
        OMEGA = np.complex128(np.exp(direction*-2*np.pi*1j/n))
        func(sigD, OMEGA, np.int32(n), grid=(gSize, 1), block=(bSize, 1, 1))
    cuda.memcpy_dtoh(signal, sigD)

    sigD.free()

    return signal
