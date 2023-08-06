#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Tomas Cassanelli
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import interpolate
from astropy.io import ascii
from astropy.utils.data import get_pkg_data_filename
import os
import yaml
from .aperture import radiation_pattern, phase
from .math_functions import wavevector2degrees, wavevector2radians
from .aux_functions import uv_ratio

__all__ = [
    'plot_beam', 'plot_data', 'plot_phase', 'plot_variance', 'plot_fit_path'
    ]

# Plot style added from relative path
plt.style.use(get_pkg_data_filename('data/pyoof.mplstyle'))


def plot_beam(
    params, d_z, wavel, illum_func, telgeo, resolution, box_factor, plim_rad,
    angle, title
        ):
    """
    Beam maps, :math:`P_\\mathrm{norm}(u, v)`, figure given fixed
    ``I_coeff`` coefficients and ``K_coeff`` set of coefficients. It is the
    straight forward result from a least squares minimization
    (`~pyoof.fit_beam`). There will be three maps, for three radial offsets,
    :math:`d_z^-`, :math:`0` and :math:`d_z^+` (in meters).

    Parameters
    ----------
    params : `~numpy.ndarray`
        Two stacked arrays, the illumination and Zernike circle polynomials
        coefficients. ``params = np.hstack([I_coeff, K_coeff])``.
    d_z : `list`
        Radial offset :math:`d_z`, added to the sub-reflector in meters. This
        characteristic measurement adds the classical interference pattern to
        the beam maps, normalized squared (field) radiation pattern, which is
        an out-of-focus property. The radial offset list must be as follows,
        ``d_z = [d_z-, 0., d_z+]`` all of them in meters.
    wavel : `float`
        Wavelength, :math:`\\lambda`, of the observation in meters.
    illum_func : `function`
        Illumination function, :math:`E_\\mathrm{a}(x, y)`, to be evaluated
        with the key **I_coeff**. The illumination functions available are
        `~pyoof.aperture.illum_pedestal` and `~pyoof.aperture.illum_gauss`.
    telgeo : `list`
        List that contains the blockage distribution, optical path difference
        (OPD) function, and the primary radius (`float`) in meters. The list
        must have the following order, ``telego = [block_dist, opd_func, pr]``.
    resolution : `int`
        Fast Fourier Transform resolution for a rectangular grid. The input
        value has to be greater or equal to the telescope resolution and with
        power of 2 for faster FFT processing. It is recommended a value higher
        than ``resolution = 2 ** 8``.
    box_factor : `int`
        Related to the FFT resolution (**resolution** key), defines the image
        pixel size level. It depends on the primary radius, ``pr``, of the
        telescope, e.g. a ``box_factor = 5`` returns ``x = np.linspace(-5 *
        pr, 5 * pr, resolution)``, an array to be used in the FFT2
        (`~numpy.fft.fft2`).
    plim_rad : `~numpy.ndarray`
        Contains the maximum values for the :math:`u` and :math:`v`
        wave-vectors, it can be in degrees or radians depending which one is
        chosen in **angle** key. The `~numpy.ndarray` must be in the following
        order, ``plim_rad = np.array([umin, umax, vmin, vmax])``.
    angle : `str`
        Angle unit, it can be ``'degrees'`` or ``'radians'``.
    title : `str`
        Figure title.

    Returns
    -------
    fig : `~matplotlib.figure.Figure`
        The three beam maps plotted from the input parameters. Each map with a
        different offset :math:`d_z` value. From left to right, :math:`d_z^-`,
        :math:`0` and :math:`d_z^+`.
    """

    I_coeff = params[:4]
    K_coeff = params[4:]

    u, v, F = [], [], []
    for _d_z in d_z:

        _u, _v, _F = radiation_pattern(
            K_coeff=K_coeff,
            I_coeff=I_coeff,
            d_z=_d_z,
            wavel=wavel,
            illum_func=illum_func,
            telgeo=telgeo,
            resolution=resolution,
            box_factor=box_factor
            )

        u.append(_u)
        v.append(_v)
        F.append(_F)

    u = np.array(u)
    v = np.array(v)
    power_pattern = np.abs(F) ** 2
    power_norm = np.array(
        [power_pattern[i] / power_pattern[i].max() for i in range(3)]
        )

    # Limits, they need to be transformed to degrees
    if plim_rad is None:
        pr = telgeo[2]  # primary reflector radius
        bw = 1.22 * wavel / (2 * pr)  # Beamwidth radians
        size_in_bw = bw * 8

        # Finding central point for shifted maps
        uu, vv = np.meshgrid(_u, _v)
        u_offset = uu[power_norm[1] == power_norm[1].max()][0]
        v_offset = vv[power_norm[1] == power_norm[1].max()][0]

        u_offset = wavevector2radians(u_offset, wavel)
        v_offset = wavevector2radians(v_offset, wavel)

        plim_rad = [
            -size_in_bw + u_offset, size_in_bw + u_offset,
            -size_in_bw + v_offset, size_in_bw + v_offset
            ]

    if angle == 'degrees':
        plim_angle = np.degrees(plim_rad)
        u_angle = wavevector2degrees(u, wavel)
        v_angle = wavevector2degrees(v, wavel)
    if angle == 'radians':
        plim_angle = plim_rad
        u_angle = wavevector2radians(u, wavel)
        v_angle = wavevector2radians(v, wavel)

    plim_u, plim_v = plim_angle[:2], plim_angle[2:]

    subtitle = [
        '$P_{\\textrm{\\scriptsize{norm}}}(u,v)$ $d_z=' +
        str(round(d_z[i], 3)) + '$ m' for i in range(3)
        ]

    fig, ax = plt.subplots(ncols=3, figsize=uv_ratio(plim_u, plim_v))

    for i in range(3):

        extent = [
            u_angle[i].min(), u_angle[i].max(),
            v_angle[i].min(), v_angle[i].max()
            ]

        im = ax[i].imshow(power_norm[i], extent=extent, vmin=0, vmax=1)
        ax[i].contour(u_angle[i], v_angle[i], power_norm[i], 10)

        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.03)
        cb = fig.colorbar(im, cax=cax)
        cb.formatter.set_powerlimits((0, 0))
        cb.ax.yaxis.set_offset_position('left')
        cb.update_ticks()

        ax[i].set_title(subtitle[i])
        ax[i].set_ylabel('$v$ ' + angle)
        ax[i].set_xlabel('$u$ ' + angle)
        ax[i].set_ylim(*plim_v)
        ax[i].set_xlim(*plim_u)
        ax[i].grid('off')

    fig.suptitle(title)
    fig.tight_layout()

    return fig


