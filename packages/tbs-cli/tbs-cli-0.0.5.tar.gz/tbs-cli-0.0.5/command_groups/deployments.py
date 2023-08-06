import time
import click
import swagger_client
from tbscli.decorators import instantiate_context, print_result
RUNTIME_ALIASES = {'python2.7': "04a08704-34a2-45c7-9a5e-1b42faed169a"}
FRAMEWORK_ALIASES = {'tensorflow': "8fc02450-a3e9-4a98-9b66-173e489e6b55",
                     'tensorflow1.4': "8fc02450-a3e9-4a98-9b66-173e489e6b55"}


@click.command(help="This is the deployment help")
# TODO: Is there a cleaner way to define all these options? This is gross.
# TODO: Define help for all these flags
@click.option("--namespace")
@click.option("--project")
@click.option("--name")
@click.option("--handler")
@click.option("--files")
@click.option("--runtime")
@click.option("--framework")
@instantiate_context
@print_result
def deploy_cmd(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj.get('namespace')
    if namespace is None:
        namespace = click.prompt("Namespace", type=str)

    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'

    project_name = kwargs.get("project")
    if project_name is None:
        project_name = click.prompt("Project", type=str)

    deployment_name = click.prompt("Name", type=str)
    handler = click.prompt("Handler Function", type=str)
    files = click.prompt("Files", type=str)
    runtime = click.prompt("Runtime", type=str)
    framework = click.prompt("Framework", type=str)

    config = swagger_client.DeploymentConfig(handler=handler,
                                             files=[f.strip() for f in files.split(",")])

    deployment_data = {'name': deployment_name,
                       'config': config,
                       'runtime': RUNTIME_ALIASES[runtime],
                       'framework': FRAMEWORK_ALIASES[framework]}

    deploy_data = swagger_client.DeploymentData(**deployment_data)

    deployments_api = swagger_client.DeploymentsApi()
    initial_response = deployments_api.deployments_create(namespace=namespace,
                                                          project=project_name,
                                                          deployment_data=deploy_data)

    response = deployments_api.deployments_deploy(namespace=namespace,
                                                  project=project_name,
                                                  deployment=initial_response.name)
    click.echo("Deploying...")
    time.sleep(10)

    final_response = deployments_api.deployments_read(project=project_name,
                                                      namespace=namespace,
                                                      deployment=initial_response.name)
    return final_response


# TODO: Is there a way to do this with inheritance? We lose context of globals()...
class DeploymentsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage model deployments"
        super(DeploymentsCLI, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        commands = [key.replace("_cmd", "") for key in globals() if key.endswith("_cmd")]
        return commands

    def get_command(self, ctx, cmd_name):
        return globals().get(cmd_name + "_cmd")
