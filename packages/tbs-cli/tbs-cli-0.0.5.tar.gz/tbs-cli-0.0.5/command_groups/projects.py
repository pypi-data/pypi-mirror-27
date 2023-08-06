import swagger_client
import click
from tbscli.decorators import instantiate_context, print_result


# TODO: Consider combining all these decorators into one. Would be a lot less verbose
@click.command()
@click.option("--namespace")
@instantiate_context
@print_result
def detail_cmd(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_name = click.prompt("Project")
    projects_api = swagger_client.ProjectsApi()
    response = projects_api.projects_read(namespace, project_name)
    return response


@click.command()
@click.option("--namespace")
@instantiate_context
@print_result
def list_cmd(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    projects_api = swagger_client.ProjectsApi()
    response = projects_api.projects_list(namespace=namespace)
    return response


@click.command()
@click.option("--namespace")
@instantiate_context
@print_result
def create_cmd(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    name = click.prompt("Project name", type=str)
    description = click.prompt("Description", type=str)
    private = click.prompt("Private", type=bool)
    proj_data = {'name': name,
                 'description': description,
                 'private': private}
    project_data = swagger_client.ProjectData(**proj_data)

    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'

    project_api = swagger_client.ProjectsApi()
    response = project_api.projects_create(namespace, project_data=project_data)
    return response


@click.command()
@click.option("--namespace")
@instantiate_context
@print_result
def delete_cmd(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_api = swagger_client.ProjectsApi()
    project_name = click.prompt("Name of project to delete")
    click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
    response = project_api.projects_delete(namespace, project=project_name)
    return response


class ProjectsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage account projects"
        super(ProjectsCLI, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        commands = [key.replace("_cmd", "") for key in globals() if key.endswith("_cmd")]
        return commands

    def get_command(self, ctx, cmd_name):
        return globals().get(cmd_name + "_cmd")

