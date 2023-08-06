# takuhai Project

Pelican server

---

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Anaconda Version][anaconda-v-image]][anaconda-v-link]
[![Travis][travis-image]][travis-link]

[pypi-v-image]: https://img.shields.io/pypi/v/takuhai.png
[pypi-v-link]: https://pypi.python.org/pypi/takuhai
[anaconda-v-image]: https://anaconda.org/daizutabi/takuhai/badges/version.svg
[anaconda-v-link]: https://anaconda.org/daizutabi/takuhai
[travis-image]: https://img.shields.io/travis/daizutabi/takuhai.svg?style=flat-square&label=Travis+CI
[travis-link]: https://travis-ci.org/daizutabi/takuhai

---

An enhanced version of pelican-livereload.py from [1] and [2].

Reference
---------
[1] [Using LiveReload with Pelican](https://merlijn.vandeen.nl/2015/pelican-livereload.html)
[2] [LiveReload with Pelican](http://tech.agilitynerd.com/livereload-with-pelican.html)


`takuhai` accepts some arguments to configure Pelican's article generation.

+ content: Path to content directory. This path is joined to `PATH` value in
    Pelican's settings dictionary.
+ host and port: Host name and Port number are variable.
+ open_url: If True, a default browser will open.
+ relative: If True, relative URLs are used which are useful when testing
    locally. Thanks to this option, you don't need to change `RELATIVE_URLS`
    of `pelicanconf.py` in developing mode. You can always set `RELATIVE_URLS`
    to False.

Usage
-----

In a Pelican project directory which contains the `pelicanconf.py`.

```bash
> takuhai content
```

To show options,


```bash
> takuhai --help
```
