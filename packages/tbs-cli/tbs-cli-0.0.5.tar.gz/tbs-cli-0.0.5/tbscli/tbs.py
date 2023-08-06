import click
import pkgutil
import command_groups
from importlib import import_module


class ThreeBladesCLI(click.MultiCommand):
    def list_commands(self, ctx):
        commands = []
        for _, modname, ispkg in pkgutil.iter_modules(command_groups.__path__):
            if not ispkg:
                cmd_name = modname
                commands.append(cmd_name)
        commands.sort()
        return commands

    def get_command(self, ctx, cmd_name):
        module = import_module(f"command_groups.{cmd_name}")
        cmd_group = getattr(module, cmd_name.title() + "CLI")()
        return cmd_group


my_cli = ThreeBladesCLI(help="Command line tools for 3Blades")


def main():
    return my_cli()
