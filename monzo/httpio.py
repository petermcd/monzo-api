"""Class that handles HTTP requests."""
from json import loads
from typing import Any, Dict, Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from monzo.exceptions import (MonzoAuthenticationError, MonzoGeneralError, MonzoHTTPError, MonzoPermissionsError,
                              MonzoRateError, MonzoServerError)

DEFAULT_TIMEOUT = 10

REQUEST_RESPONSE_TYPE = Dict[str, Any]

MONZO_ERROR_MAP = {
    400: MonzoHTTPError,
    401: MonzoAuthenticationError,
    403: MonzoPermissionsError,
    404: MonzoHTTPError,
    405: MonzoGeneralError,
    406: MonzoGeneralError,
    429: MonzoRateError,
    500: MonzoServerError,
    504: MonzoServerError,
}


class HttpIO(object):
    """
    Class to facilitate http requests.

    Underlying class that is utilised for making the API calls to the Monzo API. This class should not be used
    directly, instead the authentication make_request method should be used
    """

    def __init__(self, url: str):
        """
        Initialize HttpIO.

        Args:
            url: Base URL for requests
        """
        self._url = url

    def delete(self, path: str, data=None, headers=None, timeout: int = DEFAULT_TIMEOUT) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a DELETE request.

        Args:
            path: Path for the HTTP call
            data: Data for the request to be passed as URL parameters
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        parameters = urlencode(data).encode() if data else None
        return self._perform_request(method='DELETE', path=path, data=parameters, headers=headers, timeout=timeout)

    def get(self, path: str, data=None, headers=None, timeout: int = DEFAULT_TIMEOUT) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a GET request.

        Args:
            path: Path for the HTTP call
            data: Data for the request to be passed as URL parameters
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        parameters = urlencode(data) if data else None
        if parameters:
            path += f'?{parameters}'
        return self._perform_request(method='GET', path=path, data=None, headers=headers, timeout=timeout)

    def patch(
            self,
            path: str,
            data=None,
            headers=None,
            timeout: int = DEFAULT_TIMEOUT
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a PATCH request.

        Args:
            path: Path for the HTTP call
            data: Data for the request to be passed as form data
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        parameters = urlencode(data).encode() if data else None
        return self._perform_request(method='PATCH', path=path, data=parameters, headers=headers, timeout=timeout)

    def post(
            self,
            path: str,
            data=None,
            headers=None,
            timeout: int = DEFAULT_TIMEOUT
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a POST request.

        Args:
            path: Path for the HTTP call
            data: Data for the request to be passed as form data
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        parameters = urlencode(data).encode() if data else None
        return self._perform_request(method='POST', path=path, data=parameters, headers=headers, timeout=timeout)

    def put(
            self,
            path: str,
            data=None,
            headers=None,
            timeout: int = DEFAULT_TIMEOUT
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a PUT request.

        Args:
            path: Path for the HTTP call
            data: Data for the request to be passed as form data
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if type(data) is dict:
            parameters = urlencode(data).encode() if data else None
        else:
            parameters = data.encode('utf8')
        return self._perform_request(method='PUT', path=path, data=parameters, headers=headers, timeout=timeout)

    def _perform_request(
            self,
            method: str,
            path: str,
            data: Optional[bytes],
            headers: Dict[str, Any],
            timeout
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a given request.

        Args:
            method: HTTP method to use (DELETE, GET, POST, PUT)
            path: Path for the HTTP call
            data: Data for the request to be passed as form data
            headers: Headers as a dictionary for the request
            timeout: Timeout in seconds for the request

        Returns:
             Dictionary containing the response code, headers and content
        """
        full_url = f'{self._url}{path}'
        try:
            request = Request(url=full_url, data=data, headers=headers)
            request.method = method
            content: str = ''
            response = urlopen(request, timeout=timeout)
            with response as fh:
                content += fh.read().decode('utf-8')
        except HTTPError as error:
            raise MONZO_ERROR_MAP[error.code]() from error
        return {
            'code': response.code,
            'headers': response.headers,
            'data': loads(content) if len(content) > 0 else '',
        }
