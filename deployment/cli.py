#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '16/11/2017'.
"""

import click
import time
import datetime

from deployment.deploy import Deploy


@click.group()
@click.option('--name', '-n')
@click.pass_context
def deploy(ctx, name):
    t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    click.echo('%s: Deployment started' % t)
    ctx.obj = Deploy(name)


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
