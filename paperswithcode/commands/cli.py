import os

import click

from paperswithcode import consts
from paperswithcode.config import Config
from paperswithcode.client import Client


@click.group()
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True),
    envvar="PAPERSWITHCODE_CONFIG",
    help="Path to the alternative configuration file.",
)
@click.option(
    "--profile",
    default="default",
    envvar="PAPERSWITHCODE_PROFILE",
    help="Configuration file profile.",
)
@click.pass_context
def cli(ctx, config_path, profile):
    """PapersWithCode command line client."""
    if config_path is None:
        config_path = os.path.expanduser(consts.DEFAULT_CONFIG_PATH)
    ctx.obj = Config(config_path, profile)


@cli.command("login")
@click.pass_obj
def login(config: Config):
    """Obtain authentication token."""
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    client = Client(config)
    config.token = client.login(username=username, password=password)
    config.save()
