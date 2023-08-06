# Copyright 2017 Julien Peloton
# Licensed under the GPL-3.0 License, see LICENSE file for details.
## Author: j.peloton@sussex.ac.uk
from __future__ import absolute_import, print_function

## All small caps for py3
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

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
        ## Do not print for tests
        if not args[0].silent:
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
    def __init__(self, reponame, silent=False):
        """
        Contains current path and path to the distant repository.
        Mostly rely on os.system to wrap traditional git commands.

        Parameters
        ----------
        reponame : string
            The name of the distant repo.
        silent : bool
            If True, do not print out messages. Default is False.

        Examples
        ----------
        >>> address = 'https://github.com/JulienPeloton/i_am_a_repo.git'
        >>> where = 'toto/tutu'
        >>> reponame = clone_a_repo(address, where)
        >>> repopath = os.path.join(os.getcwd(), where, reponame)
        >>> add_repo_into_rcfile(repopath, istest=True)
        >>> r = Repository(reponame, silent=True)

        Make a pull
        >>> r.run('pull')

        Check the status
        >>> r.run('status')

        Make a diff
        >>> r.run('checkout', ['test.py'])

        Change branch
        >>> r.run('checkout', ['new_branch'])

        """
        ## name of the repo
        self.reponame = reponame
        self.silent = silent

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


def add_repo_into_rcfile(repopath, istest=False):
    """
    Add repo and path into the rcfile.
    If the rcfile doesn't exist, it will be created and stored in the $HOME.

    Parameters
    ----------
    repopath : string
        The full path to the repo: /path/to/reponame
    istest : bool, optional
        If True, skip printout message. Useful for test purposes.
        Default is False.

    Examples
    ----------
    >>> address = 'https://github.com/JulienPeloton/i_am_a_repo.git'
    >>> where = 'toto/tutu'
    >>> reponame = clone_a_repo(address, where)
    >>> repopath = os.path.join(os.getcwd(), where, reponame)

    ## istest set to False by default.
    >>> add_repo_into_rcfile(repopath, istest=True)

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
    if not isrc and not istest:
        print(".git-rrc does not exist. Now created at {}/.git-rrc.".format(
            HOME))

    Config = ConfigParser.ConfigParser()
    Config.read(rcfnpath)

    ## Check if the section already exists
    if reponame in Config._sections:
        if not istest:
            print("+---------------------------+")
            print("Repo already in the .git-rrc file!")
            print("Old path was {}".format(Config._sections[reponame]['path']))
            print("New path is {}".format(repopath))
            print("+---------------------------+")
    else:
        Config.add_section(reponame)

    Config._sections[reponame]['path'] = repopath

    with open(rcfnpath, 'w+') as f:
        Config.write(f)

def clone_a_repo(address, where=''):
    """
    Clone a repository into the machine.

    Parameters
    ----------
    address : string
        Url for the git repo.
    where : string
        Location on disk where the repo must be cloned.

    Returns
    ----------
    reponame : string
        Name of the repository.

    Examples
    ----------
    >>> address = 'https://github.com/JulienPeloton/i_am_a_repo.git'
    >>> where = 'toto/tutu'
    >>> reponame = clone_a_repo(address, where)
    """
    plan = ''
    if len(where) > 0:
        plan += 'mkdir -p {};'.format(where)
        plan += 'cd {};'.format(where)

    reponame = os.path.basename(address).split(".")[0]
    repopath = os.path.join(where, reponame)
    if not os.path.isdir(repopath):
        plan += 'git clone {};'.format(address)
        os.system(plan)
    else:
        pass

    return reponame


if __name__ == "__main__":
    import doctest
    doctest.testmod()
