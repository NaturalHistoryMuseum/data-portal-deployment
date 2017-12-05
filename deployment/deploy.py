#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '04/12/2017'.
"""

import os
import click
import ConfigParser

from git.exc import InvalidGitRepositoryError, GitCommandError

from deployment.repository import Repository
from deployment.exceptions import DeploymentException


class Deploy(object):
    '''
    Class for managing code deployment
    '''

    def __init__(self, name=None):
        self.name = name
        config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(config_dir, 'default.cfg'))
        self.dir = config.get('default', 'directory')
        self.wsgi = config.get('default', 'wsgi')

    def master(self):
        '''

        Update repositories to master

        @return: None
        @rtype:
        @raise: DeploymentException
        '''
        # Flag denoting if wsgi restart is required
        wsgi_restart = True
        for repository in self._get_repositories():
            # Check repository isn't detached
            if repository.repo.head.is_detached:
                raise DeploymentException('{} HEAD is detached'.format(repository.name))

            # Repository must be master
            if repository.repo.head.ref.name != 'master':
                raise DeploymentException('{} is not on master branch'.format(repository.name))

            # Get pull status - skipping if status is Already up to date
            if repository.repo.git.pull('--stat') == 'Already up-to-date.':
                click.secho('{} is already up-to-date'.format(repository.name), fg='green')
                continue

            # Try to pull master - raises DeploymentException on error
            try:
                repository.repo.remotes.origin.pull()
            except GitCommandError, e:
                click.secho(e.stderr, fg='red')
                raise DeploymentException('Error pulling {}'.format(repository.name))
            else:
                click.secho('{} updated'.format(repository.name), fg='green')
                # Code has been updated - WSGI restart is required
                wsgi_restart = True

        if wsgi_restart:
            click.secho('Source files updated - restarting WSGI', fg='green')
            self._restart_wsgi()

    def release(self):

        for repository in self._get_repositories():
            if repository.latest_release:
                if repository.current_release == repository.latest_release:
                    click.secho('{} is already at the latest release - {}'.format(repository.name, repository.latest_release), fg='green')
                else:
                    repository.checkout(repository.latest_release)
                    click.secho('{} updated to {}'.format(repository.name, repository.latest_release), fg='green')
            else:
                click.secho('There are no releases available for {} - skipping'.format(repository.name), fg='red')

    def _get_repositories(self):
        for name in os.listdir(self.dir):
            # If a repository name has been passed in, skip
            # any repositories not matching the name
            if self.name and self.name != name or name == 'ckan':
                continue

            path = os.path.join(self.dir, name)
            if os.path.isdir(path):
                try:
                    repo = Repository(path)
                except InvalidGitRepositoryError:
                    continue

                # Make sure this is an NHM Repo and has a latest release
                if repo.is_nhm:
                    yield repo

    def _restart_wsgi(self):
        '''
        Restart WSGI
        @return:
        @rtype:
        '''
        os.utime(self.wsgi, None)


