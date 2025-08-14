import pytest
from urllib.error import HTTPError
from unittest.mock import patch

from monzo.httpio import HttpIO
from monzo.exceptions import MonzoGeneralError


def test_unknown_status_code_raises_monzogeneralerror():
    http = HttpIO('https://example.com')
    error = HTTPError(url='https://example.com/test', code=418, msg='teapot', hdrs=None, fp=None)
    with patch('monzo.httpio.urlopen', side_effect=error):
        with pytest.raises(MonzoGeneralError):
            http.get('/test')
