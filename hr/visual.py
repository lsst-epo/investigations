"""Visual for HR diagram investigations.
"""
from .data import get_hr_data
from bokeh.plotting import figure, show


def _diagram(x, y, plot_figure, color='black', line_color='#333333', xaxis_label = "B-V [mag]", yaxis_label='V [mag]'):
    """Use a :class:`~bokeh.plotting.figure.Figure` and x and y collections
    to create an HR diagram.
    """
    plot_figure.circle(x, y, size=4, color=color, alpha=0.78,
                       line_color=line_color, line_width=0.5)
    plot_figure.xaxis.axis_label = xaxis_label
    plot_figure.yaxis.axis_label = yaxis_label


def diagram(cluster_name):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an HR
    diagram using the cluster_name; then show it.
    """
    x, y = get_hr_data(cluster_name)
    pf = figure(y_range=[max(y) + 0.5, min(y) - 0.25], title="Berkeley 20")
    _diagram(x, y, plot_figure=pf)
    show(pf)

def diagram_compare(cluster_name, cluster_name_2):    
    x1, y1 = get_hr_data(cluster_name)
    x2, y2 = get_hr_data(cluster_name_2)
    max_y = max(max(y1), max(y2))
    min_y = min(min(y1), min(y2))
    pf = figure(y_range=[max_y + 0.5, min_y - 0.25])
    _diagram(x1, y1, plot_figure=pf, color='purple', line_color='#993333')
    _diagram(x2, y2, plot_figure=pf, color='#444444')
    show(pf)
