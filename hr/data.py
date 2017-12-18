import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
output_notebook()
import csv
import re


def berkeley20_cds_data():
    with open('data/berkeley20.tsv', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        b20p = [row for row in reader]
        b20rawdata = b20p[41:]
        data = []
        [data.append(b[3:5]) for b in b20rawdata]
        x = [float(data[i][1]) for i in range(len(data) - 1)]
        y = [float(data[i][0]) for i in range(len(data) - 1)]
        return (x, y)


def berkeley20_data():
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

    
def ngc2849_data():
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


def get_hr_data(name):
    if name.lower() == "berkeley20":
        data = berkeley20_data()
    elif name.lower() == "berkeley20_cds":
        data = berkeley20_cds_data()
    elif name.lower() == "ngc2849":
        data = ngc2849_data()
    else:
        raise NotImplemented("Only berkeley20 and ngc2849 are implemented right now.")
    if data:
        return data

