# Monzo Setup

Prior to being able to use the Monzo API you need to set it up.

## Create A Client

Our first step is to obtain an access token from Monzo. To do this log into the
[Monzo Developer Platform](https://developers.monzo.com/).

* Click on "Sign in with your Monzo account"
* Click "Continue to login"
* Enter the email address registered with Monzo
* You will receive an email, click on "Log in to Monzo"
* Open the Monzo app and approve the request
* Click on "Clients"
* Click "New OAUTH Client"
* Enter the following details
  * Name - Choose a name that will easily identify the usage
  * Logo URL - A URL for a logo but this can be left blank
  * Redirect URL's - The URL used for redirecting users during authentication
  * Description - Enter a description
  * Confidentiality - Confidential
* Click "Submit"
* In the page you should now copy the following items for use:
  * Client ID
  * Owner ID
  * Client Secret (red text below the main items)

## Revoking A Token

In the event you have decided you no longer wish to use the client the following
steps should be taken to remove the client:

* Click on "Sign in with your Monzo account"
* Click "Continue to login"
* Enter the email address registered with Monzo
* You will receive an email, click on "Log in to Monzo"
* Open the Monzo app and approve the request
* Click on "Clients"
* Click on the client you wish to revoke
* Click "Revoke Client"

The client will now be fully revoked and the API configured with these client
details will no longer work in the API.

## Issues

### Client Details Not Showing

When creating the token, if the new token does not appear this is likely
caused by forgetting to approve the developer login within the Monzo app.

To rectify simply approve the request and refresh the developer tools page.

### I Didn't Get A Refresh Token

The refresh token is obtained when obtaining an access token. In the event 
you did not receive this, when creating a client you likely chose Not Confidential.

To resolve you can go back to the client list on the developer site and modify.
