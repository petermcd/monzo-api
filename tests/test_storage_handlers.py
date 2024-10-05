"""Test storage hamdlers."""
import json
from typing import Dict, Union

import pytest

from monzo.handlers.filesystem import FileSystem


class TestStorageHandlers():
    """Test storage handlers."""

    @pytest.mark.parametrize(
        'storage,args,expected_response,expected_exception',
        [
            [
                FileSystem,
                {
                    'file': './tests/storage/nonexistant.json',
                },
                {},
                None,
            ],
            [
                FileSystem,
                {
                    'file': './tests/storage/standard.json',
                },
                {
                    "access_token": "token_123",
                    "client_id": "id_123",
                    "client_secret": "secret_123",
                    "expiry": 1234,
                    "refresh_token": "refresh_123",
                },
                None,
            ],
        ],
    )
    def test_filesystem_fetch(
            self, storage,
            args: Dict[str, str],
            expected_response: Dict[str, Union[int, str]],
            expected_exception
    ):
        """
        Test to ensure that fetching using Filesystem storage behaves as expected.

        Args:
            storage (FileSystem): FileSystem.
            args (dict): Arguments to pass to storage.
            expected_response (dict): Expected response from call to fetch.
            expected_exception (Exception): Expected exception when calling fetch.
        """
        fs = storage(**args)
        if expected_exception:
            with pytest.raises(expected_exception):
                assert fs.fetch() == expected_response
        else:
            assert fs.fetch() == expected_response

    @pytest.mark.parametrize(
        'args,expected_data',
        [
            [
                {
                    "access_token": "token_123",
                    "client_id": "id_123",
                    "client_secret": "secret_123",
                    "expiry": 1234,
                    "refresh_token": "refresh_123",
                },
                {
                    "access_token": "token_123",
                    "client_id": "id_123",
                    "client_secret": "secret_123",
                    "expiry": 1234,
                    "refresh_token": "refresh_123",
                },
            ],
            [
                {
                    "access_token": "token_123",
                    "client_id": "id_123",
                    "client_secret": "secret_123",
                    "expiry": 1234,
                },
                {
                    "access_token": "token_123",
                    "client_id": "id_123",
                    "client_secret": "secret_123",
                    "expiry": 1234,
                    "refresh_token": "",
                },
            ],
        ],
    )
    def test_filesystem_store(self, args: Dict[str, str], expected_data: str, mocker):
        """
        Test to ensure the data stored in the Filesystem storage is as expected.

        Args:
            args: Arguments to pass to storage.
            expected_data: Expected response from call to store.
            mocker: Mocker fixture.
        """
        fs = FileSystem('dummy_file.json')
        fh = mocker.patch('builtins.open')
        fs.store(**args)
        fh.assert_has_calls(
            [
                mocker.call().__enter__().write(json.dumps(expected_data)),
            ]
        )
