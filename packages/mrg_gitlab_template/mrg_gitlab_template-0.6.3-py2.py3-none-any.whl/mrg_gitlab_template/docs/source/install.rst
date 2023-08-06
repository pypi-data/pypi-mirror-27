Installation
************

To install, simply use ``pip``:

.. code-block:: bash

   pip install {{package}}

To upgrade {{package}} to the latest version:

.. code-block:: bash

   pip install --upgrade --no-cache-dir {{package}}

If the package is hosted on your own pypi server then the following command
will need to be constructed,

.. code-block:: bash

   set PYPI_HOST=lab-linux-server.estec.esa.int
   pip install --extra-index-url=http://$PYPI_HOST/pypi/simple --trusted-host=$PYPI_HOST {{package}}

or,

.. code-block:: bash

    pip install --index-url=http://$PYPI_HOST/pypi/simple --trusted-host=$PYPI_HOST {{package}}
