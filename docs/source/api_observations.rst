API Observations
=====================================

While working with the API I often come across peculiarities with the API.
These will be posted here.

Transaction Merchants
-------------------------------------

As part of the returned data you are provided with the merchant ID. This can be
expanded to include further information. Merchant information is not present
on the following type of transactions:

* Bank transfers
* Transfers between pots and the main account
* Loan payments to Monzo
* Interest payments to Monzo

There may be others.
