Monzo API
=====================================

The Monzo API package allows you to interact with the API provided by Monzo
bank.

DISCLAIMER
-------------------------------------

Before using this package it is important to understand that the Monzo API should only be
used for non-public projects hosted securely. Please do not use this on a public server
and do not use it for accessing other users accounts.

Installation
-------------------------------------

The package can be installed as a standard pip project:


.. code-block:: bash

    pip install monzo-api

Basic Usage
-------------------------------------

Prior to using the API you need to obtain a few details from Monzo. Please
read `this <https://monzo-api.readthedocs.io/en/latest/monzo_setup.html>`_
document.

Please see the examples in the example directory.

Documentation
-------------------------------------

Full documentation can be found on
`Read The Docs <https://monzo-api.readthedocs.io>`_

Implemented End Points
-------------------------------------

.. list-table:: Monzo Endpoints
    :widths: 45 30 25 25
    :header-rows: 1

    * - End Point
      - Implemented
      - Version
      - Tests Written
    * - Authentication
      - yes
      - 0.0.1
      - No
    * - Refresh Access
      - yes
      - 0.0.1
      - No
    * - Whoami
      - yes
      - 0.0.1
      - Yes
    * - Logout
      - yes
      - 0.0.1
      - Yes
    * - List Accounts
      - yes
      - 0.0.2
      - Yes
    * - Read Balance
      - yes
      - 0.0.2
      - Yes
    * - List Pots
      - yes
      - 0.0.3
      - No
    * - Deposit Into Pot
      - yes
      - 0.0.3
      - No
    * - Withdraw From Pot
      - yes
      - 0.0.3
      - No
    * - Get Transaction
      - yes
      - 0.0.4
      - No (Testing Fails)
    * - Get Transaction List
      - yes
      -  0.0.4
      - Yes
    * - Annotate Transaction
      - yes
      - 0.1.1 \*
      - Yes
    * - Create Feed Item
      - yes
      - 0.0.2
      - Yes
    * - Upload Attachment
      -
      -
      - No
    * - Register Attachment
      -
      -
      - No
    * - Deregister Attachment
      -
      -
      - No
    * - Fetch Receipt
      - yes
      - 0.1.2
      - Yes
    * - Create Receipt
      - yes
      - 0.1.2
      - Yes
    * - Delete Receipt
      - yes
      - 0.1.2
      - No, Functionality currently broken
    * - Register Webhook
      - yes
      - 0.0.3
      - Yes
    * - List Webhooks
      - yes
      - 0.0.3
      - Yes
    * - Delete Webhooks
      - yes
      - 0.0.3
      - Yes
    * - Open Banking API
      - No
      - \*\*
      -

* \* Annotations only appear to work for existing keys such as Notes `view on the forum <https://community.monzo.com/t/annotate-transaction-endpoint-not-working-for-custom-key/121203>`_.
* \*\* It is unlikely that this package will implement usage of the Open Banking API due to restrictions accessing it.
