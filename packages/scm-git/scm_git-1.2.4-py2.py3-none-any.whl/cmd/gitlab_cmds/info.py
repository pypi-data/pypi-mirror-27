import click
from cli import cli
from utils import timeit


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