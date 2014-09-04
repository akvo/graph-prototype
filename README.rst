.. 

graph
======================

Quickstart
----------

To bootstrap the project::

    virtualenv graph
    source graph/bin/activate
    cd path/to/graph/repository
    pip install -r requirements.pip
    pip install -e .
    cp graph/settings/local.py.example graph/settings/local.py
    manage.py syncdb --migrate

To start ipython notebook::

    source graph/bin/activate
    python manage.py shell_plus --notebook

Once the notebook starts it will open a browser. Select the example.ipynb in the browser and select 'Cell' -> 'Run All' from the menu.

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.
