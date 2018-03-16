.PHONY: all vendors ipyaladin_clone ipyaladin_extensions ipyaladin clean


all: ipyaladin jupyterlab_bokeh

vendors:
	mkdir -p ./vendors

jupyterlab_bokeh:
	jupyter labextension install jupyterlab_bokeh

ipyaladin_clone:
	-git clone https://github.com/cds-astro/ipyaladin.git ./vendors/ipyaladin

ipyaladin_python:
	cd ./vendors/ipyaladin/;pip install -e .

ipyaladin_extensions:
	jupyter nbextension enable --py widgetsnbextension
	jupyter nbextension enable --py --sys-prefix ipyaladin
	jupyter labextension install @jupyter-widgets/jupyterlab-manager
	cd ./vendors/ipyaladin/js;jupyter labextension install

ipyaladin: vendors ipyaladin_clone ipyaladin_python ipyaladin_extensions

clean:
	rm -rf ./vendors
