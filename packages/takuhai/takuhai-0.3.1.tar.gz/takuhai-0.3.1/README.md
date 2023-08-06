# Takuhai Project

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Anaconda Version][anaconda-v-image]][anaconda-v-link]
[![Travis][travis-image]][travis-link]

[pypi-v-image]: https://img.shields.io/pypi/v/takuhai.png
[pypi-v-link]: https://pypi.python.org/pypi/takuhai
[anaconda-v-image]: https://anaconda.org/daizutabi/takuhai/badges/version.svg
[anaconda-v-link]: https://anaconda.org/daizutabi/takuhai
[travis-image]: https://img.shields.io/travis/daizutabi/takuhai.svg?style=flat-square&label=Travis+CI
[travis-link]: https://travis-ci.org/daizutabi/takuhai

An enhanced version of pelican-livereload.py from [1] and [2].

Takuhai automatically builds a Pelican project when an article is modified and reload browser pages.

## Reference

1. [Using LiveReload with Pelican](https://merlijn.vandeen.nl/2015/pelican-livereload.html)
2. [LiveReload with Pelican](http://tech.agilitynerd.com/livereload-with-pelican.html)

## Installation

From PyPI

```bash
> pip install takuhai
```


From Anaconda Cloud

```bash
> conda install -c daizutabi -c conda-forge takuhai
```

If you write articles using markdown format, you also need to install `markdown` package:

```bash
> pip install markdown
```
or

```bash
> conda install markdown
```


## Usage

In a Pelican project directory which contains the `pelicanconf.py`

```bash
> takuhai content
```

To show options

```bash
> takuhai --help
```
