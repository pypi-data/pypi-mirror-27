import os
import json
import click
import swagger_client
from pathlib import Path
from tbscli.decorators import instantiate_context, print_result


@click.command()
@instantiate_context
@print_result
def login_cmd(ctx, *args, **kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    home_dir = os.getenv("HOME")
    config_file = Path(home_dir, ".threeblades.config")
    if config_file.exists():
        click.echo(".threeblades.config file already exists in $HOME directory. "
                   "Using that to login.")
        with config_file.open() as conf:
            line = conf.read()
            conf_json = json.loads(line)
            ctx.obj['token'] = conf_json['token']
            ctx.obj['namespace'] = conf_json.get('namespace', None)
    else:
        if not (username and password):
            username = click.prompt("Username", type=str)
            password = click.prompt("Password", type=str, hide_input=True)
        auth_api = swagger_client.AuthApi()
        jwt_data = swagger_client.JWTData(username=username,
                                          password=password)
        response = auth_api.auth_jwt_token_auth(jwt_data=jwt_data)

        config = {'token': response.token,
                  'namespace': username}

        ctx.obj['token'] = response.token
        ctx.obj['namespace'] = username
        with open(config_file, "w") as tok_file:
            tok_file.write(json.dumps(config))

        click.echo(f"Welcome {username}.")

    click.echo("Login successful")
    return (f"Using {ctx.obj.get('namespace')} as a default namespace. "
            f"Override this with the --namespace flag.")


class AuthCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage auth actions"
        super(AuthCLI, self).__init__(*args, **kwargs)
    def list_commands(self, ctx):
        commands = [key.replace("_cmd", "") for key in globals() if key.endswith("_cmd")]
        return commands

    def get_command(self, ctx, cmd_name):
        return globals().get(cmd_name + "_cmd")
