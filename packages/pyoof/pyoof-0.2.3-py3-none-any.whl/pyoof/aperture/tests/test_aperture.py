#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Tomas Cassanelli
import pytest
import numpy as np
from astropy.utils.data import get_pkg_data_filename
from astropy.utils.misc import NumpyRNGContext
from numpy.testing import assert_equal, assert_allclose
import pyoof


# Basic data for the telescope
pr = 50.
x = np.linspace(-pr, pr, 1e3)
xx, yy = np.meshgrid(x, x)

r, t = pyoof.cart2pol(xx, yy)

I_coeff = [1, -14, 0, 0]
K_coeff = np.array([0.1] * 21)
d_z = 0.022  # m
wavel = 0.0093685143125

telgeo = [
    pyoof.telgeometry.block_effelsberg,
    pyoof.telgeometry.opd_effelsberg,
    pr
    ]


def test_e_rs():

    with NumpyRNGContext(0):
        phase = np.sort(np.random.uniform(-2.5, 2.5, (5, 5)))

    e_rs = pyoof.aperture.e_rs(phase)

    assert_allclose(e_rs, 0.110794937514)


def test_illum_pedestal():

    _illum_pedestal = pyoof.aperture.illum_pedestal(
        x=xx,
        y=yy,
        I_coeff=I_coeff,
        pr=pr
        )

    illum_pedestal_true = np.load(
        get_pkg_data_filename('data/illum_pedestal.npy')
        )

    assert_allclose(_illum_pedestal, illum_pedestal_true)


def test_illum_gauss():

    _illum_gauss = pyoof.aperture.illum_gauss(
        x=xx,
        y=yy,
        I_coeff=I_coeff,
        pr=pr
        )

    illum_gauss_true = np.load(
        get_pkg_data_filename('data/illum_gauss.npy')
        )

    assert_allclose(_illum_gauss, illum_gauss_true)


def test_phase():

    _x, _y, _phase = pyoof.aperture.phase(
        K_coeff=K_coeff, notilt=True, pr=pr, resolution=1e3
        )

    data_phase = np.load(
        get_pkg_data_filename('data/phase.npz')
        )
    x_true = data_phase['x']
    y_true = data_phase['y']
    phase_true = data_phase['phi']

    assert_allclose(_phase, phase_true)
    assert_allclose(_x, x_true)
    assert_allclose(_y, y_true)

def test_wavefront():

    _wavefront = pyoof.aperture.wavefront(rho=r, theta=t, K_coeff=K_coeff)
    wavefront_true = np.load(get_pkg_data_filename('data/wavefront.npy'))

    assert_allclose(_wavefront, wavefront_true)


def test_aperture():

    _aperture = pyoof.aperture.aperture(
        x=xx,
        y=yy,
        K_coeff=K_coeff,
        I_coeff=I_coeff,
        d_z=d_z,
        wavel=wavel,
        illum_func=pyoof.aperture.illum_pedestal,
        telgeo=telgeo
        )

    aperture_true = np.load(get_pkg_data_filename('data/aperture.npy'))

    assert_allclose(_aperture, aperture_true)


def test_radiation_pattern():

    _u, _v, _radiation_pattern = pyoof.aperture.radiation_pattern(
        K_coeff=K_coeff,
        I_coeff=I_coeff,
        d_z=d_z,
        wavel=wavel,
        illum_func=pyoof.aperture.illum_pedestal,
        telgeo=telgeo,
        resolution=2 ** 8,
        box_factor=5
        )

    data_radiation_pattern = np.load(
        get_pkg_data_filename('data/radiation_pattern.npz')
        )
    u_true = data_radiation_pattern['u']
    v_true = data_radiation_pattern['v']
    radiation_pattern_true = data_radiation_pattern['F']

    assert_allclose(_radiation_pattern, radiation_pattern_true)
    assert_allclose(_u, u_true)
    assert_allclose(_v, v_true)
