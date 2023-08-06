import os
import json
import click
import tbs_client
import inspect
from pathlib import Path


def istbscommand(obj):
    return (inspect.isclass(obj)
            and issubclass(obj, ThreeBladesBaseCommand)
            and obj != ThreeBladesBaseCommand)


class ThreeBladesBaseCommand(click.Command):
    def __init__(self, name, params=list, api_class=None, help=""):
        super(ThreeBladesBaseCommand, self).__init__(name=name,
                                                     params=params,
                                                     help=help,
                                                     callback=self._full_command)
        self.context = {}
        home_dir = os.getenv("HOME")
        config_file = Path(home_dir, ".threeblades.config")
        if config_file.exists():
            with config_file.open() as conf_file:
                line = conf_file.read()
                conf_json = json.loads(line)
                self.context['token'] = conf_json['token']
                self.context['namespace'] = conf_json.get('namespace')
        tbs_client.configuration.api_key['Authorization'] = self.context['token']
        tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
        self.api_client = api_class()

    def _cmd(self, *args, **kwargs):
        raise NotImplementedError("All subclasses of ThreeBladesBaseCommand must "
                                  "define the _cmd method.")

    def _validate_params(self, *args, **kwargs):
        return args, kwargs

    def _full_command(self, *args, **kwargs):
        new_args, new_kwargs = self._validate_params(*args, **kwargs)
        self._cmd(*new_args, **new_kwargs)

    def invoke(self, ctx):
        if self.callback is not None:
            return ctx.invoke(self.callback, **ctx.params)
