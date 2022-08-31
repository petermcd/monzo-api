"""Collection of exceptions the codebase may throw."""


class MonzoError(Exception):
    """
    Parent Monzo exception.

    Exception all other Monzo exceptions inherit from
    """

    pass


class MonzoAuthenticationError(MonzoError):
    """
    Authentication error exception.

    Exception to be thrown when Authentication failure has occurred at any point in dealing with the API
    """

    pass


class MonzoHTTPError(MonzoError):
    """
    HTTP error exception.

    Exception to be thrown when a HTTP error occurs during an API call
    """

    pass


class MonzoArgumentError(MonzoError):
    """
    Argument error exception.

    Exception to be thrown when an invalid value has been passed as an argument to an endpoint
    """

    pass


class MonzoServerError(MonzoError):
    """
    Errors from 5xx error codes.

    Exception usually caused by an issue on the Monzo servers
    """

    pass


class MonzoPermissionsError(MonzoError):
    """
    Permissions error exception.

    The API is logged in but insufficient permissions to perform the query
    """

    pass


class MonzoRateError(MonzoError):
    """
    Rate error exception.

    Exception to be thrown when a Monzo advise you are exceeding the rate limit for the API
    """

    pass


class MonzoGeneralError(MonzoError):
    """
    General error exception.

    Exception to be thrown when a general error occurs that do not fit into other exception types
    """

    pass
