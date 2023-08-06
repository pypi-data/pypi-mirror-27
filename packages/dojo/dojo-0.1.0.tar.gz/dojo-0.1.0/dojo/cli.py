import click

from .dojo import Dojo


@click.group()
@click.pass_context
def cli(context):
    if context.obj is None:
        context.obj = {}
    context.obj['dojo'] = Dojo()


@cli.command(help='Run a dojo dataset given the module path')
@click.argument('dataset')
@click.pass_context
def run(context, dataset):
    context.obj['dojo'].run(dataset)
