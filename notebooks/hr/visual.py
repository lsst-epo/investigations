"""Visual for HR diagram investigations.
"""
import math
import random

from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, show

from .data import Berkeley20, NGC2849, get_hr_data, L_ZERO_POINT
from .science import abs_mag, distance, luminosity, teff


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


def hr_diagram(cluster_name):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an HR
    diagram using the cluster_name; then show it.
    """
    cluster = get_hr_data(cluster_name)
    pf = hr_diagram_figure(cluster)
    show(pf)


def skyimage_figure(cluster):
    """
    Given a cluster create a Bokeh plot figure using the
    cluster's image.
    """
    pf_image = figure(x_range=(0, 1), y_range=(0, 1),
                      title='Image for {0}.'.format(cluster.name))
    pf_image.image_url(url=[cluster.image_path],
                       x=0, y=0, w=1, h=1, anchor='bottom_left')
    pf_image.toolbar_location = None
    pf_image.axis.visible = False
    return pf_image


def hr_diagram_figure(cluster):
    """
    Given a cluster create a Bokeh plot figure creating an
    HR diagram.
    """
    t, l = teff(cluster), luminosity(cluster)
    x, y = t, l
    x_range = [max(x) + max(x) * 0.05, min(x) - min(x) * 0.05]
    source = ColumnDataSource(data=dict(x=x, y=y))
    pf = figure(y_axis_type='log', x_range=x_range, title='HR Diagram for {0}.'.format(cluster.name))
    _diagram(source=source, plot_figure=pf, name='hr', color='gray',
             xaxis_label='Effective Tempurature (K)', yaxis_label='Luminosity (☉)')
    return pf


def hr_diagram_skyimage(cluster_name):
    """
    """
    cluster = get_hr_data(cluster_name)
    text_input = TextInput(value=cluster.name, title='cluster:')
    pf = hr_diagram_figure(cluster)
    pf_image = skyimage_figure(cluster)
    layout = column(text_input, row(pf_image, pf))
    show(layout)


def hr_diagram_interactive(doc):
    """
    """
    text_input = TextInput(value='ngc2849', title='Cluster:')
    cluster = get_hr_data('ngc2849')
    source = ColumnDataSource(data=dict(x=x, y=y), name='cluster')
    pf = hr_diagram_figure(cluster)
    source = pf.source
    pf_image = skyimage_figure(cluster)
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
            pf = hr_diagram_figure(cluster)
            pf.title.text = text_input.value
            layout.children[1] = row(pf_image, pf)
        except Exception as e:
            print(e)

    text_input.on_change('value', update_data)
    doc.add_root(layout)