def plot_data(u_data, v_data, beam_data, d_z, angle, title, res_mode):
    """
    Real data beam maps, :math:`P^\\mathrm{obs}(x, y)`, figures given
    given 3 out-of-focus radial offsets, :math:`d_z`.

    Parameters
    ----------
    u_data : `~numpy.ndarray`
        :math:`x` axis value for the 3 beam maps in radians. The values have
        to be flatten, in one dimension, and stacked in the same order as the
        ``d_z = [d_z-, 0., d_z+]`` values from each beam map.
    v_data : `~numpy.ndarray`
        :math:`y` axis value for the 3 beam maps in radians. The values have
        to be flatten, one dimensional, and stacked in the same order as the
        ``d_z = [d_z-, 0., d_z+]`` values from each beam map.
    beam_data : `~numpy.ndarray`
        Amplitude value for the beam map in mJy. The values have to be
        flatten, one dimensional, and stacked in the same order as the ``d_z =
        [d_z-, 0., d_z+]`` values from each beam map. If ``res_mode = False``,
        the beam map will be normalized.
    d_z : `list`
        Radial offset :math:`d_z`, added to the sub-reflector in meters. This
        characteristic measurement adds the classical interference pattern to
        the beam maps, normalized squared (field) radiation pattern, which is
        an out-of-focus property. The radial offset list must be as follows,
        ``d_z = [d_z-, 0., d_z+]`` all of them in meters.
    wavel : `float`
        Wavelength, :math:`\\lambda`, of the observation in meters.
    angle : `str`
        Angle unit, it can be ``'degrees'`` or ``'radians'``.
    title : `str`
        Figure title.
    res_mode : `bool`
        If ``True`` the beam map will not be normalized. This feature is used
        to compare the residual outputs from the least squares minimization
        (`~pyoof.fit_beam`).

    Returns
    -------
    fig : `~matplotlib.figure.Figure`
        Figure from the three observed beam maps. Each map with a different
        offset :math:`d_z` value. From left to right, :math:`d_z^-`, :math:`0`
        and :math:`d_z^+`.
    """

    if not res_mode:
        # Power pattern normalization
        beam_data = [beam_data[i] / beam_data[i].max() for i in range(3)]
    # input u and v are in radians
    uv_title = angle

    if angle == 'degrees':
        u_data, v_data = np.degrees(u_data), np.degrees(v_data)

    vmin = np.min(beam_data)
    vmax = np.max(beam_data)

    subtitle = [
        '$P_{\\textrm{\\scriptsize{norm}}}^{\\textrm{\\scriptsize{obs}}}' +
        '(u,v)$ $d_z={}$ m'.format(round(d_z[i], 3)) for i in range(3)
        ]

    fig, ax = plt.subplots(ncols=3, figsize=uv_ratio(u_data[0], v_data[0]))

    for i in range(3):
        # new grid for beam_data
        u_ng = np.linspace(u_data[i].min(), u_data[i].max(), 300)
        v_ng = np.linspace(v_data[i].min(), v_data[i].max(), 300)

        beam_ng = interpolate.griddata(
            # coordinates of grid points to interpolate from.
            points=(u_data[i], v_data[i]),
            values=beam_data[i],
            # coordinates of grid points to interpolate to.
            xi=tuple(np.meshgrid(u_ng, v_ng)),
            method='cubic'
            )

        extent = [u_ng.min(), u_ng.max(), v_ng.min(), v_ng.max()]
        im = ax[i].imshow(beam_ng, extent=extent, vmin=vmin, vmax=vmax)
        ax[i].contour(u_ng, v_ng, beam_ng, 10)

        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.03)

        cb = fig.colorbar(im, cax=cax)
        cb.formatter.set_powerlimits((0, 0))
        cb.ax.yaxis.set_offset_position('left')
        cb.update_ticks()

        ax[i].set_ylabel('$v$ ' + uv_title)
        ax[i].set_xlabel('$u$ ' + uv_title)
        ax[i].set_title(subtitle[i])
        ax[i].grid('off')

    fig.suptitle(title)
    fig.tight_layout()

    return fig


