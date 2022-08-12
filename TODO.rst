TODO
=====================================

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
      - No Functionality currently broken
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
      -
      - \*\*
      - No

* \* Annotations only appear to work for existing keys such as Notes `view on the forum <https://community.monzo.com/t/annotate-transaction-endpoint-not-working-for-custom-key/121203>`_.
* \*\* It is unlikely that this package will implement usage of the Open Banking API due to restrictions accessing it.

Miscellaneous
-------------------------------------

- Tidy exceptions and ensure scenarios are captured correctly
- Implement testing
- Facilitate receiving webhook calls
- Enhancing the test server for development
- Improve documentation
