import swagger_client
import click


def detail(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_name = click.prompt("Project")
    projects_api = swagger_client.ProjectsApi()
    response = projects_api.projects_read(namespace, project_name)
    return response


def list(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    projects_api = swagger_client.ProjectsApi()
    response = projects_api.projects_list(namespace=namespace)
    return response


def create(ctx, *args, **kwargs):
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


def delete(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_api = swagger_client.ProjectsApi()
    project_name = click.prompt("Name of project to delete")
    click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
    response = project_api.projects_delete(namespace, project=project_name)
    return response