def plot_phase(K_coeff, notilt, pr, title):
    """
    Aperture phase distribution (phase error), :math:`\\varphi(x, y)`, figure,
    given the Zernike circle polynomial coefficients, ``K_coeff``, solution
    from the least squares minimization.

    Parameters
    ----------
    K_coeff : `~numpy.ndarray`
        Constants coefficients, :math:`K_{n\\ell}`, for each of them there is
        only one Zernike circle polynomial, :math:`U^\ell_n(\\varrho,
        \\varphi)`. The coefficients are between :math:`[-2, 2]`.
    notilt : `bool`
        Boolean to include or exclude the tilt coefficients in the aperture
        phase distribution. The Zernike circle polynomials are related to tilt
        through :math:`U^{-1}_1(\\varrho, \\varphi)` and
        :math:`U^1_1(\\varrho, \\varphi)`.
    pr : `float`
        Primary reflector radius in meters.
    title : `str`
        Figure title.

    Returns
    -------
    fig : `~matplotlib.figure.Figure`
        Aperture phase distribution parametrized in terms of the Zernike
        circle polynomials, and represented for the telescope's primary dish.
    """

    if notilt:
        cbartitle = (
            '$\\varphi_{\\scriptsize{\\textrm{no-tilt}}}(x,y)$ amplitude rad'
            )
    else:
        cbartitle = '$\\varphi(x, y)$ amplitude rad'

    extent = [-pr, pr, -pr, pr]
    _x, _y, _phase = phase(K_coeff=K_coeff, notilt=notilt, pr=pr)

    fig, ax = plt.subplots(figsize=(6, 5.8))

    levels = np.linspace(-2, 2, 9)

    im = ax.imshow(_phase, extent=extent)
    ax.contour(_x, _y, _phase, levels=levels, colors='k', alpha=0.3)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.03)
    cb = fig.colorbar(im, cax=cax)
    cb.ax.set_ylabel(cbartitle)

    ax.set_title(title)
    ax.set_ylabel('$y$ m')
    ax.set_xlabel('$x$ m')
    ax.grid('off')

    fig.tight_layout()

    return fig


