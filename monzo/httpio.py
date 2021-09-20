from json import loads
from typing import Any, Dict, Optional
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from monzo.exceptions import MonzoHTTPError

DEFAULT_TIMEOUT = 10

REQUEST_RESPONSE_TYPE = Dict[str, Any]


class HttpIO:
    def __init__(self, url: str):
        """
        Standard init.

        Args:
            url: Base URL for requests
        """
        self._url = url

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
        parameters = None
        if data:
            parameters = urlencode(data)
        if parameters:
            path += f'?{parameters}'
        return self._perform_request(path, data=None, headers=headers, timeout=timeout)

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
        parameters = None
        if data:
            parameters = urlencode(data).encode()
        return self._perform_request(path, data=parameters, headers=headers, timeout=timeout)

    def _perform_request(
            self,
            path: str,
            data: Optional[bytes],
            headers: Dict[str, Any],
            timeout
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Perform a given request.

        Args:
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
            content: str = ''
            response = urlopen(request, timeout=timeout)
            with response as fh:
                content += fh.read().decode('utf-8')
        except URLError:
            raise MonzoHTTPError(f'{full_url} failed to load')
        return {
            'code': response.code,
            'headers': response.headers,
            'data': loads(content),
        }
