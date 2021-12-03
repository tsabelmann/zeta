"""This module implements a CLI for the zeta module."""

import click
import pathlib
import toml
from zeta import backend

class BasedIntParamType(click.ParamType):
    name = 'integer'

    def convert(self, value, param, ctx):
        try:
            if type(value) == int:
                return value
            else:
                if value[:2].lower() == '0x':
                    return int(value[2:], 16)
                elif value[:1] == '0':
                    return int(value, 8)
                return int(value, 10)
        except ValueError:
            self.fail('%s is not a valid integer' % value, param, ctx)


BASED_INT = BasedIntParamType()


@click.group()
def main():
    pass


@main.command()
def version():
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
        name = pyproject["tool"]["poetry"]["name"]
        vers = pyproject["tool"]["poetry"]["version"]
        print(f"{name} {vers}")


@main.command()
@click.argument("file_path", type=pathlib.Path)
@click.option("-w", "--w", "--width", "width", type=click.INT, default=1920)
@click.option("-h", "--h", "--height", "height", type=click.INT, default=1080)
@click.option("-bg", "--bg", "--background", "background", type=BASED_INT, default=0x000000)
@click.option("-fg", "--fg", "--foreground", "foreground", type=BASED_INT, default=0xFCFE5B)
def create(file_path: pathlib.Path, width: int, height: int, background, foreground):
    # construct absolute path
    file_path = file_path.absolute()

    # create parent directory
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # if file_path.is_file():
    #     pass
    # else:
    #     print("ERROR")

    # create zeta function image file
    image = backend.CriticalZeta(file_path, background, foreground, width, height)
    image.generate()
