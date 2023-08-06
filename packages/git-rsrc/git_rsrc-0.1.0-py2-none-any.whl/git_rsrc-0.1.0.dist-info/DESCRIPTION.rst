=============================
git-r
=============================

.. contents:: **Table of Contents**

What is git-r?
===============
git-r is a python module to manage git repositories from a distant folder.
We provide an executable ``git-r`` which is a wrapper around the traditional ``git`` command
and can be called from any location to make change to a particular git repository on the machine.

Requirements
===============

No special dependencies. Work for both python2.7 and python 3.X.

Installation
===============

The best is to use pip

::

    pip install git-r

Make sure that the executable is in your path.

Quick examples
===============

The general usage is very simple

::

    git-r <command> [<options>] <repo_name>

Note that ``command`` can be any git commands.

Say now I have a repo at ``/some/path/repo``. First, you need to create the .git-rrc file in
your ``$HOME`` and register ``repo`` (see the example provided). git-r allows you to that
from the command line:

::

    julien:workspace$ git-r add_repo /some/path/repo
    .git-rrc does not exist. Now created at /Users/julien/.git-rrc.

This message will appear only once when the file is created.
Then you can as many repo as you want. You can also overwrite location of
old repo:

::

    julien:workspace$ git-r add_repo /some/new/path/repo
    +---------------------------+
    Repo already in the .git-rrc file!
    Path used is /Users/julien/Documents/Workspace_postdoc/github/s4cmb
    Do you want to overwrite it? [Y/n]


**Example 1: Pull**

Imagine I am working from a folder distant ``/some/other/path/workspace`` (but still the same machine!)
and I want to pull the latest change from ``repo``:

::

    julien:workspace$ git-r pull repo
    Repo: /some/path/repo
    <can ask password>
    Already up-to-date.
    julien:workspace$

**Example 2: Changing branch**

Imagine I am working from a folder distant ``/some/other/path/workspace`` (but still the same machine!)
and I want to switch from the ``master`` branch to ``mybranch`` branch in ``repo``:

::

    julien:workspace$ git-r checkout mybranch repo
    Repo: /some/path/repo
    Switched to branch 'mybranch'
    Your branch is up-to-date with 'origin/mybranch'.
    julien:workspace$


Support
===============

.. raw:: html

    <img src="https://github.com/JulienPeloton/git-r/blob/master/pics/erc.jpg" height="200px">


