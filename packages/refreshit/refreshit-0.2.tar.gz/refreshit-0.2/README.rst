refreshit
=========
A print to always print in the same line, refreshing the content

Setup
-----

.. code-block:: bash

    $ pip install refreshit

Code sample
-----------

Refreshing some text

.. code-block:: python

    from refreshit import uprint
    from time import sleep

    uprint("Beautiful is better than ugly.")
    sleep(1)
    uprint("Explicit is better than implicit.\n")
    sleep(1)

Loading state

.. code-block:: python

    from refreshit import uprint
    from time import sleep

    load = ["Loading", "Loading.", "Loading..", "Loading..."]
    for i in range(4):
        for item in load:
            uprint(item)
            sleep(0.2)
    uprint("Complete\n")


A progress bar

.. code-block:: python

    from refreshit import uprint
    from time import sleep

    n = 20
    squares = [u"\u25A0"*x+" "+"{:.0f}".format((x/(n-1))*100)+"%" for x in range(n)]
    for i in range(2):
        for item in squares:
            uprint(item)
            sleep(0.1)
    print()