def plot_variance(matrix, order, diag, cbtitle, title):
    """
    Variance-Covariance matrix or Correlation matrix figure. It returns
    the triangle figure with a color amplitude value for each element. Used to
    check/compare the correlation between the fitted parameters in a least
    squares minimization.

    Parameters
    ----------
    matrix : `~numpy.ndarray`
        Two dimensional array containing the Variance-Covariance or
        Correlation function. Output from the fit procedure.
    order : `int`
        Order used for the Zernike circle polynomial, :math:`n`.
    diag : `bool`
        If `True` it will plot the matrix diagonal.
    cbtitle : `str`
        Color bar title.
    title : `str`
        Figure title.

    Returns
    -------
    fig : `~matplotlib.figure.Figure`
        Triangle figure representing Variance-Covariance or Correlation matrix.
    """
    n = order
    N_K_coeff = (n + 1) * (n + 2) // 2
    ln = [(j, i) for i in range(0, n + 1) for j in range(-i, i + 1, 2)]
    L = np.array(ln)[:, 0]
    N = np.array(ln)[:, 1]

    params_names = [
        '$A_{E_\mathrm{a}}$', '$\mathrm{taper}_\mathrm{dB}$', '$x_0$', '$y_0$'
        ]
    for i in range(N_K_coeff):
        params_names.append('$K_{' + str(N[i]) + '\,' + str(L[i]) + '}$')
    params_names = np.array(params_names)

    params_used = [int(i) for i in matrix[:1][0]]
    _matrix = matrix[1:]

    x_ticks, y_ticks = _matrix.shape

    extent = [0, x_ticks, 0, y_ticks]

    if diag:
        k = -1
        # idx represents the ignored elements
        labels_x = params_names[params_used]
        labels_y = labels_x[::-1]
    else:
        k = 0
        # idx represents the ignored elements
        labels_x = params_names[params_used][:-1]
        labels_y = labels_x[::-1][:-1]

    # selecting half covariance
    mask = np.tri(_matrix.shape[0], k=k)
    matrix_mask = np.ma.array(_matrix, mask=mask).T
    # mask out the lower triangle

    fig, ax = plt.subplots()

    # get rid of the frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    im = ax.imshow(
        X=matrix_mask,
        extent=extent,
        vmax=_matrix.max(),
        vmin=_matrix.min(),
        cmap=plt.cm.Reds,
        interpolation='nearest',
        origin='upper'
        )

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.03)
    cb = fig.colorbar(im, cax=cax)
    cb.formatter.set_powerlimits((0, 0))
    cb.ax.yaxis.set_offset_position('left')
    cb.update_ticks()
    cb.ax.set_ylabel(cbtitle)

    ax.set_title(title)
    ax.set_xticks(np.arange(x_ticks) + 0.5)
    ax.set_xticklabels(labels_x, rotation='vertical')
    ax.set_yticks(np.arange(y_ticks) + 0.5)
    ax.set_yticklabels(labels_y)
    ax.grid('off')

    fig.tight_layout()

    return fig


