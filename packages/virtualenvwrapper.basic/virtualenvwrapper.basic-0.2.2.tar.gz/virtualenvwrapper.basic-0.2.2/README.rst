=======================
virtualenvwrapper.basic
=======================

virtualenvwrapper.basic is a template for virtualenvwrapper_ to create the base
skeleton of a python application when creating a new project directory.


Installation
============

::

  $ pip install virtualenvwrapper.basic


Usage
=====

::

  $ mkproject -t basic new_project


The previous command will create a directory and will populate it with various
files, namely ``ANNOUNCE``, ``AUTHORS``, ``CHANGES``, ``LICENSE``,
``MANIFEST.in``, ``README``, ``requirements.txt`` and ``setup.py``.

The content of each file is matched to the name of your project and your
:code:`git` configuration.

You can set up another reference skeleton directory by specifying the path to
it in the environment variable :code:`VIRTUALENVWRAPPER_BASIC`. The content
of this directory will be used as the template of the new project.

::

  $ VIRTUALENVWRAPPER_BASIC="/my/own/template" mkproject -t basic new_project


Template variables
==================

virtualenvwrapper.basic supports template variables to be remplaced at the
creation time of a new project. The variables can be used in the content and
the name of a file.

The following variables are available:

+------------------------------+----------------------------------------------+
| Variable                     | Description                                  |
+==============================+==============================================+
| $PROJECT_NAME                | Replaced by the project name used with       |
|                              | :code:`virtualenvwrapper`.                   |
+------------------------------+----------------------------------------------+
| $AUTHOR_EMAIL                | Replaced by the email configured in git as   |
|                              | :code:`user.email` or `AUTHOR_EMAIL`         |
|                              | environment variable if set.                 |
+------------------------------+----------------------------------------------+
| $AUTHOR_NAME                 | Replaced by the name configured in git as    |
|                              | :code:`user.name` or `AUTHOR_NAME`           |
|                              | environment variable if set.                 |
+------------------------------+----------------------------------------------+
| $YEAR                        | Replaced by the current year.                |
+------------------------------+----------------------------------------------+
| $MONTH                       | Replaced by the current month.               |
+------------------------------+----------------------------------------------+
| $DAY                         | Replaced by the current day.                 |
+------------------------------+----------------------------------------------+

.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper
