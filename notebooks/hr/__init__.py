import logging
import os
import urllib

from .data import get_hr_data
from .visual import hr_diagram

import bokeh.io
import bokeh.resources


def setup_notebook(debug=False):
    """Called at the start of notebook execution to setup the environment.

    This will configure bokeh, and setup the logging library to be
    reasonable."""
    bokeh.io.output_notebook(bokeh.resources.INLINE, hide_banner=True)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Running notebook in debug mode.')

def show_with_bokeh_server(obj):
    def jupyter_proxy_url(notebook_url, port):
        base_url = os.environ['EXTERNAL_URL']
        service_url_path = os.environ['JUPYTERHUB_SERVICE_PREFIX']
        proxy_url_path = 'proxy/%d' % port

        user_url = urllib.parse.urljoin(base_url, service_url_path)
        full_url = urllib.parse.urljoin(user_url, proxy_url_path)
        return full_url

    bokeh.io.show(obj, proxy_url_func=jupyter_proxy_url)
