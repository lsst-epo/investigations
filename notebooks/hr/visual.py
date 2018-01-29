"""Visual for HR diagram investigations.
"""
import math
import random

from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Div
from bokeh.plotting import figure, show

from .data import Berkeley20, NGC2849, get_hr_data, L_ZERO_POINT


def _telescope_pointing_widget():
    html = '<table><thead><tr>'
    html += '<td><b>Telescope pointing</b></td>'
    html += '<td><b>Cluster Name</b></td>'
    html += '<td><b>Image number</b></td>'
    html += '<td><b>Right ascension</b></td>'
    html += '<td><b>Declination</b></td>'
    html += '</tr></thead><tbody><tr>'
    html += '<td><img src="files/data/sphere.png"></td>'
    html += '<td>LSST 8433</td>'
    html += '<td>20221274993</td>'
    html += '<td>05h 32m 37s</td>'
    html += '<td>+00h 11m 18s</td>'
    html += '</tr></tbody></table>'
    return Div(text=html, width=600, height=175)


def _diagram(plot_figure, source=None, color='black', line_color='#333333',
             xaxis_label="B-V [mag]", yaxis_label='V [mag]', name=None):
    """Use a :class:`~bokeh.plotting.figure.Figure` and x and y collections
    to create an HR diagram.
    """
    plot_figure.circle(x=source.data.get('x'), y=source.data.get('y'),
                       size=4, color=color, alpha=0.78, name=name,
                       line_color=line_color, line_width=0.5)
    plot_figure.xaxis.axis_label = xaxis_label
    plot_figure.yaxis.axis_label = yaxis_label


def cc_diagram(cluster_name):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an HR
    diagram using the cluster_name; then show it.
    """
    x, y = get_hr_data(cluster_name)
    y_range = [max(y) + 0.5, min(y) - 0.25]
    pf = figure(y_range=y_range, title=cluster_name)
    _diagram(x, y, pf)
    show(pf)


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


def m_M_compare(cluster):
    """
    """
    x1, y1 = cluster.stars()
    x2, y2 = abs_mag(cluster)
    max_y = max(max(y1), max(y2))
    min_y = min(min(y1), min(y2))
    source_1 = ColumnDataSource(data=dict(x=x1, y=y1))
    source_2 = ColumnDataSource(data=dict(x=x2, y=y2))
    pf = figure(y_range=[max_y + 0.5, min_y - 0.25])
    _diagram(source=source_1, plot_figure=pf, name='app', color='purple',
             line_color='#993333')
    _diagram(source=source_2, plot_figure=pf, name='abs', color='#444444')
    show(pf)


def m_M_compare_interactive_b20(doc):
    """
    """
    cluster = Berkeley20()
    x1, y1 = cluster.stars()
    x2, y2 = abs_mag(cluster)
    max_y = max(max(y1), max(y2))
    min_y = min(min(y1), min(y2))
    source_1 = ColumnDataSource(name='app', data=dict(x=x1, y=y1))
    source_2 = ColumnDataSource(name='abs', data=dict(x=x2, y=y2))
    pf = figure(title='Distance through μ',
                y_range=[max_y + 0.5, min_y - 0.25])
    _diagram(source=source_1, plot_figure=pf, name='app', color='purple',
             line_color='#993333')
    _diagram(source=source_2, plot_figure=pf, name='abs', color='#444444')

    def update_data(attrname, old, new):
        new_x, new_y = abs_mag(cluster, float(distance.value))
        selected = pf.select(name='app')
        selected[0].data_source.data = dict(x=new_x, y=new_y)

    min_adj = random.randint(2, 5)
    adj = random.randint(
        math.floor(cluster.coord.distance.value / min_adj),
        math.floor(cluster.coord.distance.value / (min_adj - 1)))
    end = cluster.coord.distance.value + adj
    distance = Slider(title='Distance(parsecs)', value=0.0,
                      start=0.0, end=end, step=10)
    distance.on_change('value', update_data)
    inputs = widgetbox(distance)
    doc.add_root(row(inputs, pf))
    doc.title = 'Distance through μ'


def m_M_compare_interactive_ngc2849(doc):
    """
    """
    cluster = NGC2849()
    x1, y1 = cluster.stars()
    x2, y2 = abs_mag(cluster)
    max_y = max(max(y1), max(y2))
    min_y = min(min(y1), min(y2))
    source_1 = ColumnDataSource(name='app', data=dict(x=x1, y=y1))
    source_2 = ColumnDataSource(name='abs', data=dict(x=x2, y=y2))
    pf = figure(title='Distance through μ',
                y_range=[max_y + 0.5, min_y - 0.25])
    _diagram(source=source_1, plot_figure=pf, name='app', color='purple',
             line_color='#993333')
    _diagram(source=source_2, plot_figure=pf, name='abs', color='#444444')

    def update_data(attrname, old, new):
        new_x, new_y = abs_mag(cluster, float(distance.value))
        selected = pf.select(name='app')
        selected[0].data_source.data = dict(x=new_x, y=new_y)

    min_adj = random.randint(2, 5)
    adj = random.randint(
        math.floor(cluster.coord.distance.value / min_adj),
        math.floor(cluster.coord.distance.value / (min_adj - 1)))
    end = cluster.coord.distance.value + adj
    distance = Slider(title='Distance(parsecs)', value=0.0,
                      start=0.0, end=end, step=10)
    distance.on_change('value', update_data)
    inputs = widgetbox(distance)
    doc.add_root(row(inputs, pf))
    doc.title = 'Distance through μ'


def luminosity(M_vs):
    """
    """
    ls = []
    for M_v in M_vs:
        ls.append(pow(10, -(0.4 * M_v)))  # * L_ZERO_POINT
    return ls


def hr_diagram(cluster_name):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an HR
    diagram using the cluster_name; then show it.
    """
    cluster = get_hr_data(cluster_name)
    x, y = abs_mag(cluster)
