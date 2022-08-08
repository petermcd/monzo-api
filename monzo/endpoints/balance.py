"""Class to manage balance."""
from __future__ import annotations

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo


class Balance(Monzo):
    """
    Class to manage balances.

    Class provides methods to fetch account balances. To properly utilise the class the Account class should be
    utilised along with the balance property. Otherwise you can fetch an accounts balance utilising the fetch
    class method.
    """

    __slots__ = ['_balance', '_total_balance', '_currency', '_spend_today']

    def __init__(self, auth: Authentication, balance: int, total_balance: int, currency: str, spend_today: str):
        """
        Initialize Balance.

        Args:
            balance: Balance of the account
            total_balance: Balance of account and associated pots
            currency: Currency the balances are in
            spend_today: Amount spent on the current day
        """
        self._balance = balance
        self._total_balance = total_balance
        self._currency = currency
        self._spend_today = spend_today
        super().__init__(auth=auth)

    @property
    def balance(self) -> int:
        """
        Property for the balance.

        Returns:
            Balance for the account in pence/cents
        """
        return self._balance

    @property
    def currency(self) -> str:
        """
        Property for the currency.

        Returns:
            Currency the balances are in
        """
        return self._currency

    @property
    def spend_today(self) -> str:
        """
        Property for total spent today.

        Returns:
            Total spend today in pence/cents
        """
        return self._spend_today

    @property
    def total_balance(self) -> int:
        """
        Property for the total balance.

        Returns:
            Total balance for the account in pence/cents
        """
        return self._total_balance

    @classmethod
    def fetch(cls, auth: Authentication, account_id: str) -> Balance:
        """
        Implement and instantiates an Account object.

        Args:
             auth: Monzo authentication object
             account_id: Account to fetch the balance for

        Returns:
            Balance object for the account
        """
        data = {'account_id': account_id}
        res = auth.make_request(path='/balance', data=data)
        return Balance(
            auth=auth,
            balance=res['data']['balance'],
            total_balance=res['data']['total_balance'],
            currency=res['data']['currency'],
            spend_today=res['data']['spend_today'],
        )
