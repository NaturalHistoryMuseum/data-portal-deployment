#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '16/11/2017'.
"""

import click

from deployment.deploy import Deploy


@click.group()
@click.option('--name', '-n')
@click.pass_context
def deploy(ctx, name):
    ctx.obj = Deploy(name)
    click.echo('Debug mode is %s' % ('on' if name else 'off'))


@deploy.command()
@click.pass_context
def master(ctx):
    click.echo('Deploying master branch')
    ctx.obj.master()


@deploy.command()
@click.pass_context
def release(ctx):
    click.echo('Deploying latest release')
    ctx.obj.release()


if __name__ == '__main__':
    deploy()
