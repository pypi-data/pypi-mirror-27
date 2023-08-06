import click
from gitlab.helper import GITLABHelper
from utils import try_except
from conf import TOKEN, URL


@click.group()
@click.option('--token', default=TOKEN, help="GitLab user api token.")
@click.option('--url', default=URL, help="GitLab api url")
@click.pass_context
@try_except
def cli(ctx, url, token):
    ctx.obj['git'] = GITLABHelper(url, token)