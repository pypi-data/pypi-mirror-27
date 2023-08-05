import pygasp.fftIterative as fft
import numpy as np
import pytest


def test_fft_equal_numpy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i)
        control = np.fft.fft(signal)
        ours = fft.fft(signal)
        assert np.allclose(control, ours)


def test_ifft_equal_numpy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i)
        control = np.fft.ifft(signal)
        ours = fft.ifft(signal)
        assert np.allclose(control, ours)


def test_fft2_equal_numpy_arange():
    for i in [8, 16]:
        signal = np.arange(i**2).reshape(i, i)
        control = np.fft.fft2(signal)
        ours = fft.fft2(signal)
        assert np.allclose(control, ours)


def test_ifft2_equal_numpy_arange():
    for i in [8, 16]:
        signal = np.arange(i**2).reshape(i, i)
        control = np.fft.ifft2(signal)
        ours = fft.ifft2(signal)
        assert np.allclose(control, ours)
