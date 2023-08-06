import click
import pkgutil
import command_groups
from importlib import import_module
from command_groups import login


class ThreeBladesCLI(click.Group):
    def list_commands(self, ctx):
        commands = ["login"]
        for _, modname, ispkg in pkgutil.iter_modules(command_groups.__path__):
            if not ispkg:
                cmd_name = modname
                commands.append(cmd_name)
        commands.sort()
        return commands

    def get_command(self, ctx, cmd_name):
        if cmd_name != "login":
            module = import_module(f"command_groups.{cmd_name}")
            cmd_group = getattr(module, cmd_name.title() + "CLI")()
            return cmd_group
        else:
            return login


my_cli = ThreeBladesCLI(help="Command line tools for 3Blades")


def main():
    return my_cli()
