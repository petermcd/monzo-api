Basic API Calls
=====================================

All API calls in the package take the same form, therefore following this
tutorial should help you understand how the package works.

For this tutorial we are going to select all accounts that we have in Monzo.

Obtaining Our Account List
-------------------------------------

This tutorial will work through the following script:

.. literalinclude:: ../../examples/get_accounts.py
  :language: python

As before the script requires several pieces of information to start with. We
obtained each of these in the previous tutorials.

Client ID, Client Secret and Redirect URL are as we obtained from the Monzo
developer site.

.. code-block:: python

    monzo = Authentication(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_uri,
        access_token=access_token,
        access_token_expiry=expiry,
        refresh_token=refresh_token
    )

Access Token, Expiry and Refresh Token were obtained in the "Generating An
Access Token" (handily in a format you could copy and paste overwriting the
variables in the above script). In a real world application these would be
stored in a database or a state file.

We now create an Authentication object using the variables above. This object is
responsible for authentication of the API, making requests and refreshing access.
This object is passed about to almost any other object we create.

We can now carry out a fetch of the accounts that we have with Monzo:

.. code-block:: python

   accounts = Account.fetch(monzo)

As you can see we have called a class method, with this package you should not
need to instantiate objects yourself (apart from the Authentication object).

Each endpoint that you may call has a class in the endpoints folder, each of
these contain either a fetch or fetchone class method that will carry out
a query and return a list of objects matching your query.

You now have a list of accounts that you can inspect and work with.
