"""Collection of exceptions the codebase may throw."""


class MonzoError(Exception):
    """
    Parent Monzo exception.

    Exception all other Monzo exceptions inherit from
    """


class MonzoAuthenticationError(MonzoError):
    """
    Authentication error exception.

    Exception to be thrown when Authentication failure has occurred at any point in dealing with the API
    """


class MonzoHTTPError(MonzoError):
    """
    HTTP error exception.

    Exception to be thrown when an HTTP error occurs during an API call
    """


class MonzoArgumentError(MonzoError):
    """
    Argument error exception.

    Exception to be thrown when an invalid value has been passed as an argument to an endpoint
    """


class MonzoServerError(MonzoError):
    """
    Errors from 5xx error codes.

    Exception usually caused by an issue on the Monzo servers
    """


class MonzoPermissionsError(MonzoError):
    """
    Permissions error exception.

    The API is logged in but does not have enough permissions to perform the query
    """


class MonzoRateError(MonzoError):
    """
    Rate error exception.

    Exception to be thrown when a Monzo advises you are exceeding the rate limit for the API
    """


class MonzoGeneralError(MonzoError):
    """
    General error exception.

    Exception to be thrown when a general error occurs that does not fit into other exception types
    """
