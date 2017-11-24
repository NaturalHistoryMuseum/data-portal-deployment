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

@click.command()
@click.option('--repo_name', '-n')
def main(repo_name):

    config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(config_dir, 'default.cfg'))
    directory = config.get('default', 'directory')

    for name in os.listdir(directory):
        # If we only want to update one repo, skip if it doesn't match repo_name
        if repo_name and name != repo_name:
            continue
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            try:
                repo = Repository(path)
            except InvalidGitRepositoryError:
                continue

            # Make sure this is an NHM Repo and has a latest release
            if repo.is_nhm:
                if repo.latest_release:
                    if repo.current_release == repo.latest_release:
                        click.secho('{} is already at the latest release - {}'.format(name, repo.latest_release), fg='green')
                    else:
                        repo.checkout(repo.latest_release)
                        click.secho('{} updated to {}'.format(name, repo.latest_release), fg='green')
                else:
                    click.secho('There are no releases available for {} - skipping'.format(name), fg='red')

    click.secho('Repositories updated - please touch WSGI to compile changes:\n\n\ttouch apache2.wsgi\n', fg='green')

if __name__ == '__main__':
    main()
