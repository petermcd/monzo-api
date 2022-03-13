"""Class to manage webhooks."""
from __future__ import annotations

from typing import List

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo


class Webhook(Monzo):
    """
    Class to manage webhooks.

    Class provides methods create, fetch and delete webhooks.
    """

    __slots__ = ['_account_id', '_url', '_webhook_id']

    def __init__(self, auth: Authentication, account_id: str, url: str, webhook_id: str):
        """
        Initialize Webhook.

        Args:
            auth: Monzo authentication object
            account_id: Account ID the webhook is associated with
            url: URL to receive account updates
            webhook_id: Webhook ID
        """
        self._account_id = account_id
        self._url = url
        self._webhook_id = webhook_id
        super().__init__(auth=auth)

    def _create(self) -> None:
        """Create the webhook."""
        data = {
            'account_id': self._account_id,
            'url': self._url,
        }
        res = self._monzo_auth.make_request(path='/webhooks', method='POST', data=data)
        self._webhook_id = res['data']['webhook']['id']

    def _delete(self):
        """Delete the current webhook."""
        path = f'/webhooks/{self._webhook_id}'
        self._monzo_auth.make_request(path=path, method='DELETE')

    @property
    def account_id(self) -> str:
        """
        Property for the account ID.

        Returns:
            Account ID for the associated account
        """
        return self._account_id

    @property
    def url(self) -> str:
        """
        Property for the URl.

        Returns:
            URl that receives updates
        """
        return self._url

    @property
    def webhook_id(self) -> str:
        """
        Property for the webhook ID.

        Returns:
            Webhook ID
        """
        return self._webhook_id

    @classmethod
    def create(cls, auth: Authentication, account_id: str, url: str) -> Webhook:
        """
        Create a webhook.

        Args:
            auth: Monzo authentication object
            account_id: Account ID a webhook should be associated with
            url: URL transaction data should be sent too

        Returns:
            Created webhook
        """
        webhook = Webhook(auth=auth, account_id=account_id, url=url, webhook_id='NEW')
        webhook._create()
        return webhook

    @classmethod
    def delete(cls, webhook: Webhook) -> None:
        """
        Delete an existing webhook.

        Args:
            webhook: Webhook requiring deletion
        """
        webhook._delete()

    @classmethod
    def fetch(cls, auth: Authentication, account_id: str) -> List[Webhook]:
        """
        Fetch webhooks for an account.

        Args:
            auth: Monzo authentication object
            account_id: Account to fetch the webhooks for

        Returns:
            List of webhook objects for the account
        """
        data = {'account_id': account_id}
        res = auth.make_request(path='/webhooks', data=data)
        webhooks = []
        for webhook_item in res['data']['webhooks']:
            webhook = Webhook(
                auth=auth,
                account_id=webhook_item['account_id'],
                url=webhook_item['url'],
                webhook_id=webhook_item['id'],
            )
            webhooks.append(webhook)
        return webhooks
