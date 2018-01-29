"""
"""
import math


def abs_mag(cluster, distance=None):
    """
    """
    stars = cluster.stars()
    b_v = stars[0]
    m_v = stars[1]
    M_v = []
    if not distance:
        distance = cluster.coord.distance.value
    for m in m_v:
        M_v.append(m - 5 * (math.log(distance, 10) - 1))
    return (b_v, M_v)


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
        ls.append(pow(10, (4.74-abs_mag) * 0.4))  # * L_ZERO_POINT
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
        teffs.append(8575 - 5222.27 * (b_v) \
                     + 1380.92 * b_v**2 \
                     + 701.7 * b_v * (cluster.fe_h - 0.15))
    return teffs


def absolute_mag(cluster):
    """
    """
    abs_mags = []
    teffs = teff(cluster)
    _, vs = cluster.stars()
    for t,v in zip(teffs, vs):
        abs_mags.append(v + bc(t) - 5 * math.log(cluster.distance / 10, 10) \
                        - 3.1 * cluster.eb_v)
    return abs_mags


def bc(temp):
    """
    Calculate Bolometric Correction Using the Teff from the previous equation.
    This correction is for main sequence stars of the Teff range given above.
    """
    return (-1.007203E1 + temp * 4.347330E-3 - temp**2 * 6.159563E-7
            + temp**3 * 2.851201E-11)