#    y = luminosity(y)
    y_range = [max(y) + 0.5, min(y) - 0.25]
    source = ColumnDataSource(data=dict(x=x, y=y))
    pf = figure(y_range=y_range, title=cluster_name)
    _diagram(source=source, plot_figure=pf, name='hr', color='gray',
             yaxis_label='V absolute [mag]')
    show(pf)


def hr_diagram_skyviewer(cluster_name):
    """
    """
    input_caption = 'Type in the name of your cluster and press Enter/Return:'
    text_input = TextInput(value=cluster_name, title=input_caption)
    cluster = get_hr_data(cluster_name)
    x, y = abs_mag(cluster)
    y_range = [max(y) + 0.5, min(y) - 0.25]
    source = ColumnDataSource(data=dict(x=x, y=y), name='cluster')
    pf = figure(y_range=y_range, title='berkeley20')
    _diagram(source=source, plot_figure=pf, name='cluster', color='gray',
             yaxis_label='V absolute [mag]')
    pf_image = figure(x_range=(0, 1), y_range=(0, 1))
    pf_image.image_url(url=['notebooks/data/b20.png'],
                       x=0, y=0, w=1, h=1, anchor='bottom_left')
    pf_image.toolbar_location = None
    pf_image.axis.visible = False
    layout = column(text_input, _telescope_pointing_widget(),
                    row(pf_image, pf), sizing_mode="scale_width")
    show(layout)


def hr_diagram_interactive(doc):
    """
    """
    text_input = TextInput(value='ngc2849', title='Cluster:')

    cluster = get_hr_data('ngc2849')
    x, y = abs_mag(cluster)
    y_range = [max(y) + 0.5, min(y) - 0.25]
    source = ColumnDataSource(data=dict(x=x, y=y), name='cluster')
    pf = figure(y_range=y_range, title='berkeley20')
    _diagram(source=source, plot_figure=pf, name='hr', color='gray',
             yaxis_label='V absolute [mag]')
    pf_image = figure(x_range=(0, 1), y_range=(0, 1))
    pf_image.image_url(url=['notebooks/data/berkeley20.png'],
                       x=0, y=0, w=1, h=1, anchor="bottom_left")
    pf_image.toolbar_location = None
    pf_image.axis.visible = False
    inputs = widgetbox(text_input)
    layout = column(text_input, row(pf_image, pf))

    def update_data(attrname, old, new_):
        try:
            cluster = get_hr_data(text_input.value)
            new_x, new_y = abs_mag(cluster)
            #    y = luminosity(y)
            y_range = [max(new_y) + 0.5, min(new_y) - 0.25]
            source = ColumnDataSource(data=dict(x=new_x, y=new_y),
                                      name='cluster')
            pf = figure(y_range=y_range, title=text_input.value)
            _diagram(source=source, plot_figure=pf, name='hr', color='gray',
                     yaxis_label='V absolute [mag]')
            pf.title.text = text_input.value
            layout.children[1] = row(pf_image, pf)
        except Exception as e:
            print(e)

    text_input.on_change('value', update_data)
    doc.add_root(layout)
