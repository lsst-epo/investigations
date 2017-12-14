import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
output_notebook()
import csv


def berkeley20_data():
    with open('berkeley20.tsv', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        b20p = [row for row in reader]
        b20rawdata = b20p[41:]
        b20data = []
        [b20data.append(b[3:5]) for b in b20rawdata]
        return b20data


def ngc2849_data():
    pass


def get_h_r_data(name):
    if name.lower() == "berkeley20":
        data = berkeley20_data()
    elif name.lower() == "ngc2849":
        data = ngc2849_data()
    else:
        raise NotImplemented("Only berkeley20 is implemented right now.")
    if data:
        x = [float(data[i][1]) for i in range(len(data) - 1)]
        y = [float(data[i][0]) for i in range(len(data) - 1)]
        return (x, y)


def H_R(name):
    x, y = hr.get_h_r_data(name)
    p = figure(y_range=[max(y) + 0.5, min(y) - 0.25])
    p.circle(x, y, size=4, color='black', alpha=0.78, line_width=1, line_color='#9999FF')
    show(p)
