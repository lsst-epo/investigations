"""
"""
import math

import numpy as np


def distance(modulus):
    """
    """
    return math.pow(10, modulus/5 + 1) * u.parsec


def luminosity(cluster):
    """
    """
    abs_mags = absolute_mag(cluster)
    ls = []
    for abs_mag in abs_mags:
        ls.append(pow(10, (4.74-abs_mag) * 0.4))  # In watts add * L_ZERO_POINT
    return ls


def teff(cluster):
    """
    Calculate Teff for main sequence stars ranging from Teff 3500K - 8000K. Use
    [Fe/H] of the cluster, if available.

    Returns a list of Teff values.
    """
    b_vs, _ = cluster.stars()
    teffs = []
    for b_v in b_vs:
        teffs.append(8575 - 5222.27 * b_v
                     + 1380.92 * b_v**2
                     + 701.7 * b_v * (cluster.fe_h - 0.15))
    return teffs


def absolute_mag(cluster):
    """
    """
    abs_mags = []
    teffs = teff(cluster)
    _, vs = cluster.stars()
    for t, v in zip(teffs, vs):
        abs_mags.append(v + bc(t) - 5 * math.log(cluster.distance / 10, 10)
                        - 3.1 * cluster.eb_v)
    return abs_mags


def bc(temp):
    """
    Calculate Bolometric Correction Using the Teff from the previous equation.
    This correction is for main sequence stars of the Teff range given above.
    """
    return (-1.007203E1 + temp * 4.347330E-3 - temp**2 * 6.159563E-7
            + temp**3 * 2.851201E-11)


def color(teffs):
    """
    Conventional color descriptions of stars.
    Source: https://en.wikipedia.org/wiki/Stellar_classification
    """
    colors = []
    for t in teffs:
        if t >= 7500:
            colors.append('blue_white')  # RGB:CAE1FF
        elif t >= 6000:
            colors.append('white')  # RGB:F6F6F6
        elif t >= 5200:
            colors.append('yellowish_white')  # RGB:FFFEB2
        elif t >= 3700:
            colors.append('pale_yellow_orange')  # RGB:FFB28B
        else:
            colors.append('light_orange_red')  # RGB:FF9966
    return colors


def table(cluster):
    """
    Create a numpy.ndarray with all observed fields and
    computed teff and luminosity values.
    """
    teffs = teff(cluster)
    lums = luminosity(cluster)
    arr = cluster.to_array()
    i = 0
    for row in arr:
        row['lum'][0] = np.array([lums[i]], dtype='f')
        row['temp'][0] = np.array([teffs[i]], dtype='f')
        i += 1
    return arr
