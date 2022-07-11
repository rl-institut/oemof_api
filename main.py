"""CLI functionality"""

import click

from fastapi_app import database, settings


@click.group()
def cli():
    """Click group"""


@cli.command()
def create_db():
    """Sets up database and all tables"""
    database.Base.metadata.create_all(settings.engine)


if __name__ == "__main__":
    cli()
