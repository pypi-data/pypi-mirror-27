py-discover - Discover nodes in different Cloud providers
=========================================================

[![Build Status](https://travis-ci.org/nir0s/py-discover.svg?branch=master)](https://travis-ci.org/nir0s/py-discover)
[![Build status](https://ci.appveyor.com/api/projects/status/e812qjk1gf0f74r5/branch/master?svg=true)](https://ci.appveyor.com/project/nir0s/py-discover/branch/master)
[![PyPI version](http://img.shields.io/pypi/v/py-discover.svg)](https://pypi.python.org/pypi/py-discover)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/py-discover.svg)](https://img.shields.io/pypi/pyversions/py-discover.svg)
[![Requirements Status](https://requires.io/github/nir0s/py-discover/requirements.svg?branch=master)](https://requires.io/github/nir0s/py-discover/requirements/?branch=master)
[![Code Coverage](https://codecov.io/github/nir0s/py-discover/coverage.svg?branch=master)](https://codecov.io/github/nir0s/py-discover?branch=master)
[![Code Quality](https://landscape.io/github/nir0s/py-discover/master/landscape.svg?style=flat)](https://landscape.io/github/nir0s/py-discover)
[![Is Wheel](https://img.shields.io/pypi/wheel/py-discover.svg?style=flat)](https://pypi.python.org/pypi/py-discover)




## Installation

Installation of the latest released version from PyPI:

```shell
pip install py-discover
```

Installation of the latest development version:

```shell
pip install https://github.com/nir0s/py-discover/archive/master.tar.gz
```


## Usage

```
$ python
>>> import discover
>>> discover.nodes(provider=aws, profile='default', tag_key=Name, tag_value=nomad-server)
['172.16.30.44', '172.16.25.8', '172.16.32.16']
```


## Testing

```shell
git clone git@github.com:nir0s/py-discover.git
cd py-discover
pip install tox
tox
```
