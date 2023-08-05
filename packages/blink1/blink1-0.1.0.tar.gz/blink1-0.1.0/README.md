

Python3 Blink(1) library
========================

Official Python library for blink(1) USB RGB LED notification devices
https://blink1.thingm.com/

About this library
------------------

This is a rewrite of the original Python library. It includes the following modifications:

* 100% test coverage on all library components
* Python 3.x compatible
* Automatic installation via Python Package Index.
* Higher level control over the blink(1).
* Single implementation with `pyhidapi` (instead of PyUSB), intended to be installed with admin access or virtualenv.

This library lives at https://github.com/todbot/blink1-python

Originally written by @salimfadhley, at https://github.com/salimfadhley/blink1/tree/master/python/pypi.
Moved to this repository and rewritten for `pyhidapi` by @todbot.

Installation
------------

Use the pip utility to fetch the latest release of this package and any additional components required in a single step:

    pip install blink1

Developer installation
----------------------

Having checked out the blink1-python library, cd to it and run the setup script:

    git clone https://github.com/todbot/blink1-python
    cd blink1-python
    python3 setup.py develop
    python3 ./blink1_demo/demo1.py

You can now use the `blink1` package on your system. To uninstall the development version:

    python setup.py develop --uninstall


Use
---

The simplest way to use this library is via a context manager.

    import time
    from blink1.blink1 import blink1

    with blink1() as b1:
        b1.fade_to_color(100, 'navy')
        time.sleep(10)

When the blink1() block exits the light is automatically switched off.
It is also possible to access the exact same set of functions without the context manager:

    from blink1.blink1 import Blink1
        import time

        b1 = Blink1()
        b1.fade_to_rgb(1000, 64, 64, 64)
        time.sleep(3)
        b1.fade_to_rgb(1000, 255, 255, 255)

Unlike the context manager, this demo will leave the blink(1) open at the end of execution.
To close it, use the `b1.close()` method.

Colors
------

There are a number of ways to specify colors in this library:

    b1.fade_to_color(1000, '#ffffff') # Hexdecimal RGB as a string
    b1.fade_to_color(1000, 'green') # Named color - any color name understood by css3
    b1.fade_to_color(1000, (22,33,44) # RGB as a tuple. Luminance values are 0 <= lum <= 255

Attempting to select a color outside the plausible range will generate an InvalidColor exception.

Gamma correction
----------------

The context manager supports a ''gamma'' argument which allows you to supply a per-channel gamma correction value.

    from blink1.blink1 import blink1

    with blink1(gamma=(2, 2, 2)) as b1:
        b1.fade_to_color(100, 'pink')
        time.sleep(10)

This example provides a gamma correction of 2 to each of the three colour channels.

Higher values of gamma make the blink(1) appear more colorful but decrease the brightness of colours.

White point correction
----------------------

The human eye's perception of color can be influenced by ambient lighting. In some circumstances it may be desirable
to apply a small colour correction in order to make colors appear more accurate. For example, if we were operating
the blink(1) in a room lit predimenantly by candle-light:

    with blink1(white_point='candle', switch_off) as b1:
        b1.fade_to_color(100, 'white')

Viewed in daylight this would make the Blink(1) appear yellowish, hoever in a candle-lit room this would be perceived
as a more natural white. If we did not apply this kind of color correction the Blink(1) would appear blueish.

The following values are acceptable white-points:

* Any triple of (r,g,b). Each 0 <= luminance <= 255
* Any color_temperature expressed as an integer or float in Kelvin
* A color temperature name.

The library supports the following temperature names:

* candle
* sunrise
* incandescent
* tungsten
* halogen
* sunlight
* overcast
* shade
* blue-sky
