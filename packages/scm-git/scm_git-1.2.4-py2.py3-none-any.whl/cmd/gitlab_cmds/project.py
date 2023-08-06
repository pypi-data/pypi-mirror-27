import click
from utils import try_except, timeit
from cli import cli


@cli.group()
@click.pass_context
def project(ctx):
    ''' GitLab project related operations'''
    pass


@project.command("info")
@click.option('--name', '-n', help="The project name", required=True)
@click.option('--pretty', help="Pretty display the project info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def get_project_info(ctx, name, pretty, time):
    ''' Get project information by a given project name '''
    return ctx.obj['git'].get_project_by_name(name)


@project.command("create")
@click.option('--group_name', '-g', help="The group name", required=True)
@click.option('--project_name', '-p', help="The project name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def create_project(ctx, group_name, project_name, pretty, time):
    ''' Create a project under a group by given group name and project name '''
    return ctx.obj['git'].create_project_under_group_by_group_name(group_name, project_name)


@project.command("setProtectedBranch")
@click.option('--project_name', '-p', help="The project name", required=True)
@click.option('--branch_name', '-b', help="The branch name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def set_protected_branch(ctx, project_name, branch_name, pretty, time):
    ''' Protect a branch for a project with below access levels
    push_access_levels: "Master",
    merge_access_levels: "Developer + Master"
    '''
    return ctx.obj['git'].set_protected_branch_by_project_name(project_name, branch_name)


@project.command("addDeveloper")
@click.option('--username', '-u', help="User name", required=True)
@click.option('--project_name', '-g', help="Project name", required=True)
@click.option('--pretty', help="Pretty display the returned info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def add_user_to_project_as_developer(ctx, username, project_name, pretty, time):
    ''' Add user as a developer to a project '''
    return ctx.obj['git'].add_user_to_project(username, project_name)