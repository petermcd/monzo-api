import pytest

from monzo.authentication import Authentication
from monzo.endpoints import feed_item
from monzo.exceptions import MonzoArgumentError


class TestFeedItem:
    @pytest.mark.parametrize(
        "account_id, feed_type, params, url, expected_date",
        [
            (
                "mock_account_id",
                "basic",
                {"title": "Test Title", "image_url": "http://example.com/image.png"},
                "",
                {
                    "account_id": "mock_account_id",
                    "type": "basic",
                    "params[title]": "Test Title",
                    "params[image_url]": "http://example.com/image.png",
                },
            ),
            (
                "mock_account_id",
                "basic",
                {"title": "Another Title", "image_url": "http://example.com/image2.png"},
                "http://example.com",
                {
                    "account_id": "mock_account_id",
                    "type": "basic",
                    "url": "http://example.com",
                    "params[title]": "Another Title",
                    "params[image_url]": "http://example.com/image2.png",
                },
            ),
        ],
    )
    def test_create_feed_item(
        self,
        account_id: str,
        feed_type: str,
        params: dict,
        url: str,
        expected_date: dict[str, str],
        mocker,
    ):
        """
        Test the creation of a feed item using the FeedItem class.

        Args:
            account_id: The account ID for which the feed item is being created.
            feed_type: The type of feed item to create (must be in FEED_ITEM_TYPES).
            params: A dictionary of parameters for the feed item.
            url: An optional URL for the feed item.
            expected_date: A dictionary containing the expected data to be sent in the request.
            mocker: Pytest mocker fixture
        """
        mock_make_request = mocker.patch.object(Authentication, "make_request")
        auth = Authentication(
            client_id="mock_client_id",
            client_secret="mock_client_secret",
            redirect_url="http://localhost",
            access_token="mock_access_token",
            access_token_expiry=0,
            refresh_token="mock_refresh_token",
        )

        feed_items: feed_item.FeedItem = feed_item.FeedItem.create(
            auth=auth,
            account_id=account_id,
            feed_type=feed_type,
            params=params,
            url=url,
        )

        assert feed_items._account_id == account_id
        assert feed_items._feed_type == feed_type
        assert feed_items._params == params
        assert feed_items._url == url
        mock_make_request.assert_called_once_with(path="/feed", method="POST", data=expected_date)

    @pytest.mark.parametrize(
        "account_id, feed_type, params, url, expected_exception, expected_exception_message",
        [
            (
                "mock_account_id",
                "complex",
                {"title": "Test Title", "image_url": "http://example.com/image.png"},
                "",
                MonzoArgumentError,
                "Feed type appears invalid",
            ),
            (
                "mock_account_id",
                "basic",
                {"title": "Test Title"},
                "",
                MonzoArgumentError,
                "image_url is a required parameter for basic feed type",
            ),
            (
                "mock_account_id",
                "basic",
                {"image_url": "http://example.com/image.png"},
                "",
                MonzoArgumentError,
                "title is a required parameter for basic feed type",
            ),
            (
                "mock_account_id",
                "basic",
                {},
                "",
                MonzoArgumentError,
                "title is a required parameter for basic feed type",
            ),
        ],
    )
    def test_create_feed_exceptions(
        self,
        account_id: str,
        feed_type: str,
        params: dict,
        url: str,
        expected_exception: type[BaseException],
        expected_exception_message: str,
    ):
        """
        Test the creation of a feed item using the FeedItem class.

        Args:
            account_id: The account ID for which the feed item is being created.
            feed_type: The type of feed item to create (must be in FEED_ITEM_TYPES).
            params: A dictionary of parameters for the feed item.
            url: An optional URL for the feed item.
            expected_exception: The expected exception type to be raised.
            expected_exception_message: The expected exception message to be raised.
            mocker: Pytest mocker fixture
        """
        auth = Authentication(
            client_id="mock_client_id",
            client_secret="mock_client_secret",
            redirect_url="http://localhost",
            access_token="mock_access_token",
            access_token_expiry=0,
            refresh_token="mock_refresh_token",
        )

        with pytest.raises(expected_exception) as exc_info:
            feed_item.FeedItem.create(
                auth=auth,
                account_id=account_id,
                feed_type=feed_type,
                params=params,
                url=url,
            )
        assert exc_info.value.args[0] == expected_exception_message