def plot_fit_path(
    path_pyoof, order, illum_func, telgeo, resolution, box_factor, angle,
    plim_rad, save
        ):
    """
    Plot all important figures after a least squares minimization.

    Parameters
    ----------
    path_pyoof : `str`
        Path to the pyoof output, ``'pyoof_out/directory'``.
    order : `int`
        Order used for the Zernike circle polynomial, :math:`n`.
    illum_func : `function`
        Illumination function, :math:`E_\\mathrm{a}(x, y)`, to be evaluated
        with the key **I_coeff**. The illumination functions available are
        `~pyoof.aperture.illum_pedestal` and `~pyoof.aperture.illum_gauss`.
    telgeo : `list`
        List that contains the blockage distribution, optical path difference
        (OPD) function, and the primary radius (`float`) in meters. The list
        must have the following order, ``telego = [block_dist, opd_func, pr]``.
    resolution : `int`
        Fast Fourier Transform resolution for a rectangular grid. The input
        value has to be greater or equal to the telescope resolution and with
        power of 2 for faster FFT processing. It is recommended a value higher
        than ``resolution = 2 ** 8``.
    box_factor : `int`
        Related to the FFT resolution (**resolution** key), defines the image
        pixel size level. It depends on the primary radius, ``pr``, of the
        telescope, e.g. a ``box_factor = 5`` returns ``x = np.linspace(-5 *
        pr, 5 * pr, resolution)``, an array to be used in the FFT2
        (`~numpy.fft.fft2`).
    angle : `str`
        Angle unit, it can be ``'degrees'`` or ``'radians'``.
    plim_rad : `~numpy.ndarray`
        Contains the maximum values for the :math:`u` and :math:`v`
        wave-vectors, it can be in degrees or radians depending which one is
        chosen in **angle** key. The `~numpy.ndarray` must be in the following
        order, ``plim_rad = np.array([umin, umax, vmin, vmax])``.
    save : `bool`
        If ``True``, it stores all plots in the ``'pyoof_out/directory'``
        directory.

    Returns
    -------
    fig_beam : `~matplotlib.figure.Figure`
        The three beam maps plotted from the input parameters. Each map with a
        different offset :math:`d_z` value. From left to right, :math:`d_z^-`,
        :math:`0` and :math:`d_z^+`.
    fig_phase : `~matplotlib.figure.Figure`
        Aperture phase distribution for the Zernike circle polynomials for the
        telescope primary dish.
    fig_res : `~matplotlib.figure.Figure`
        Figure from the three observed beam maps residual. Each map with a
        different offset :math:`d_z` value. From left to right, :math:`d_z^-`,
        :math:`0` and :math:`d_z^+`.
    fig_data : `~matplotlib.figure.Figure`
        Figure from the three observed beam maps. Each map with a different
        offset :math:`d_z` value. From left to right, :math:`d_z^-`, :math:`0`
        and :math:`d_z^+`.
    fig_cov : `~matplotlib.figure.Figure`
        Triangle figure representing Variance-Covariance matrix.
    fig_corr : `~matplotlib.figure.Figure`
        Triangle figure representing Correlation matrix.
    """

    try:
        path_pyoof
    except NameError:
        print('pyoof directory does not exist: ' + path_pyoof)
    else:
        pass

    if not os.path.exists(path_pyoof + '/plots'):
        os.makedirs(path_pyoof + '/plots')

    path_plot = path_pyoof + '/plots'

    # Info
    n = order
    fitpar = ascii.read(path_pyoof + '/fitpar_n' + str(n) + '.csv')
    K_coeff = np.array(fitpar['parfit'])[4:]

    with open(path_pyoof + '/pyoof_info.yml', 'r') as inputfile:
        pyoof_info = yaml.load(inputfile)

    obs_object = pyoof_info['obs_object']
    meanel = round(pyoof_info['meanel'], 2)

    # Residual
    res = np.genfromtxt(path_pyoof + '/res_n' + str(n) + '.csv')

    # Data
    u_data = np.genfromtxt(path_pyoof + '/u_data.csv')
    v_data = np.genfromtxt(path_pyoof + '/v_data.csv')
    beam_data = np.genfromtxt(path_pyoof + '/beam_data.csv')

    # Covariance and Correlation matrix
    cov = np.genfromtxt(path_pyoof + '/cov_n' + str(n) + '.csv')
    corr = np.genfromtxt(path_pyoof + '/corr_n' + str(n) + '.csv')

    if n == 1:
        fig_data = plot_data(
            u_data=u_data,
            v_data=v_data,
            beam_data=beam_data,
            d_z=pyoof_info['d_z'],
            title='{} observed power pattern $\\alpha={}$ degrees'.format(
                obs_object, meanel),
            angle=angle,
            res_mode=False
            )

    fig_beam = plot_beam(
        params=np.array(fitpar['parfit']),
        title='{} fit power pattern  $n={}$ $\\alpha={}$ degrees'.format(
            obs_object, n, meanel),
        d_z=pyoof_info['d_z'],
        wavel=pyoof_info['wavel'],
        illum_func=illum_func,
        telgeo=telgeo,
        plim_rad=plim_rad,
        angle=angle,
        resolution=resolution,
        box_factor=box_factor
        )

    fig_phase = plot_phase(
        K_coeff=K_coeff,
        title=(
            '{} phase error $d_z=\\pm {}$ m ' +
            '$n={}$ $\\alpha={}$ deg'
            ).format(obs_object, round(pyoof_info['d_z'][2], 3), n, meanel),
        notilt=True,
        pr=telgeo[2]
        )

    fig_res = plot_data(
        u_data=u_data,
        v_data=v_data,
        beam_data=res,
        d_z=pyoof_info['d_z'],
        title='{} residual $n={}$'.format(obs_object, n),
        angle=angle,
        res_mode=True
        )

    fig_cov = plot_variance(
        matrix=cov,
        order=n,
        title='{} variance-covariance matrix $n={}$'.format(obs_object, n),
        cbtitle='$\sigma_{ij}^2$',
        diag=True
        )

    fig_corr = plot_variance(
        matrix=corr,
        order=n,
        title='{} correlation matrix $n={}$'.format(obs_object, n),
        cbtitle='$\\rho_{ij}$',
        diag=True
        )

    if save:
        fig_beam.savefig(path_plot + '/fitbeam_n{}.pdf'.format(n))
        fig_phase.savefig(path_plot + '/fitphase_n{}.pdf'.format(n))
        fig_res.savefig(path_plot + '/residual_n{}.pdf'.format(n))
        fig_cov.savefig(path_plot + '/cov_n{}.pdf'.format(n))
        fig_corr.savefig(path_plot + '/corr_n{}.pdf'.format(n))

        if n == 1:
            fig_data.savefig(path_plot + '/obsbeam.pdf')
