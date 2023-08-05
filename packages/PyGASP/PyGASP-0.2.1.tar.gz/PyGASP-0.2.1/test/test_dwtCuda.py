import pygasp.dwtCuda as dwt
import numpy as np
import pytest
pywt = pytest.importorskip("pywt")


def test_dwtCuda_equal_pywt_arange():
    for i in range(12, 13):
        signal = np.arange(2**i)
        control = pywt.wavedec(signal, 'db2', level=1, mode='zpd')
        ours = dwt.dwt(signal, wav='db2', levels=1, mode='zpd')
        assert np.allclose(control, ours)


def test_idwtCuda_equal_pywt_arange():
    for i in range(12, 13):
        signal = np.arange(2**i)
        transformed = pywt.wavedec(signal, 'db2', level=1, mode='zpd')
        recovered = dwt.idwt(transformed, wav='db2', levels=1, mode='zpd')
        assert np.allclose(signal, recovered)


def test_dwt2Cuda_equal_pywt_arange():
    for i in [100, 105]:
        signal = np.arange(i**2).reshape(i, i)
        control = pywt.dwt2(signal, 'db2', mode='zpd')
        ours = dwt.dwt2(signal, wav='db2', mode='zpd')

        assert np.allclose(control[0], ours[0])
        for j in range(3):
            assert np.allclose(control[1][j], ours[1][j])


def test_idwt2Cuda_equal_pywt_arange():
    for i in [128, 256]:
        signal = np.arange(i**2).reshape(i, i)
        transformed = pywt.dwt2(signal, 'db2', mode='zpd')
        recovered = dwt.idwt2(transformed, wav='db2', mode='zpd')
        assert np.allclose(signal, recovered)
