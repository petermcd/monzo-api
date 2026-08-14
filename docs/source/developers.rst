Developer Guide
=====================================

Many banks now provide an API to allow you too obtain data from your account
by utilising an API. This access can give you great insights into your
financials.

The Monzo API package helps simplify usage of the API.

CICD and Code Standards
-------------------------------------

Prior to committing code you should ensure that the code meets the coding standards.
During CICD the following tools are run, running these prior to submitting a merge
request will help ensure that the code meets the standards.

.. code-block:: bash

    uvx ruff check
    uvx ruff format --check
    uvx ty check
    uv audit

Building Documentation
-------------------------------------

Unless testing, you should have no need to build the docs, ReadTheDocs does
this automatically, however, if you find you need to build the
documentation from source the following steps can be taken:

.. code-block:: bash

    cd docs
    uv run sphinx-build -b html source/ build/html

Tagging
-------------------------------------

Tagging should only take place once a feature branch has been merged. The
tag should match the version that can be found in setup.cfg

To create and push a tag the following steps should be taken replacing
x.x.x with the version in setup.cfg:

.. code-block:: bash

    git checkout main
    git pull
    git tag -a vx.x.x -m "x.x.x SHORT MESSAGE"
    git push origin vx.x.x

Distributing Package
-------------------------------------

Distributing the package is no longer required. A Github action
automatically uploads the generated .tar.gz and .whl files.
