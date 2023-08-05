import pygasp.dctCuda as dct
import numpy as np
import scipy.fftpack
import pytest


def test_dctCuda_equal_scipy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i, dtype=np.float64)
        control = scipy.fftpack.dct(signal, norm='ortho')
        test = dct.dct(signal)

        assert np.allclose(test, control)


def test_idctCuda_equal_scipy_arange():
    for i in range(8, 11):
        signal = np.arange(2**i, dtype=np.float64)
        control = scipy.fftpack.idct(signal, norm='ortho')
        test = dct.idct(signal)

        assert np.allclose(test, control)


def test_dct2Cuda_equal_scipy_arange():
    for i in [100, 105]:
        signal = np.arange(i**2, dtype=np.float64).reshape(i, i)
        control = scipy.fftpack.dct(
                    scipy.fftpack.dct(signal, norm='ortho', axis=0),
                    norm='ortho', axis=1)
        test = dct.dct2(signal)

        assert np.allclose(test, control)


def test_idct2Cuda_equal_scipy_arange():
    for i in [100, 105]:
        signal = np.arange(i**2, dtype=np.float64).reshape(i, i)
        control = scipy.fftpack.idct(
                    scipy.fftpack.idct(signal, norm='ortho', axis=0),
                    norm='ortho', axis=1)
        test = dct.idct2(signal)

        assert np.allclose(test, control)
