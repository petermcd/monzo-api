TODO
=====================================

Implemented End Points
-------------------------------------

.. list-table:: Monzo Endpoints
    :widths: 45 30 25
    :header-rows: 1

    * - End Point
      - Implemented
      - Version
    * - Authentication
      - yes
      - 0.0.1
    * - Refresh Access
      - yes
      - 0.0.1
    * - Whoami
      - yes
      - 0.0.1
    * - Logout
      - yes
      - 0.0.1
    * - List Accounts
      - yes
      - 0.0.2
    * - Read Balance
      - yes
      - 0.0.2
    * - List Pots
      - yes
      - 0.0.3
    * - Deposit Into Pot
      - yes
      - 0.0.3
    * - Withdraw From Pot
      - yes
      - 0.0.3
    * - Get Transaction
      - yes
      - 0.0.4
    * - Get Transaction List
      - yes
      -  0.0.4
    * - Annotate Transaction
      - yes
      - 0.1.1 \*
    * - Create Feed Item
      - yes
      - 0.0.2
    * - Upload Attachment
      -
      -
    * - Register Attachment
      -
      -
    * - Deregister Attachment
      -
      -
    * - Fetch Receipts
      -
      -
    * - Fetch Receipt
      -
      -
    * - Create Receipt
      -
      -
    * - Delete Receipt
      -
      -
    * - Register Webhook
      - yes
      - 0.0.3
    * - List Webhooks
      - yes
      - 0.0.3
    * - Delete Webhooks
      - yes
      - 0.0.3
    * - Open Banking API
      -
      - \*\*

* \* Annotations only appear to work for existing keys such as Notes `view on the forum <https://community.monzo.com/t/annotate-transaction-endpoint-not-working-for-custom-key/121203>`_.
* \*\* It is unlikely that this package will implement usage of the Open Banking API due to restrictions accessing it.

Miscellaneous
-------------------------------------

- Tidy exceptions and ensure scenarios are captured correctly
- Implement testing
- Facilitate receiving webhook calls
- Enhancing the test server for development
- Improve documentation
