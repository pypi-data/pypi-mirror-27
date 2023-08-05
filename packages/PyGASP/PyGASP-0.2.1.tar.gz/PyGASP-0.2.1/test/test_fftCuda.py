import pygasp.fftCuda as fft
import numpy as np
import pytest


def test_fftCuda_equal_numpy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i)
        control = np.fft.fft(signal)
        ours = fft.fft(signal)
        assert np.allclose(control, ours)


def test_ifftCuda_equal_numpy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i)
        control = np.fft.ifft(signal)
        ours = fft.ifft(signal)
        assert np.allclose(control, ours)


def test_fft2Cuda_equal_numpy_arange():
    for i in [8, 16]:
        signal = np.arange(i**2).reshape(i, i)
        control = np.fft.fft2(signal)
        ours = fft.fft2(signal)
        assert np.allclose(control, ours)


def test_ifft2Cuda_equal_numpy_arange():
    for i in [8, 16]:
        signal = np.arange(i**2).reshape(i, i)
        control = np.fft.ifft2(signal)
        ours = fft.ifft2(signal)
        assert np.allclose(control, ours)
