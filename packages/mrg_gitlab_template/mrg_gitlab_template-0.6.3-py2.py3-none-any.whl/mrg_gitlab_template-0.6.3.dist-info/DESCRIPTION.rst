mrg_gitlab_template
===================

A Python gitlab template for initiating new projects in gitlab. The
boilerplate / template files that are copied are based on best-practices
for Python package development. The new project contains the following
features,

* ``tests`` directory for defining unittests
* ``examples`` directory for placing example snippets
* ``docs`` 
    Sphinx based on the RTD theme for API and
    architectural documentation. It also enables UML
    diagrams to be dynamically generated based on PlantUML
    and graphviz tool.
* ``run.py`` main script entry point with a generic argument parser implementation.
* ``versioneer.py`` an automated version numbering system.
* ``pylint.cfg`` file for source code lexical analysis.
* ``setup.py``: file for wheel file building and deployment to PyPI server.
* ``.gitlab-ci.yml`` file for continuous integration for,
    * unit testing
    * code coverage
    * lint analysis
    * Sphinx documentation building
    * Pages documentation generation
    * deployment to PyPI server.




Installation
------------

Install using pip::

    pip install mrg_gitlab_template

Or to upgrade::

    pip install --upgrade --no-cache-dir mrg_gitlab_template


Command line usage
------------------

The ``pygitcopy`` is a command line utility program to create a new project.
The help switch provides the command line arguments::

    $ pygitcopy --help

    usage: pygitcopy [-h] -g GROUP [-p PAGES_DOMAIN] [-u GITLAB_URL] [-a AUTHOR]
                     [-e EMAIL] [-y YEAR] [-d DIRECTORY] [-v]
                     package

    Create new project from template

    positional arguments:
      package               package name

    optional arguments:
      -h, --help            show this help message and exit
      -g GROUP, --group GROUP
                            the gitlab account. Example: mrg-tools, sci-fv, your
                            account name, etc (default: None)
      -p PAGES_DOMAIN, --pages-domain PAGES_DOMAIN
                            the gitlab pages url domain. Example: gitlab.io,
                            io.esa.int (default: gitlab.io)
      -u GITLAB_URL, --gitlab-url GITLAB_URL
                            the gitlab pages url domain. Example: gitlab.com,
                            gitlab.esa.int (default: gitlab.com)
      -a AUTHOR, --author AUTHOR
                            author name (default: {{author}})
      -e EMAIL, --email EMAIL
                            author email (default: {{email}})
      -y YEAR, --year YEAR  author email (default: <this-year>)
      -d DIRECTORY, --directory DIRECTORY
                            base directory location (default: .)
      -v, --verbosity       Increase output verbosity (default: 0)


Creating a new project
----------------------

Execute the following command::

    pygitcopy <package> --group <group> --directory <new-project-base-dir> -vv

Execute the following commands to add the new project to gitlab::

    cd <new-project-base-dir>/<name>
    git init
    git add .
    git commit -m "First commit"

Navigate to https://gitlab.com/projects/new
and create a new <name> project. Your local can be linked to this repository
using the following commands::



    git remote add origin https://gitlab.com/<group>/<name>.git
    git push -u origin --all
    git push -u origin --tags

To delete a repository from gitlab, use this link and scroll to the
end,

* https://gitlab.com/<group>/<name>/edit


Create "testproj" Example
-------------------------

This example will show you how to,

* create a virtual environment
* create a new gitlab repository
* create a new local project based on this template project
* link the local project to the repository
* commit and push the project files to the repository

Install system requirements::

    sudo apt-get install git
    sudo apt-get install virtualenv
    sudo apt-get install plantuml

Create the new testproj repository project in the gitlab web site:

    firefox https://gitlab.com/projects/new

Create virtual environment::

    mkdir ~/venv
    cd ~venv
    virtualenv -p python3 py3
    source py3/bin/activate


Install the template package::

    pip install mrg_gitlab_template


Create a new local project and upload to git::

    cd ~/PycharmProjects/
    pygitcopy testproj --group mrg-tools
    cd testproj
    git init
    git add .
    git remote add origin https://gitlab.com/mrg-tools/testproj.git
    git push -u origin --all

Check the gitlab pipelines and generated files,

* https://gitlab.com/mrg-tools/testproj/pipelines
* https://mrg-tools.gitlab.io/testproj
* https://mrg-tools.gitlab.io/testproj/doc/

Prepare the project for development::

    pip install -r requirements-dev.txt
    export PYTHONPATH=$PWD

Run some tests::

    pylint --pylint-rc=pylint.cfg testproj
    pytest
    pytest --cov

Build the documentation::

    cd docs
    make html
    firefox build/html/index.html


