Viewer
=====================================

The viewer is a server application that aides in the creation of Access
tokens.

Within the tutorials section we guide you through how to create a client
in the Monzo developer center. You are still required to do this however
once you have these details you can use the viewer to simply convert
this into an access token.

To get started simply run the following:

.. code-block:: bash

    cd monzo-api
    pip install -e .
    start-server

The terminal will provide a URL that you should visit, by default this
is `http://127.0.0.1:8080/index.html <http://127.0.0.1:8080/index.html>`_.

Once you arrive at auth_step_one.html you will find a redirect URL, this
will have a value of
`http://127.0.0.1:8080/monzo <http://127.0.0.1:8080/monzo>`_, prior to
proceeding ensure that the client you have created on Monzo contains this
as a redirect URL.

During the process of getting an access token you will be redirected back
to  http://127.0.0.1:8764/monzo, this will automatically handle the process
therefore no need to copy the code and state from the URL.

Once finished you will be presented with the credentials in a format that
can simply be copied into a script.

Transactions
-------------------------------------

After configuration when visiting `http://127.0.0.1:8080/index.html <http://127.0.0.1:8080/index.html>`_ the page will
automatically fetch the list of accounts. From this you can request the transactions. At present these transactions
span from the last 7 days.

Raw Requests
-------------------------------------

You can make raw requests to the API by visiting
`http://127.0.0.1:8080/raw_request.html <http://127.0.0.1:8080/raw_request.html>`_. This page will allow you to specify
the path, http method, and parameters for the request. Regardless of whether you are using get or post the parameters
should be entered as a json dictionary.

The Future
-------------------------------------

At present the viewer has an extremely limited (but useful) feature set.
In the future we plan on making this a fully featured viewer for objects
that can be returned by the the API.
