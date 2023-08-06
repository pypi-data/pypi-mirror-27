# Copyright 2017 Julien Peloton
# Licensed under the GPL-3.0 License, see LICENSE file for details.
## Author: j.peloton@sussex.ac.uk
from __future__ import absolute_import, print_function

import ConfigParser
import os
import sys

def print_path(func):
    """
    Wrapper to print the path of the distant repository
    To be used as a decorator.

    Parameters
    ----------
    func : function
        The function for the decorator.

    Returns
    ----------
    wrapper : function
        The wrapped function.

    """
    def wrapper(*args, **kwargs):
        """ The wrapper """
        print('Repo: ', args[0].path)
        res = func(*args, **kwargs)
        return res
    return wrapper

def checkrc(func):
    """
    Check that the .git-rrc exists. Raise an error if not.
    To be used as a decorator.

    Parameters
    ----------
    func : function
        The function for the decorator.

    Returns
    ----------
    wrapper : function
        The wrapped function.

    """
    def wrapper(*args, **kwargs):
        """ The wrapper """
        msg = 'Cannot find {}'.format(args[0].rcfile)
        assert os.path.isfile(args[0].rcfile), AssertionError(msg)
        res = func(*args, **kwargs)
        return res
    return wrapper


class Repository():
    """ Generic class for repository """
    def __init__(self, reponame):
        """
        Contains current path and path to the distant repository.
        Mostly rely on os.system to wrap traditional git commands.

        Parameters
        ----------
        reponame : string
            The name of the distant repo.

        """
        ## name of the repo
        self.reponame = reponame

        ## Define useful path
        self.current_location = os.getcwd()
        self.HOME = os.getenv('HOME')
        self.rcfile = os.path.join(self.HOME, '.git-rrc')

        ## Load the parameter(s) in the rc file for this repo
        self.readrc()

    @checkrc
    def readrc(self):
        """
        Check that the name of the repo is registered in the .git-rrc file.

        """
        Config = ConfigParser.ConfigParser()
        Config.read(self.rcfile)

        msg = 'The repo <{}> is not registered in {}. '.format(
            self.reponame, self.rcfile) + 'Run `git-r add_repo <repopath>`.'
        assert self.reponame in Config._sections, AssertionError(msg)

        self.path = Config._sections[self.reponame]['path']

    @print_path
    def run(self, command, options=['']):
        """
        Routine to execute git command inside the distant repository.

        Parameters
        ----------
        command : string
            Git command to execute.
        options : list of strings, optional
            Other option to git command. Can be a filename (if doing a diff),
            or a branch name (if doing a checkout) for example.

        """
        walkin = 'cd {};'.format(self.path)
        walkback = 'cd {};'.format(self.current_location)
        com = 'git {} '.format(command)
        for op in options:
            com += op + ' '
        com += ';'

        os.system(walkin + com + walkback)


def add_repo_into_rcfile(repopath):
    """
    Add repo and path into the rcfile.
    If the file doesn't exist, it will be created.

    Parameters
    ----------
    repopath : string
        The full path to the repo: /path/to/reponame

    """
    HOME = os.getenv('HOME')
    rcfn = '.git-rrc'
    rcfnpath = os.path.join(HOME, rcfn)
    reponame = os.path.basename(repopath)

    ## Check that the folder exists
    msg = 'No folder at {}'.format(repopath)
    assert os.path.isdir(repopath), AssertionError(msg)

    ## Check that the folder is a git repo
    gitrep = os.path.join(repopath, '.git')
    msg = '{} is not a git repository.'.format(gitrep)
    assert os.path.isdir(gitrep), AssertionError(msg)

    ## Check if the .git-rrc exists
    isrc = os.path.isfile(rcfnpath)
    if not isrc:
        print(".git-rrc does not exist. Now created at {}/.git-rrc.".format(
            HOME))

    Config = ConfigParser.ConfigParser()
    Config.read(rcfnpath)

    ## Check if the section already exists
    if reponame in Config._sections:
        print("+---------------------------+")
        print("Repo already in the .git-rrc file!")
        print("Path used is {}".format(Config._sections[reponame]['path']))
        answer = raw_input("Do you want to overwrite it? [Y/n]")
        print("+---------------------------+")

        if answer in ['Y', 'y', 'yes', 'Yes']:
            print("Overwrite...")
        elif answer in ['n', 'No', 'N', 'no']:
            print("Do not overwrite...")
            sys.exit()
    else:
        Config.add_section(reponame)

    Config._sections[reponame]['path'] = repopath

    with open(rcfnpath, 'w+') as f:
        Config.write(f)
