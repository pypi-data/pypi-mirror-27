=======
kmdvalg 
=======

What is kmdvalg?
----------------

* It is a wrapper around *BeautifulSoup* to extract data from www.kmdvalg.dk.
* Bokeh map patches are created with *pyshp* from shapefiles.
* The shapefile dataset is: 'Digdag (Kommunal)' downloaded 2017/12/03 from https://download.kortforsyningen.dk.
* The voting information is combined with map information before plotting.

Important links
---------------

* Source code: https://github.com/tlinnet/kmdvalg
* PyPI package: https://pypi.python.org/pypi/kmdvalg

See examples
------------------------

Use **nbviewer.jupyter.org** to:

* See Notebook to list Danske kommuner: get_kommune.ipynb_
* See Notebook to make bokeh map of Kommunevalg 2017: get_kommune_map.ipynb_

.. _get_kommune.ipynb: http://nbviewer.jupyter.org/github/tlinnet/kmdvalg/blob/master/examples/get_kommune.ipynb
.. _get_kommune_map.ipynb: http://nbviewer.jupyter.org/github/tlinnet/kmdvalg/blob/master/examples/get_kommune_map.ipynb

Launch interactive Jupyter Notebook mybinder.org_ to try examples:

.. _mybinder.org: https://mybinder.org/v2/gh/tlinnet/kmdvalg/master

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/tlinnet/kmdvalg/master

.. image:: https://raw.githubusercontent.com/tlinnet/kmdvalg/master/docs/images/image1.png

How to install?
---------------
If using conda, these steps will install an environment

.. code-block:: bash

   # With pip from https://pypi.python.org/pypi/kmdvalg
   pip install kmdvalg

Developer install for local conda environment:

.. code-block:: bash

   # Create environment
   conda env create -f environment.yml
   
   # Activate environment
   conda env list
   source activate kmdvalg
   
   # Enable ipywidgets
   jupyter nbextension list
   jupyter nbextension enable --py widgetsnbextension --sys-prefix

   # Start jupyter
   jupyter notebook

Or manual install in root environment:

.. code-block:: bash

   # Manually install package
   python setup.py install --force
   
   #  Manually uninstall
   python setup.py install --record files.txt
   PACK=`dirname $(head -n 1 files.txt)`
   rm -rf $PACK
   #cat files.txt | xargs rm -rf

Developer
---------

* Guide for upload: http://peterdowns.com/posts/first-time-with-pypi.html
* Updated info: https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
* PyPI test account: http://testpypi.python.org/pypi?%3Aaction=register_form 
* PyPI Live account: http://pypi.python.org/pypi?%3Aaction=register_form

.. code-block:: bash

   # Modify version in: kmdvalg/__init__.py
   
   # Create tag
   VERS=`python -c "from kmdvalg import __version__; print(__version__)"`
   # Adds a tag so that we can put this on PyPI
   git tag $VERS -m ""
   git push --tags origin master
   
   # Upload your package to PyPI Test
   python setup.py sdist upload -r pypitest
   open https://testpypi.python.org/pypi/kmdvalg
   
   # Upload to PyPI Live
   # Once you've successfully uploaded to PyPI Test, perform the same steps but point to the live PyPI server instead.
   python setup.py sdist upload -r pypi
   open https://pypi.python.org/pypi/kmdvalg