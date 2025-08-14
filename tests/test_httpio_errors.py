from unittest.mock import patch
from urllib.error import HTTPError

import pytest

from monzo.exceptions import MonzoGeneralError
from monzo.httpio import HttpIO


def test_unknown_status_code_raises_monzogeneralerror():
    http = HttpIO('https://example.com')
    error = HTTPError(url='https://example.com/test', code=418, msg='teapot', hdrs=None, fp=None)
    with patch('monzo.httpio.urlopen', side_effect=error):
        with pytest.raises(MonzoGeneralError):
            http.get('/test')
