import click
# from takuhai.convert import convert


@click.group()
def cli():
    pass


@cli.command(name='convert')
def convert_command():
    print(1)


if __name__ == '__main__':
    cli()
