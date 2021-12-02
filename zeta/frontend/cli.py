"""This module implements a CLI for the zeta module."""

import click
import toml


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
