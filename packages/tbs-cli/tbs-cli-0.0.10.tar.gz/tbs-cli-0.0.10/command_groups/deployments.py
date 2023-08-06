import time
import click
import tbs_client
from command_groups import (ThreeBladesBaseCommand,
                            istbscommand)
RUNTIME_ALIASES = {'python2.7': "04a08704-34a2-45c7-9a5e-1b42faed169a"}
FRAMEWORK_ALIASES = {'tensorflow': "8fc02450-a3e9-4a98-9b66-173e489e6b55",
                     'tensorflow1.4': "8fc02450-a3e9-4a98-9b66-173e489e6b55"}


class DeploymentsDetailsCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [click.Option(param_decls=["--namespace"]),
                   click.Option(param_decls=["--project"]),
                   click.Option(param_decls=["--deployment"])]
        self.context = {}
        super(DeploymentsDetailsCommand, self).__init__(name="details",
                                                        params=options,
                                                        help="Get details for a given deployment",
                                                        api_class=tbs_client.DeploymentsApi)

    def _validate_params(self, *args, **kwargs):
        # This _could_ be refactored to the parent class, but I think that might be
        # a bit too magical and would probably get it wrong sometimes
        namespace = kwargs.get('namespace') or self.context.get('namespace')
        if namespace is None:
            namespace = click.prompt("Namespace", type=str)
        kwargs['namespace'] = namespace

        project_name = kwargs.get("project")
        if project_name is None:
            project_name = click.prompt("Project", type=str)
        kwargs['project'] = project_name

        deployment_identifier = kwargs.get('deployment')
        if deployment_identifier is None:
            deployment_identifier = click.prompt("Deployment", type=str)
        kwargs['deployment'] = deployment_identifier

        return args, kwargs

    def _cmd(self, *args, **kwargs):
        response = self.api_client.deployments_read(**kwargs)
        print(response)


class DeploymentsCreateCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [click.Option(param_decls=["--namespace"]),
                   click.Option(param_decls=["--project"]),
                   click.Option(param_decls=["--name"]),
                   click.Option(param_decls=["--handler"]),
                   click.Option(param_decls=["--files"]),
                   click.Option(param_decls=["--runtime"]),
                   click.Option(param_decls=["--framework"])]
        self.context = {}
        super(DeploymentsCreateCommand, self).__init__(name="create",
                                                       params=options,
                                                       help="Create and deploy a model as a RESTful endpoint",
                                                       api_class=tbs_client.DeploymentsApi)

    def _validate_params(self, *args, **kwargs):
        namespace = kwargs.get('namespace') or self.context.get('namespace')
        if namespace is None:
            namespace = click.prompt("Namespace", type=str)
        kwargs['namespace'] = namespace

        project_name = kwargs.get("project")
        if project_name is None:
            project_name = click.prompt("Project", type=str)
        kwargs['project'] = project_name

        name = kwargs.get("name")
        if name is None:
            name = click.prompt("Name", type=str)
        kwargs['name'] = name

        handler = kwargs.get('handler')
        if handler is None:
            handler = click.prompt("Handler Function", type=str)
        kwargs['handler'] = handler

        files = kwargs.get('files')
        if files is None:
            files = click.prompt("Files", type=str)
        kwargs['files'] = files

        runtime = kwargs.get('runtime')
        if runtime is None:
            runtime = click.prompt("Runtime", type=str)
        kwargs['runtime'] = RUNTIME_ALIASES[runtime]

        framework = kwargs.get('framework')
        if framework is None:
            framework = click.prompt("Framework", type=str)
        kwargs['framework'] = FRAMEWORK_ALIASES[framework]

        return args, kwargs

    def _cmd(self, *args, **kwargs):
        config = tbs_client.DeploymentConfig(handler=kwargs.get('handler'),
                                             files=[f.strip() for f in kwargs.get('files').split(",")])
        deployment_data = {'name': kwargs.get('name'),
                           'config': config,
                           'runtime': kwargs.get('runtime'),
                           'framework': kwargs.get('framework')}
        deploy_data = tbs_client.DeploymentData(**deployment_data)
        initial_response = self.api_client.deployments_create(namespace=kwargs.get('namespace'),
                                                              project=kwargs.get('project'),
                                                              deployment_data=deploy_data)
        response = self.api_client.deployments_deploy(namespace=kwargs.get('namespace'),
                                                      project=kwargs.get('project'),
                                                      deployment=initial_response.name)
        click.echo("Deploying...")
        # TODO: Add a status bar here
        time.sleep(10)
        final_response = self.api_client.deployments_read(project=kwargs.get('project'),
                                                          namespace=kwargs.get('namespace'),
                                                          deployment=initial_response.name)
        click.echo(final_response)


class DeploymentsDeleteCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [click.Option(param_decls=["--namespace"]),
                   click.Option(param_decls=["--project"]),
                   click.Option(param_decls=["--deployment"])]
        self.context = {}
        super(DeploymentsDeleteCommand, self).__init__(name="delete",
                                                       params=options,
                                                       help="Delete a given deployment",
                                                       api_class=tbs_client.DeploymentsApi)

    def _validate_params(self, *args, **kwargs):
        namespace = kwargs.get('namespace') or self.context.get('namespace')
        if namespace is None:
            namespace = click.prompt("Namespace", type=str)
        kwargs['namespace'] = namespace

        project_name = kwargs.get("project")
        if project_name is None:
            project_name = click.prompt("Project", type=str)
        kwargs['project'] = project_name

        deployment_identifier = kwargs.get('deployment')
        if deployment_identifier is None:
            deployment_identifier = click.prompt("Deployment to delete", type=str)
        kwargs['deployment'] = deployment_identifier

        return args, kwargs

    def _cmd(self, *args, **kwargs):
        response = self.api_client.deployments_delete(**kwargs)
        if response is None:
            print(f"Deployment {kwargs['deployment']} deleted successfully.")
        else:
            print(response)


class DeploymentsListCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [click.Option(param_decls=["--namespace"]),
                   click.Option(param_decls=["--project"])]
        self.context = {}
        super(DeploymentsListCommand, self).__init__(name="list",
                                                     params=options,
                                                     help="List all deployments for a given project",
                                                     api_class=tbs_client.DeploymentsApi)

    def _validate_params(self, *args, **kwargs):
        # This _could_ be refactored to the parent class, but I think that might be
        # a bit too magical and would probably get it wrong sometimes
        namespace = kwargs.get('namespace') or self.context.get('namespace')
        if namespace is None:
            namespace = click.prompt("Namespace", type=str)
        kwargs['namespace'] = namespace

        project_name = kwargs.get("project")
        if project_name is None:
            project_name = click.prompt("Project", type=str)
        kwargs['project'] = project_name

        return args, kwargs

    def _cmd(self, *args, **kwargs):
        response = self.api_client.deployments_list(**kwargs)
        print(response)


class DeploymentsUpdateCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [click.Option(param_decls=["--namespace"]),
                   click.Option(param_decls=["--project"]),
                   click.Option(param_decls=["--deployment"]),
                   click.Option(param_decls=["--name"]),
                   click.Option(param_decls=["--handler"]),
                   click.Option(param_decls=["--files"]),
                   click.Option(param_decls=["--runtime"]),
                   click.Option(param_decls=["--framework"])]
        self.context = {}
        self.deployment = None
        super(DeploymentsUpdateCommand, self).__init__(name="update",
                                                       params=options,
                                                       help="Update a given deployment",
                                                       api_class=tbs_client.DeploymentsApi)

    def _validate_params(self, *args, **kwargs):
        namespace = kwargs.get('namespace') or self.context.get('namespace')
        if namespace is None:
            namespace = click.prompt("Namespace", type=str)
        kwargs['namespace'] = namespace

        project_name = kwargs.get("project")
        if project_name is None:
            project_name = click.prompt("Project", type=str)
        kwargs['project'] = project_name

        deployment_identifier = kwargs.get('deployment')
        if deployment_identifier is None:
            deployment_identifier = click.prompt("Deployment to update", type=str)
        kwargs['deployment'] = deployment_identifier

        self.deployment = self.api_client.deployments_read(namespace=kwargs['namespace'],
                                                           project=kwargs['project'],
                                                           deployment=kwargs['deployment'])

        return args, kwargs

    def _cmd(self, *args, **kwargs):
        click.echo("Leave fields blank to maintain their current values.")

        name = kwargs.get("name")
        if name is None:
            name = click.prompt("Name",
                                type=str,
                                default=self.deployment.name)

        handler = kwargs.get('handler')
        if handler is None:
            handler = click.prompt("Handler Function",
                                   type=str,
                                   default=self.deployment.config['handler'])

        files = kwargs.get('files')
        if files is None:
            files = click.prompt("Files",
                                 type=str,
                                 default=self.deployment.config['files'],
                                 show_default=False)
            if isinstance(files, str):
                # The user entered a new list of files. If they left the default,
                # files is of type list
                files = [f.strip() for f in files.split(",")]

        runtime = kwargs.get('runtime')
        if runtime is None:
            runtime = click.prompt("Runtime",
                                   type=str,
                                   default=self.deployment.runtime)

        framework = kwargs.get('framework')
        if framework is None:
            framework = click.prompt("Framework",
                                     type=str,
                                     default=self.deployment.framework)

        config = tbs_client.DeploymentConfig(handler=handler,
                                             files=files)

        deployment_data = tbs_client.DeploymentData(name=name,
                                                    runtime=RUNTIME_ALIASES.get(runtime) or runtime,
                                                    framework=FRAMEWORK_ALIASES.get(framework) or framework,
                                                    config=config)

        response = self.api_client.deployments_update(namespace=kwargs['namespace'],
                                                      project=kwargs['project'],
                                                      deployment=kwargs['deployment'],
                                                      deployment_data=deployment_data)
        print(response)


# TODO: Is there a way to do this with inheritance? We lose context of globals()...
class DeploymentsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage model deployments"
        super(DeploymentsCLI, self).__init__(*args, **kwargs)
        self.commands = {value().name: value for key, value in globals().items() if istbscommand(value)}

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, cmd_name):
        return self.commands.get(cmd_name)()
