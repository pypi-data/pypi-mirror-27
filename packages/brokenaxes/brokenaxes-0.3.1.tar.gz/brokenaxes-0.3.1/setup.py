from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os


long_description = \
"""# brokenaxes

![brokenaxes logo. Reference: http://www.brianhensley.net/2012/02/python-controlling-spi-bus-on.html](broken_python_snake.png)

brokenaxes makes matplotlib plots with breaks in the axes for showing data across a discontinuous range.

[![PyPI](https://img.shields.io/pypi/v/brokenaxes.svg?style=plastic)](https://pypi.python.org/pypi/brokenaxes)

## Installation
I recommend the [Anaconda python distribution](http://continuum.io/downloads)
```
pip install brokenaxes
```

## Usage
```python
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import numpy as np

fig = plt.figure(figsize=(5,2))
bax = brokenaxes(xlims=((0, .1), (.4, .7)), ylims=((-1, .7), (.79, 1)), hspace=.05)
x = np.linspace(0, 1, 100)
bax.plot(x, np.sin(10 * x), label='sin')
bax.plot(x, np.cos(10 * x), label='cos')
bax.legend(loc=3)
bax.set_xlabel('time')
bax.set_ylabel('value')
```
![example1](example1.png)

Create subplots:

```python
from brokenaxes import brokenaxes
from matplotlib.gridspec import GridSpec
import numpy as np

sps1, sps2 = GridSpec(2,1)

bax = brokenaxes(xlims=((.1, .3),(.7, .8)), subplot_spec=sps1)
x = np.linspace(0, 1, 100)
bax.plot(x, np.sin(x*30), ls=':', color='m')

x = np.random.poisson(3, 1000)
bax = brokenaxes(xlims=((0, 2.5), (3, 6)), subplot_spec=sps2)
bax.hist(x, histtype='bar')
```
![example2](example2.png)

### Features:
* Break x and y axes.
* Supports multiple breaks on a single axis.
* Automatically scales axes according to relative ranges.
* Plot multiple lines.
* Legend with positioning relative to entire broken axes object
* x and y label centered to entire plot
* Make brokenaxes object a subplot itself with `matplotlib.GridSpec.subplot_spec`.
* xlims and ylims may be datetime.datetime objects

### Life advice
Please use this tool wisely. Any data visaulization techique can be used to elucidate trends in the data, and can be used to manipulate and mislead. The latter is particularly true for broken axes plots, so please try to use them responsibly. Other than that, this software is free to use for any purpose.
"""


setup(
    name='brokenaxes',
    version='0.3.1',
    description='Create broken axes',
    long_description=long_description,
    author='Ben Dichter',
    author_email='ben.dichter@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='data visualization',

    #packages=find_packages(exclude=['docs']),
    py_modules=["brokenaxes"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['matplotlib'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    #    'dev': ['check-manifest'],
        'test': ['pytest'],
    },


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)
