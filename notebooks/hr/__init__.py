from .data import get_hr_data
from .visual import hr_diagram

import bokeh.io
import bokeh.resources

import logging


def setup_notebook(debug=False):
    """Called at the start of notebook execution to setup the environment.

    This will configure bokeh, and setup the logging library to be
    reasonable."""
    bokeh.io.output_notebook(bokeh.resources.INLINE, hide_banner=True)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Running notebook in debug mode.')
