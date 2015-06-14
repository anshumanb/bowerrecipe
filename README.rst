.. contents::

Introduction
============

This recipe allows downloading and installing assets such as images, CSS and JavaScript using Twitter Bower.

Supported options
=================

The recipe supports the following options:

packages
    Packages that should be installed with bower. Packages specified here are
    passed to bower verbatim. They can be specified in any form that is
    supported by bower::

        packages =
            underscore
            git://github.com/components/jquery.git
            bootstrap#2.2.2

base-directory
    Absolute path to the bower "project" directory. ``bower install`` is run
    from this directory and the bower configuration file, ``.bowerrc`` is also
    placed here.  Optional; defaults to ``${buildout:parts-directory}/bower``.
    Requires an absolute path.

    This directory is not removed when the Buildout part is uninstalled.

executable
    Absolute path to the ``bower`` executable. Packages are installed using
    this executable. Optional; defaults to ``bower`` on ``PATH``.

downloads
    Relative path, from the ``base-directory``, to the directory where bower
    will download packages to. This path is written to the ``.bowerrc`` file
    prior to running the executable. Optional; defaults to ``downloads``. Thus,
    the downloaded packages are placed in ``${base-directory}/downloads`` by
    default.

    This directory *is* removed when the Buildout part is uninstalled.


Example usage
=============

A sample buildout that uses this recipe could look like::

    [buildout]
    parts = node web

    [node]
    recipe = gp.recipe.node
    url = http://nodejs.org/dist/v0.8.16/node-v0.8.16.tar.gz
    npms = bower@0.6.8
    scripts = bower

    [web]
    recipe = bowerrecipe
    packages = jquery#1.8.3 normalize-css
    executable = ${buildout:bin-directory}/bower

This would place the downloaded packages in ``parts/bower/downloads``.
Modifying the ``web`` section to be::

    [web]
    recipe = bowerrecipe
    packages = jquery#1.8.3 normalize-css
    executable = ${buildout:bin-directory}/bower
    base-directory = ${buildout:parts-directory}
    downloads = components

would result in bower placing the downloaded packages in ``parts/components``.

Notes
=====

#. Bower still looks at the ``~/.bowerrc`` file. Hence, if this file exists, it
   may affect the buildout bower configuration
#. Bower still uses the cache located in the user's home directory. For me,
   this happens to be ``~/.bower/cache/``

