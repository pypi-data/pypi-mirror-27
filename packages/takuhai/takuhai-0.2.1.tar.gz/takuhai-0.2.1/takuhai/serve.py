from functools import partial

from livereload import Server
from pelican import Pelican
from pelican.settings import read_settings


def build(pelican):
    try:
        pelican.run()
    except SystemExit as e:
        pass


def serve(host, port, open_url=False):
    settings = read_settings('pelicanconf.py')
    settings['RELATIVE_URLS'] = True
    pelican = Pelican(settings)

    _build = partial(build, pelican)
    _build()

    server = Server()
    server.watch(pelican.settings['PATH'], _build)
    server.watch(pelican.settings['THEME'], _build)
    server.watch('./pelicanconf.py', _build)

    server.serve(host=host, port=port, root=settings['OUTPUT_PATH'],
                 open_url_delay=open_url)


def main():
    serve(host='localhost', port='8000')


if __name__ == '__main__':
    main()
