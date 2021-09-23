class MonzoAuthenticationError(Exception):
    """
    Authentication error exception.

    Exception to be thrown when Authentication failure has occurred at any point in dealing with the API
    """
    pass


class MonzoHTTPError(Exception):
    """
    HTTP error exception.

    Exception to be thrown when a HTTP error occurs during an API call
    """
    pass


class MonzoArgumentError(Exception):
    """
    Argument error exception.

    Exception to be thrown when an invalid value has been passed as an argument to an endpoint
    """
    pass


class MonzoGeneralError(Exception):
    """
    General error exception.

    Exception to be thrown when a general error occurs that do not fit into other exceptio types
    """
    pass
