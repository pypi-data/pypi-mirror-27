import os
import json
import click
from importlib import import_module
from pprint import pprint
from pathlib import Path

# TODO: Clean up how arguments/options are passed to subcommands.
# It's not great at the moment

# TODO: Refactor to keep it DRY


def invoke_command(ctx, module_name, *args, **kwargs):
    sub_command = kwargs['sub_command']
    try:
        command_func = getattr(import_module(f"command_groups.{module_name}"), sub_command)
    except AttributeError:
        click.echo(f"Invalid sub-command: {sub_command}")
        raise
    response = command_func(ctx, *args, **kwargs)
    if response is not None:
        pprint(response)


@click.group()
@click.pass_context
def cli(ctx):
    home_dir = os.getenv("HOME")
    config_file = Path(home_dir, ".threeblades.config")
    if config_file.exists():
        with config_file.open() as conf_file:
            line = conf_file.read()
            conf_json = json.loads(line)
            ctx.obj['token'] = conf_json['token']
            ctx.obj['namespace'] = conf_json.get('namespace')


@click.command()
@click.option("--username")
@click.option("--password")
@click.pass_context
def login(ctx, *args, **kwargs):
    kwargs['sub_command'] = "login"
    invoke_command(ctx, "auth_cli", *args, **kwargs)


@click.command()
# TODO: Make namespace optional, defaulting to that of the user that is currently logged in.
# TODO: Add the various parameters?
@click.argument("sub_command")
@click.option("--namespace", prompt="Namespace")
@click.pass_context
def projects(ctx, *args, **kwargs):
    if "token" not in ctx.obj:
        click.echo("Make sure you've logged in first!")
    invoke_command(ctx, "projects_cli", *args, **kwargs)


@click.command()
@click.argument("sub_command")
@click.option("--namespace")
@click.option("--project")
@click.pass_context
# @click.option("--framework")
# @click.option("--files")
def deployments(ctx, *args, **kwargs):
    if "token" not in ctx.obj:
        click.echo("Make sure you've logged in first!")
    invoke_command(ctx, "deployments_cli", *args, **kwargs)


cli.add_command(login)
cli.add_command(projects)
cli.add_command(deployments)


def main():
    return cli(obj={})
