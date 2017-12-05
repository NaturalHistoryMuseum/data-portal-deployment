#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '16/11/2017'.
"""
import os
import click
import ConfigParser

from git.exc import InvalidGitRepositoryError

from deployment.repository import Repository
from deployment.exceptions import DeploymentException
from deployment.deploy import Deploy



#
#
# def update_repo_to_latest_release(repo):
#     '''
#     Update a repository to the latest release
#     @param repo:
#     @type Repository:
#     @return:
#     @rtype:
#     '''
#
#
# def update_repo_to_master(repo):
#     '''
#     Update a repository from master branch
#     @param repo:
#     @type Repository:
#     @return:
#     @rtype:
#     '''
#

#
#
# @click.command()
# @click.option('--latest_release', '-r', is_flag=True)

# def main(latest_release, repo_name):
#     for repo in list_repositories():
#
#         # If we only want to update one repo, skip if it doesn't match repo_name
#         if repo_name and repo.name != repo_name:
#             continue
#
#         if latest_release:
#             update_repo_to_latest_release(repo)
#         else:
#             # Need to identify if the repo's been changed
#             # ANd only restart apache if it has been
#             update_repo_to_master(repo)
#
#             click.secho('Repositories updated - please restart WSGI to release changes:\n\n\ttouch /etc/ckan/default/apache.wsgi\n', fg='green')


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
