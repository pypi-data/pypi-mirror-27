Installation
------------

Using conda
~~~~~~~~~~~

conda install -c conda-forge lagranto


Using pip
~~~~~~~~~

Ideally install it in a virtual environment. See for example virtualenvwrapper_.

.. code:: bash

    pip install Lagranto

Then you can install the dependencies for testing or the documentations as follow:

.. code:: bash

    pip install Lagranto[testing]
    pip install Lagranto[docs]

To build the documentation do the following:

.. code:: bash

    cd /path/to/lagranto/location
    cd docs
    make html

To test the package do the following:

.. code:: bash

    cd /path/to/lagranto/location
    pytest

.. _virtualenvwrapper:  https://virtualenvwrapper.readthedocs.io/en/latest/


.. role:: bash(code)
   :language: bash
