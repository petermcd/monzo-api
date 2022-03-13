"""Class to implement making requests for data from Monzo."""
import datetime
from typing import Any, Dict, List, Optional

from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.endpoints.transaction import Transaction
from monzo.exceptions import MonzoPermissionsError


class MonzoData:
    """Class to query Monzo API."""

    __slots__ = [
        '_accounts',
        '_transactions'
    ]

    def __init__(self):
        """Initialize MonzoData."""
        self._accounts: List[Account] = []
        self._transactions: Dict[str, List[Transaction]] = {}

    def get_accounts(self, auth: Authentication) -> List[Account]:
        """
        Fetch Monzo accounts.

        Args:
            auth: Monzo Authentication object

        Returns:
            List of Account objects
        """
        if not self._accounts:
            self._accounts = Account.fetch(auth=auth)
        return self._accounts

    def get_transactions(self, auth: Authentication, account_id: str) -> List[Transaction]:
        """
        Fetch account transactions.

        Args:
            auth: Monzo Authentication object
            account_id: ID of the account to fetch transactions for

        Returns:
            List of transaction objects
        """
        today = datetime.date.today()
        since_date = today - datetime.timedelta(days=7)
        since = datetime.datetime(
            year=since_date.year,
            month=since_date.month,
            day=since_date.day,
        )
        if not self._transactions or account_id not in self._transactions:
            try:
                transactions = Transaction.fetch(auth=auth, account_id=account_id, since=since, expand=['merchant'])
            except MonzoPermissionsError:
                transactions = []
            self._transactions[account_id] = transactions
        return self._transactions[account_id]

    @staticmethod
    def get_raw_request(
        auth: Authentication,
        path: str,
        authenticated: bool = True,
        request_type: str = 'get',
        headers: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Perform a raw request.

        Args:
            auth: Monzo Authentication object
            path: API path for request
            authenticated: True if call should be authenticated
            request_type: HTTP method to use (DELETE, GET, POST, PUT)
            headers: Dictionary of headers for the request
            parameters: Dictionary of parameters for the request

        Returns:
            List of Account objects
        """
        try:
            res = auth.make_request(
                path=path,
                authenticated=authenticated,
                method=request_type,
                data=parameters,
                headers=headers,
            )
            records = res['data']
        except MonzoPermissionsError:
            records = {'error': 'Permissions error'}
        return records
