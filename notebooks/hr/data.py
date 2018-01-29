import numpy as np
import csv
import re

from astropy import units as u
from astropy.coordinates import SkyCoord


class OpenCluster(object):
    ra = None
    dec = None
    distance = None

    def stars(cls):
        NotImplemented()


class Berkeley20(OpenCluster):
    """
    paper: ???
    http://simbad.u-strasbg.fr/simbad/sim-id?Ident=Berkeley20&submit=submit+id
    https://www.aanda.org/articles/aa/abs/2002/27/aa2476/aa2476.html
    """
    coord = SkyCoord("05 32 37.0 +00 11 18", unit=(u.hourangle, u.deg),
                     distance=9000 * u.parsec)  # +- 480
    fe_h = -0.3
    tau = 5.5
    eb_v = 0.15
    Z = 0.008  # Z_sun
    d_modulus = 14.7  # (m - M)
    name = "Berkeley 20"
    image_path = 'notebooks/data/berkeley20-square.png'

    @property
    def distance(self):
        return self.coord.distance.value


    def cds_stars(cls):
        with open('data/berkeley20.tsv', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            b20p = [row for row in reader]
            b20rawdata = b20p[41:]
            data = []
            for b in b20rawdata:
                data.append(b[3:5])
            x = [float(data[i][1]) for i in range(len(data) - 1)]
            y = [float(data[i][0]) for i in range(len(data) - 1)]
            return (x, y)

    def stars(cls):
        with open('data/berkeley20-durgapal.dat', newline='') as f:
            lines = f.readlines()
            data = []
            pattern = re.compile("^\s+|\s* \s*|\s+$")
            for l in lines:
                values = [v for v in pattern.split(l) if v]
                V = float(values[3])
                B_V = float(values[5])
                data.append([V, B_V])
            x = [data[i][1] for i in range(len(data) - 1)]
            y = [data[i][0] for i in range(len(data) - 1)]
            return (x, y)


class NGC2849(OpenCluster):
    """
    paper: http://iopscience.iop.org/article/10.1086/424939/pdf
           https://academic.oup.com/mnras/article/430/1/221/984833
    """
    coord = SkyCoord("09 19 23.0 -40 31 01", unit=(u.hourangle, u.deg),
                     distance=6110 * u.parsec)

    def stars(cls):
        with open('data/ngc2849-kyeong.dat', newline='') as f:
            lines = f.readlines()
            lines = lines[2:]
            data = []
            pattern = re.compile("^\s+|\s* \s*|\s+$")
            for l in lines:
                values = [v for v in pattern.split(l) if v]
                V = float(values[7])
                B = float(values[5])
                data.append([V, B - V])
                x = [data[i][1] for i in range(len(data) - 1)]
                y = [data[i][0] for i in range(len(data) - 1)]
        return (x, y)


class NGC7790(OpenCluster):
    """
    paper: https://aas.aanda.org/articles/aas/pdf/2000/15/ds6060.pdf
    """
    coord = SkyCoord("23 58 24.0 +61 12 30", unit=(u.hourangle, u.deg),
                     distance=3230 * u.parsec)


# http://adsbit.harvard.edu/cgi-bin/nph-iarticle_query?bibcode=1968ApJ...151..611M&db_key=AST&page_ind=3&data_type=GIF&type=SCREEN_VIEW&classic=YES
# Morgan-Keenan (MK), Effective Surface Temperature, U-V, B-V
temps = [['O5', 37500, -1.47, -0.32],
         ['O6', 36500, -1.46, -0.32],
         ['O7', 35700, -1.45, -0.32],
         ['O8', 35000, -1.44, -0.31],
         ['O9', 34300, -1.43, -0.31],
         ['O9.5', 32100, -1.40, -0.30],
         ['B0', 30900, -1.38, -0.30],
         ['B0.5', 26200, -1.29, -0.28],
         ['B1', 22600, -1.19, -0.26],
         ['B2,', 20500, -1.10, -0.24],
         ['B3', 17900, -0.91, -0.20],
         # B4 is missing?
         ['B5', 15600, -0.72, -0.16],
         ['B6', 14600, -0.63, -0.14],
         ['B7', 13600, -0.54, -0.12],
         ['B8', 12000, -0.39, -0.09],
         ['B9', 10700, -0.25, -0.06],
         ['B9.5', 10000, -0.13, -0.03],
         ['A0', 9600, 0.00, 0.00],
         ['A1', 9320, 0.06, 0.03],
         ['A2', 9070, 0.12, 0.06],
         ['A3', 8840, 0.17, 0.09],
         ['A4', 8630, 0.21, 0.12],
         ['A5', 8500, 0.25, 0.14],
         # A6 is missing?
         ['A7', 8200, 0.30, 0.19],
         ['F0', 7520, 0.37, 0.31],
         # F1 is missing?
         ['F2', 7240, 0.39, 0.36],
         ['F3', 7000, 0.41, 0.40],
         # F4 is missing
         ['F5', 6810, 0.43, 0.43],
         ['F6', 6580, 0.48, 0.47],
         ['F7', 6370, 0.54, 0.51],
         ['F8', 6210, 0.60, 0.54],
         ['G0', 5980, 0.70, 0.59],
         ['G1', 5890, 0.75, 0.61],
         ['G2', 5800, 0.79, 0.63],
         ['G', 5200],
         ['K', 3700],
         ['M', 2400]]


def get_hr_data(name):
    if name.lower() == "berkeley20":
        data = Berkeley20()
    elif name.lower() == "berkeley20_cds":
        b20 = Berkeley20()
        b20.stars = b20.cds_stars
        data = b20
    elif name.lower() == "ngc2849":
        data = NGC2849()
    else:
        raise NotImplemented("Only berkeley20 and ngc2849 are "
                             "implemented right now.")
    if data:
        return data


L_ZERO_POINT = 3.0128 * pow(10, 28)  # units to add:  * u.watt
