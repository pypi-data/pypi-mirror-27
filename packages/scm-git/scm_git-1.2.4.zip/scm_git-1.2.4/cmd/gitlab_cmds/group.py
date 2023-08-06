import click
from utils import try_except, timeit
from cli import cli


@cli.group()
@click.pass_context
def group(ctx):
    ''' GitLab group related operations'''
    pass


@group.command("info")
@click.option('--name', '-n', help="The group name", required=True)
@click.option('--pretty', help="Pretty display the returned info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def get_group_info(ctx, name, pretty, time):
    ''' Get group information by a given group name '''
    return ctx.obj['git'].get_group_by_name(name)


@group.command("create")
@click.option('--parent_group_name', '-p', help="The parent group name", required=True)
@click.option('--sub_group_name', '-s', help="The sub group name", required=True)
@click.option('--pretty', help="Pretty display the returned info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def create_sub_group(ctx, parent_group_name, sub_group_name, pretty, time):
    ''' Create sub group by a given parent group name and sub group name '''
    return ctx.obj['git'].create_sub_group_by_parent_group_name(parent_group_name, sub_group_name)


@group.command("addDeveloper")
@click.option('--username', '-u', help="User name", required=True)
@click.option('--group_name', '-g', help="Group name", required=True)
@click.option('--pretty', help="Pretty display the returned info [True|False]", default=False)
@click.option('--time', help="Display the time spent [True|False]", default=False)
@click.pass_context
@try_except
@timeit
def add_user_to_group_as_developer(ctx, username, group_name, pretty, time):
    ''' Add user as a developer to a group '''
    return ctx.obj['git'].add_user_to_group(username, group_name)