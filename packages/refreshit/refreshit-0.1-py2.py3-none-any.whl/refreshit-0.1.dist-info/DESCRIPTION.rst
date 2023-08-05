refreshit
===========
A print to always print in the same line, refreshing the content

Setup
-----

.. code-block:: bash

    $ pip install refreshit

Code sample
-----

.. code-block:: python

    from refreshit import uprint
    from time import sleep

    uprint("Beautiful is better than ugly.")
    sleep(1)
    uprint("Explicit is better than implicit.\n")
    sleep(1)


