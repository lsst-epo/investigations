"""Visual for H-R diagram investigations.
"""
import logging
import math
import random

from bokeh.layouts import row, column, widgetbox
from bokeh.models import CategoricalColorMapper, ColumnDataSource,\
    CustomJS, LassoSelectTool, Range1d, ResetTool
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import Slider, TextInput, Div
from bokeh.plotting import figure, show

from ipyaladin import Aladin

from ipywidgets import Layout, Box, widgets

import numpy

from .data import Berkeley20, NGC2849, get_hr_data, L_ZERO_POINT
from .science import absolute_mag, distance, luminosity, teff, color


def _telescope_pointing_widget(cluster_name):
    html = '<table><thead><tr>'
    html += '<td><b>Telescope pointing</b></td>'
    html += '<td><b>Cluster Name</b></td>'
    html += '<td><b>Image number</b></td>'
    html += '<td><b>Right ascension</b></td>'
    html += '<td><b>Declination</b></td>'
    html += '</tr></thead><tbody><tr>'
    html += '<td><img src="files/data/sphere.png"></td>'
    html += '<td>%s</td>' % cluster_name
    html += '<td>20221274993</td>'
    html += '<td>05h 32m 37s</td>'
    html += '<td>+00h 11m 18s</td>'
    html += '</tr></tbody></table>'
    return Div(text=html, width=600, height=175)


def _diagram(plot_figure, source=None, color='black', line_color='#444444',
             xaxis_label="B-V [mag]", yaxis_label='V [mag]', name=None):
    """Use a :class:`~bokeh.plotting.figure.Figure` and x and y collections
    to create an H-R diagram.
    """
    logging.info(type(source))
    logging.info(source)
    plot_figure.circle(x="x", y="y", source=source,
                       size=8, color=color, alpha=1, name=name,
                       line_color=line_color, line_width=0.5)
    plot_figure.xaxis.axis_label = xaxis_label
    plot_figure.yaxis.axis_label = yaxis_label
    plot_figure.yaxis.formatter = NumeralTickFormatter()


def cc_diagram(cluster_name):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an H-R
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
    x2, y2 = absolute_mag(cluster)
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
    x2, y2 = absolute_mag(cluster)
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
        new_x, new_y = absolute_mag(cluster, float(distance.value))
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
    x2, y2 = absolute_mag(cluster)
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
        new_x, new_y = absolute_mag(cluster, float(distance.value))
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
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an H-R
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
                      title='Image of {0}'.format(cluster.name))
    pf_image.image_url(url=[cluster.image_path],
                       x=0, y=0, w=1, h=1, anchor='bottom_left')
    pf_image.toolbar_location = None
    pf_image.axis.visible = False
    return pf_image


def hr_diagram_figure(cluster):
    """
    Given a cluster create a Bokeh plot figure creating an
    H-R diagram.
    """
    temps, lums = teff(cluster), luminosity(cluster)
    x, y = temps, lums
    colors, color_mapper = hr_diagram_color_helper(temps)
    x_range = [max(x) + max(x) * 0.05, min(x) - min(x) * 0.05]
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors))
    pf = figure(y_axis_type='log', x_range=x_range, name='hr',
                tools="box_select,lasso_select,reset",
                title='H-R Diagram for {0}'.format(cluster.name))
    _diagram(source=source, plot_figure=pf, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    return pf


def calculate_diagram_ranges(data):
    """
    Given a numpy array calculate what the ranges of the H-R
    diagram should be.
    """
    temps = data['temp']
    x_range = [1.05 * numpy.amax(temps), .95 * numpy.amin(temps)]

    lums = data['lum']
    y_range = [.50 * numpy.amin(lums), 2 * numpy.amax(lums)]
    return (x_range, y_range)


def hr_diagram_from_data(data, x_range, y_range):
    """
    Given a numpy array create a Bokeh plot figure creating an
    H-R diagram.
    """
    temps, lums = data['temp'], data['lum']
    x, y = temps, lums
    colors, color_mapper = hr_diagram_color_helper(temps)
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors))
    pf = figure(y_axis_type='log', x_range=x_range, y_range=y_range)
    _diagram(source=source, plot_figure=pf, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    show(pf)


def cluster_text_input(cluster, title=None):
    """
    Create an :class:`~bokeh.models.widgets.TextInput` using
    the cluster.name as the default value and title.

    If no title is provided use, 'Type in the name of your cluster
    and press Enter/Return:'.
    """
    if not title:
        title = 'Type in the name of your cluster and press Enter/Return:'
    return TextInput(value=cluster.name, title=title)


def hr_diagram_skyimage(cluster_name):
    """
    """
    cluster = get_hr_data(cluster_name)
    text_input = cluster_text_input(cluster)
    pf = hr_diagram_figure(cluster)
    pf_image = skyimage_figure(cluster)
    layout = column(text_input, _telescope_pointing_widget(cluster.name),
                    row(pf_image, pf), sizing_mode="scale_width")
    show(layout)


def ipywidget_box(bokeh_widget):
    """
    """
    outw = widgets.Output()
    display(outw)
    return outw


def hr_diagram_skyviewer(cluster_name):
    """
    """
    cluster = get_hr_data(cluster_name)
    text_input = cluster_text_input(cluster)
    pf = hr_diagram_figure(cluster)
    skyviewer = None


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
            new_x, new_y = absolute_mag(cluster)
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


def hr_diagram_color_helper(temps):
    colors = color(temps)
    color_mapper = CategoricalColorMapper(
        factors=['blue_white',
                 'white',
                 'yellowish_white',
                 'pale_yellow_orange',
                 'light_orange_red'],
        palette=['#CAE1FF',
                 '#F6F6F6',
                 '#FFFEB2',
                 '#FFB28B',
                 '#FF9966'])
    return colors, color_mapper


def hr_diagram_selection(cluster_name):
    """
    Given a cluster create two Bokeh plot based H-R diagrams.
    The Selection in the left H-R diagram will show up on the
    right one.
    """
    cluster = get_hr_data(cluster_name)
    temps, lums = teff(cluster), luminosity(cluster)
    x, y = temps, lums
    colors, color_mapper = hr_diagram_color_helper(temps)
    x_range = [max(x) + max(x) * 0.05, min(x) - min(x) * 0.05]
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors), name='hr')
    source_selected = ColumnDataSource(data=dict(x=[], y=[], color=[]),
                                       name='hr')
    pf = figure(y_axis_type='log', x_range=x_range,
                tools='lasso_select,reset',
                title='H-R Diagram for {0}'.format(cluster.name))
    _diagram(source=source, plot_figure=pf, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    pf_selected = figure(y_axis_type='log', y_range=pf.y_range,
                         x_range=x_range,
                         tools="reset",
                         title='H-R Diagram for {0}'.format(cluster.name))
    _diagram(source=source_selected, plot_figure=pf_selected, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    source.callback = CustomJS(args=dict(source_selected=source_selected), code="""
        var inds = cb_obj.selected['1d'].indices;
        var d1 = cb_obj.data;
        var d2 = source_selected.data;
        console.log(inds);
        d2['x'] = []
        d2['y'] = []
        d2['color'] = []
        for (i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
            d2['color'].push(d1['color'][inds[i]])
        }
        source_selected.change.emit();
        """)
    show(row(pf, pf_selected))
