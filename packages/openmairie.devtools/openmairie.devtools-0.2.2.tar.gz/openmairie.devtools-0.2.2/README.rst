openmairie.devtools
===================

openMairie Developer Tools

.. image:: https://img.shields.io/pypi/v/openmairie.devtools.svg
    :target: https://pypi.python.org/pypi/openmairie.devtools/
    :alt: Latest PyPI version

.. contents::

Introduction
------------

openmairie.devtools is a collection of command-line programs to handle tasks on
`openMairie Framework <http://www.openmairie.org/framework/>`_ based projects.
Mainly initialize environment, run tests, release a project, ...


Installation
------------

You just need `pip <https://pip.pypa.io>`_ ::

    pip install openmairie.devtools


Available commands
------------------

- **om-tests**: should be run from the *tests* folder of your project and
  allow you to initialize your test environment, to run all tests suites or to
  run only one tests suite.

- **om-svnexternals**: should be run from the root of your project and allow
  you to export the externals props find in EXTERNALS.txt files. Useful when
  you are mirroring your SVN project to GIT.

