Developer Guide
=====================================

Many banks now provide an API to allow you too obtain data from your account
by utilising an API. This access can give you great insights into your
financials.

The Monzo API package helps simplify usage of the API.

Building Documentation
-------------------------------------

Unless eating you should have no need to build the docs, ReadTheDocs does
this automatically, however, if you find you need to build the
documentation from source the following steps can be taken:

.. code-block:: bash

    cd docs
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
    python -m build
    twine upload dist/*

