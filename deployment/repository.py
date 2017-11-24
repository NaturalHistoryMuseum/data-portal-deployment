#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '24/11/2017'.
"""


import re
from git import Repo
from git.exc import GitCommandError


class Repository(object):
    '''
    Class for managing code deployment
    '''

    def __init__(self, path):
        '''
        Constructor for Deployment
        '''
        self.repo = Repo(path)

    @property
    def releases(self):
        '''
        Get list of tag names from remote repo
        @return: tag names
        @rtype: list
        '''
        remote_tags = self.repo.git.ls_remote('--tags')
        tag_re = re.compile('tags/(v[0-9.]+)')
        # Tags are returned as a multiline string - split them and extract the tags
        return [tag_re.search(l).group(1) for l in remote_tags.splitlines()]

    @property
    def latest_release(self):
        '''
        Get the latest remote tag
        @return: tag
        @rtype: string
        '''
        try:
            return sorted(self.releases, key=lambda v: [int(i) for i in v.lstrip('v').split('.')])[-1]
        except (IndexError, AttributeError):
            return None

    @property
    def current_release(self):
        '''
        Get current deployed release
        @return: release tag
        @rtype: basestring
        '''
        try:
            return self.repo.git.describe('--abbrev=0', '--tags')
        except GitCommandError:
            return None

    def checkout(self, release):
        '''
        Checkout release
        @param release:
        @type release:
        @return:
        @rtype:
        '''
        origin = self.repo.remotes.origin
        origin.fetch()
        tag = 'tags/{}'.format(release)
        self.repo.git.checkout(tag)

    @property
    def is_nhm(self):
        return 'NaturalHistoryMuseum' in self.repo.remote().url
