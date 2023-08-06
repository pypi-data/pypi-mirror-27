mir.git README
==============

.. image:: https://circleci.com/gh/darkfeline/mir-git.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir-git
   :alt: CircleCI
.. image:: https://codecov.io/gh/darkfeline/mir-git/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir-git
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.git.svg
   :target: https://badge.fury.io/py/mir.git
   :alt: PyPI Release
.. image:: https://readthedocs.org/projects/mir-git/badge/?version=latest
   :target: http://mir-git.readthedocs.io/en/latest/
   :alt: Latest Documentation

Python interface to Git.

See module docstring for public API.

Before running any other make command, run::

  $ pipenv install --dev

To build an installable wheel, run::

  $ make wheel

To build a source distribution, run::

  $ make sdist

To run tests, run::

  $ make check

To build docs, run::

  $ make html

To build a TAGS file, run::

  $ make TAGS

To clean up all built files, run::

  $ make distclean
