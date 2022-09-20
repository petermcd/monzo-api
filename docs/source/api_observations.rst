API Observations
=====================================

While working with the API I often come across peculiarities with the API.
These will be posted here.

Transactions
-------------------------------------
Although the accounts provide all the different types including:

* Current Account
* Loan
* Flex
* Flex Backing Loan

Only current account and Flex actually have the ability to return transactions.

The API call to fetch transactions will work but return no transactions.

The API call for Flex Backing Loan will result in a 403 Forbidden HTTP response from the API.

Monzo support have confirmed these account types are not supported by the transaction endpoint.

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
