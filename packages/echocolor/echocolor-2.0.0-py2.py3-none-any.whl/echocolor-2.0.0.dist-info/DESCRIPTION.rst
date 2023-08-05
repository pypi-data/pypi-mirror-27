|pipeline status| |coverage report|

Echocolor
=========

Simple Python interface for printing colored text to a terminal.

For the time being, both Python 3 and Python 2.7 are supported. However,
only Python 3 support is guaranteed for the future. But since this
library probably won't have many reasons to change, it's likely that
Python 2.7 will be supported for awhile.

Installation
------------

Install from PyPi:

::

    pip install echocolor


To install for development, clone this repo, then cd into the directory and do ``pip install -e .[dev]``


Running tests
-------------

Without the dev dependencies:

::

    python -m unittest discover tests/

Or in a dev environment to include test coverage:

::

    pip install nose coverage
    nosetests --nocapture --with-coverage --cover-erase --cover-package echocolor --cover-inclusive tests/


Examples
--------

Basic usage would would involve ``echo`` and ``err``, which write to stdout and 
stderr respectively.  The methods available on them are dynamically defined from 
a list of colors (see full list at the end of readme).  ``echo`` and ``err`` 
provide methods for normal foreground and background coloring.  The structure of 
the method names is ``echo.<color>`` for foreground colors, and ``echo.<color>_on_<bgcolor>`` 
for foreground on background colors.

.. code:: python

    from echocolor import echo, err

    echo.cyan("This text will be cyan")
    echo.magenta_on_yellow("This text will be magenta with a yellow background and will look terrible")
    err.light_red("This text will be red and written to stderr instead of stdout")

In addition to colors, bold and underlined text are also possible:

.. code:: python

    echo.bold("This text will be bold")
    echo.underline("And this will be underlined")

If you want to color strings without printing them, import ``colors``:

.. code:: python

    from echocolor import echo
    from echocolor.colors import light_green

    green_text = light_green("This part will be green")
    print("This part will be regular. " + green_text)

However, since the strings end with the escape code to reset all
styling, doing something like the following will result in the second
part of the line being unstyled:

.. code:: python

    from echocolor import echo
    from echocolor.colors import magenta

    echo.underline(magenta("This text will be magenta and underlined.") + " But this text will be unstyled.")

By default, if stdout is being redirected then all the echo output will
be unformatted. That can be changed by setting
``echo.force_color = True``.

Colors
------

The following colors are supported along with any combination of ``<colorX>_on_<colorY>``.  The full list can also be seen from the code by checking the value of ``echocolor.terminal_codes.COLORS``.  

::

    black
    red
    green
    yellow
    blue
    magenta
    cyan
    light_gray
    dark_gray
    light_red
    light_green
    light_yellow
    light_blue
    light_magenta
    light_cyan
    white



.. |pipeline status| image:: https://gitlab.com/danielhones/echocolor/badges/master/pipeline.svg
   :target: https://gitlab.com/danielhones/echocolor/commits/master
.. |coverage report| image:: https://gitlab.com/danielhones/echocolor/badges/master/coverage.svg
   :target: https://gitlab.com/danielhones/echocolor/commits/master


