Developer Guide
=====================================

Many banks now provide an API to allow you too obtain data from your account
by utilising an API. This access can give you great insights into your
financials.

The Monzo API package helps simplify usage of the API.

CICD and Code Standards
-------------------------------------

We have attempted to reduce the work required to ensure the code conforms to
our coding standards. You can help ensure that any code changes will pass
CICD by making use of pre-commit. The following steps will set this up for you:

.. code-block:: bash

    pip install pre-commit
    pre-commit install
    pre-commit run --all-file

The above commands will create pre-commit hooks, this will test the code prior
to code being committed by Git. Some of the tasks will even correct the data
instead of throwing an error.

If you would like to run the checks without cmmitting code you can run the
following command:

.. code-block:: bash

    pre-commit run --all-file

Building Documentation
-------------------------------------

Unless eating you should have no need to build the docs, ReadTheDocs does
this automatically, however, if you find you need to build the
documentation from source the following steps can be taken:

.. code-block:: bash

    cd docs
    pip install -e .[docs]
    sphinx-build -b html source/ build/html

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

Distributing the package should no longer be required. Github actions
automatically upload the generated .tar.gz and .whl files.

Prior to being able to upload a package to Pypi you first need to create an
API key,once obtained create a file called .pypirc in %homepath% with the
following details, replacing API_TOKEN with the real API token.

.. code-block:: yaml

    [pypi]
      username = __token__
      password = API_TOKEN

You can now run the following to upload the package.

.. code-block:: bash

    git checkout main
    git pull
    pip install -e .[build]
    twine upload dist/*
