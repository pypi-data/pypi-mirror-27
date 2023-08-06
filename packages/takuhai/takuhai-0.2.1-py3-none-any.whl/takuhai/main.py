import click
from takuhai.serve import serve


@click.command()
@click.option('--host', '-h', default='localhost', help='Host name.')
@click.option('--port', '-p', default='8000', help='Port number.')
@click.option('--open_url', '-o', is_flag=True, help='Open default browser.')
def cli(host, port, open_url):
    serve(host, port, open_url)


def main():
    cli()


if __name__ == '__main__':
    main()
