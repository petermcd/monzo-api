Refreshing Tokens
=====================================

In a previous tutorial we spoke about the fact that tokens will expire.

Although the Authentication class has a refresh_token method you can use,
there should be no reason to do so. The package refreshes tokens when it
is required automatically.

This raises the question how do you know if a token has been refreshed.

Identifying Refreshed ToKens
-------------------------------------

There are two ways that you can identify if a token has been refreshed.

Checking The Current Token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unfortunately you cannot rely on a token not having expired when
identifying if a token will be replaced or not, there can be instances
when a valid token needs to be replaced.

Therefore the first method, although far from ideal, is to fetch the
current token after you have carried out a request comparing it to the
token you already have.

An Authentication object contains three properties to fetch the current
details:

.. code-block:: python

    from monzo.authentication import Authentication

    monzo = Authentication(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_uri,
        access_token=access_token,
        access_token_expiry=expiry,
        refresh_token=refresh_token
    )

    # Carry out some API calls

    print(monzo.access_token)
    print(monzo.access_token_expiry)
    print(monzo.refresh_token)

You should then store these for the next time you wish to carry out API calls.

Registering A Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned, the above method is not convenient at all, a better method would
be if for example the package just told you that those details changed.

This is where handlers come in.

.. code-block:: python

    from monzo.authentication import Authentication
    from monzo.endpoints.echo import Echo

    monzo = Authentication(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_uri,
        access_token=access_token,
        access_token_expiry=expiry,
        refresh_token=refresh_token
    )

    # Instantiate our handler
    handler = Echo()

    #Register the handler
    monzo.register_callback_handler(handler)

    # Carry out API calls

Now whenever the package needs to fetch new tokens the store method of
the handler will be called.

This package currently contains two handlers:

**Echo**

This handler simply prints the new token details. Under no circumstances should
this handler be used in a real application.

**FileSystem**

This handler stores the details on the file system in a location you specify
when instantiating the handler.

The file system handler also implements a Fetch method allowing you to
retrieve the details from the file.

Implementing A Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is not beyond the realms of possibility that you may wish to store these
details in a database or using some other mechanism.

To achieve this you should create a class that extends from the Storage
abstract base class. At present this simply dictates that you must have
a store method and the parameters that must be present.

Reading the Echo handler code should clarify how this works

.. literalinclude:: ../../monzo/handlers/echo.py
  :language: python
