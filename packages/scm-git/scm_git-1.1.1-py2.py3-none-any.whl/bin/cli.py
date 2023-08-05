#!/usr/bin/env python

import click
from pprint import pprint
from scm_git.gitlab_helper import GITLABHelper

TOKEN = '_yCUXgMgrPxLqqy5CZtT'
URL = 'https://gitlabe1.ext.net.nokia.com/api/v4'


def pretty_print(value, pretty):
    if pretty:
        pprint(value)
    else:
        print(value)


@click.group()
@click.option('--token', default=TOKEN, help="GitLab user api token.")
@click.option('--url', default=URL, help="GitLab api url")
@click.pass_context
def cli(ctx, url, token):
    ctx.obj['git'] = GITLABHelper(url, token)


@cli.group()
@click.pass_context
def info(ctx):
    ''' Show some information '''
    pass


@info.command('env')
@click.pass_context
def info_env(ctx):
    ''' Show environment information'''
    click.echo(ctx.obj['git'])


@cli.group()
@click.pass_context
def project(ctx):
    ''' GitLab project related operations'''
    pass


@project.command("info")
@click.option('--name', '-n', help="The project name", required=True)
@click.option('--pretty', help="Pretty display the project info [True|False]", default=False)
@click.pass_context
def get_project_info(ctx, name, pretty):
    ''' Get project information by a given project name '''
    git = ctx.obj['git']
    try:
        res = git.get_project_by_name(name)
    except ValueError as ex:
        print(ex)
    except UnboundLocalError:
        pass
    else:
        pretty_print(res, pretty)


@project.command("create")
@click.option('--group_name', '-g', help="The group name", required=True)
@click.option('--project_name', '-p', help="The project name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.pass_context
def create_project(ctx, group_name, project_name, pretty):
    ''' Create a project under a group by given group name and project name '''
    git = ctx.obj['git']
    try:
        res = git.create_project_under_group_by_group_name(group_name, project_name)
    except ValueError as ex:
        print(ex)
    except UnboundLocalError:
        pass
    else:
        pretty_print(res, pretty)


@project.command("set_protected_branch")
@click.option('--project_name', '-p', help="The project name", required=True)
@click.option('--branch_name', '-b', help="The branch name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.pass_context
def set_protected_branch(ctx, project_name, branch_name, pretty):
    ''' Protect a branch for a project with below access levels
    push_access_levels: "Master",
    merge_access_levels: "Developer + Master"
    '''
    git = ctx.obj['git']
    try:
        res = git.set_protected_branch_by_project_name(project_name, branch_name)
    except ValueError as ex:
        print(ex)
    except UnboundLocalError:
        pass
    else:
        pretty_print(res, pretty)


@cli.group()
@click.pass_context
def group(ctx):
    ''' GitLab group related operations'''
    pass


@group.command("info")
@click.option('--name', '-n', help="The group name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.pass_context
def get_group_info(ctx, name, pretty):
    ''' Get group information by a given group name '''
    git = ctx.obj['git']
    try:
        res = git.get_group_by_name(name)
    except ValueError as ex:
        print(ex)
    except UnboundLocalError:
        pass
    else:
        pretty_print(res, pretty)


@group.command("create")
@click.option('--parent_group_name', '-p', help="The parent group name", required=True)
@click.option('--sub_group_name', '-s', help="The sub group name", required=True)
@click.option('--pretty', help="Pretty display the group info [True|False]", default=False)
@click.pass_context
def create_sub_group(ctx, parent_group_name, sub_group_name, pretty):
    ''' Create sub group by a given parent group name and sub group name '''
    git = ctx.obj['git']
    try:
        res = git.create_sub_group_by_parent_group_name(parent_group_name, sub_group_name)
    except ValueError as ex:
        print(ex)
    except UnboundLocalError:
        pass
    else:
        pretty_print(res, pretty)


if __name__ == '__main__':
    cli(obj={})
