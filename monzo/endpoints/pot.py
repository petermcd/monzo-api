"""Class to manage pots."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from monzo.authentication import Authentication
from monzo.endpoints.balance import Balance
from monzo.endpoints.monzo import Monzo
from monzo.exceptions import MonzoGeneralError
from monzo.helpers import create_date


class Pot(Monzo):
    """
    Class to manage pots.

    Class provides methods to fetch pots as well as depositing and withdrawing from pots.
    """

    __slots__ = [
        '_pot_id',
        '_name',
        '_style',
        '_balance',
        '_currency',
        '_created',
        '_updated',
        '_deleted',
    ]

    def __init__(
            self,
            auth: Authentication,
            pot_id: str,
            name: str,
            style: str,
            balance: int,
            currency: str,
            created: datetime,
            updated: datetime,
            deleted: bool
    ):
        """
        Initialize Pot.

        Args:
            auth: Monzo authentication object
            pot_id: The unique ID for the pot
            name: The name you have given the pot
            style: Image style chosen for the pot
            balance: Current balance in the pot in pence/cents
            currency: The currency the pot is in
            created: Date and time the pot was created
            updated: Date and time the pot was updated
            deleted: True if the pot has been deleted otherwise False
        """
        self._pot_id = pot_id
        self._name = name
        self._style = style
        self._balance = balance
        self._currency = currency
        self._created = created
        self._updated = updated
        self._deleted = deleted
        super().__init__(auth=auth)

    @property
    def balance(self) -> int:
        """
        Property for the pot balance.

        Returns:
            Balance of the pot in pence/cents
        """
        return self._balance

    @property
    def created(self) -> datetime:
        """
        Property for when the pot was created.

        Returns:
            Datetime object for when the pot was created
        """
        return self._created

    @property
    def currency(self) -> str:
        """
        Property for pot currency.

        Returns:
            Pot currency
        """
        return self._currency

    @property
    def deleted(self) -> bool:
        """
        Property for identifying if the pot is deleted.

        Returns:
            True if the pot is deleted otherwise False
        """
        return self._deleted

    @property
    def name(self) -> str:
        """
        Property for the pot name.

        Returns:
            The pot name
        """
        return self._name

    @property
    def pot_id(self) -> str:
        """
        Property for pot id.

        Returns:
            ID of the pot
        """
        return self._pot_id

    @property
    def style(self) -> str:
        """
        Property for the pot display style.

        Returns:
            Pot display style
        """
        return self._style

    @property
    def updated(self) -> datetime:
        """
        Property for when the pot was last updated.

        Returns:
            Datetime object for when the pot was last updated
        """
        return self._updated

    @classmethod
    def deposit(cls, auth: Authentication, pot: Pot, account_id: str, amount: int, dedupe_id: str) -> Pot:
        """
        Deposit funds from an account into a pot.

        Args:
            auth: Monzo authentication object
            pot: Pot to deposit funds into
            account_id: ID of the account to withdraw funds into
            amount: Amount in pence/cents to withdraw from pot
            dedupe_id: Unique ID for the request, must be maintained between retries

        Raises:
            MonzoGeneralError: On attempting to withdraw from an account that does not have sufficient funds

        Returns:
            Updated pot
        """
        account_balance_obj = Balance.fetch(auth=auth, account_id=account_id)
        account_balance = account_balance_obj.balance

        if account_balance < amount:
            raise MonzoGeneralError('The account does not contain enough funds')
        path = f'/pots/{pot.pot_id}/deposit'
        data = {
            'source_account_id': account_id,
            'amount': amount,
            'dedupe_id': dedupe_id
        }
        res = auth.make_request(path=path, method='PUT', data=data)
        return cls._update_pot(pot=pot, data=res['data'])

    @classmethod
    def fetch(cls, auth: Authentication, account_id: str) -> List[Pot]:
        """
        Fetch a list of pots associated with an account.

        Args:
            auth: Monzo authentication object
            account_id: Account ID to fetch pots for

        Returns:
            List of pots
        """
        data = {
            'current_account_id': account_id
        }
        res = auth.make_request(path='/pots', data=data)
        pot_list = []
        for pot_item in res['data']['pots']:
            pot = Pot(
                auth=auth,
                pot_id=pot_item['id'],
                name=pot_item['name'],
                style=pot_item['style'],
                balance=pot_item['balance'],
                currency=pot_item['currency'],
                created=create_date(pot_item['created']),
                updated=create_date(pot_item['updated']),
                deleted=pot_item['deleted'],
            )
            pot_list.append(pot)
        return pot_list

    @classmethod
    def fetch_single(cls, auth: Authentication, account_id: str, pot_id: str) -> Optional[Pot]:
        """
        Fetch a list of pots associated with an account.

        Args:
            auth: Monzo authentication object
            account_id: Account ID to fetch pots for

        Returns:
            List of pots
        """
        pots = Pot.fetch(auth=auth, account_id=account_id)
        return next((pot for pot in pots if pot.pot_id == pot_id), None)

    @classmethod
    def withdraw(cls, auth: Authentication, pot: Pot, account_id: str, amount: int, dedupe_id: str) -> Pot:
        """
        Withdraw funds from a pot into an account.

        Args:
            auth: Monzo authentication object
            pot: Pot to withdraw funds from
            account_id: ID of the account to withdraw funds into
            amount: Amount in pence/cents to withdraw from pot
            dedupe_id: Unique ID for the request, must be maintained between retries

        Raises:
            MonzoGeneralError: On attempting to withdraw from a pot that does not have sufficient funds

        Returns:
            Updated pot
        """
        if amount > pot.balance:
            raise MonzoGeneralError('The pot does not contain enough funds')
        path = f'/pots/{pot.pot_id}/withdraw'
        data = {
            'destination_account_id': account_id,
            'amount': amount,
            'dedupe_id': dedupe_id
        }
        res = auth.make_request(path=path, method='PUT', data=data)
        return cls._update_pot(pot=pot, data=res['data'])

    @classmethod
    def _update_pot(cls, pot: Pot, data: Dict[str, Any]) -> Pot:
        """
        Update a provided pot from a result received from a request.

        Args:
            pot: Pot to be updated
            data: Data to update the pot using

        Returns:
            Updated pot
        """
        pot._balance = data['balance']
        pot._created = create_date(data['created'])
        pot._updated = create_date(data['updated'])

        return pot
