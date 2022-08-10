"""Class to manage transactions."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo
from monzo.helpers import create_date, format_date

EXPAND_VALID_VALUES = [
    'merchant'
]


class Transaction(Monzo):
    """
    Class to manage transactions.

    Class provides methods to fetch transactions.
    """

    __slots__ = [
        '_account_id',
        '_amount',
        '_amount_is_pending',
        '_atm_fees_detailed',
        '_attachments',
        '_can_add_to_tab',
        '_can_be_excluded_from_breakdown',
        '_can_be_made_subscription',
        '_can_match_transactions_in_categorization',
        '_can_split_the_bill',
        '_categories',
        '_category',
        '_counterparty',
        '_created',
        '_currency',
        '_decline_reason',
        '_dedupe_id',
        '_description',
        '_fees',
        '_include_in_spending',
        '_international',
        '_is_load',
        '_labels',
        '_local_amount',
        '_local_currency',
        '_merchant',
        '_metadata',
        '_notes',
        '_originator',
        '_scheme',
        '_settled',
        '_transaction_id',
        '_updated',
        '_user_id'
    ]

    def __init__(
            self,
            auth: Authentication,
            transaction_data: Dict[str, Any]
    ):
        """
        Initialize Transaction.

        Args:
            auth: Monzo authentication object
            transaction_data: Data returned from an API call
        """
        self._account_id: str = transaction_data['account_id']
        self._amount: int = transaction_data['amount']
        self._amount_is_pending: bool = transaction_data['amount_is_pending']
        self._atm_fees_detailed: str = transaction_data['atm_fees_detailed']
        self._attachments: str = transaction_data['attachments']
        self._can_add_to_tab: bool = transaction_data['can_add_to_tab']
        self._can_be_excluded_from_breakdown: bool = transaction_data['can_be_excluded_from_breakdown']
        self._can_be_made_subscription: bool = transaction_data['can_be_made_subscription']
        self._can_match_transactions_in_categorization: bool = \
            transaction_data['can_match_transactions_in_categorization']
        self._can_split_the_bill: bool = transaction_data['can_split_the_bill']
        self._categories: Dict[str, Union[int, str]] = transaction_data['categories']
        self._category: str = transaction_data['category']
        self._counterparty = transaction_data['counterparty']
        self._created: datetime = create_date(transaction_data['created'])
        self._currency: str = transaction_data['currency']
        self._dedupe_id: str = transaction_data['dedupe_id']
        self._decline_reason: str = transaction_data.get('decline_reason', '')
        self._description: str = transaction_data['description']
        self._fees: Dict[str, Any] = transaction_data['fees']
        self._include_in_spending: bool = transaction_data['include_in_spending']
        self._international: Optional[str] = transaction_data['international']
        self._is_load: bool = transaction_data['is_load']
        self._labels: str = transaction_data['labels']
        self._local_amount: int = transaction_data['local_amount']
        self._local_currency: str = transaction_data['local_currency']
        self._merchant: str = transaction_data['merchant']
        self._metadata: Dict[str, str] = transaction_data['metadata']
        self._notes: str = transaction_data['notes']
        self._originator: bool = transaction_data['originator']
        self._scheme: str = transaction_data['scheme']
        self._settled: Optional[datetime] = None
        if transaction_data['settled']:
            self._settled = create_date(transaction_data['settled'])
        self._transaction_id: str = transaction_data['id']
        self._updated: datetime = create_date(transaction_data['updated'])
        self._user_id: str = transaction_data['user_id']

        super().__init__(auth=auth)

    @property
    def account_id(self) -> str:
        """
        Property for the account ID the transaction is associated with.

        Returns:
            Account ID
        """
        return self._account_id

    @property
    def amount(self) -> int:
        """
        Property for the transaction amount.

        Returns:
            Transaction amount in pence/cents
        """
        return self._amount

    @property
    def amount_is_pending(self) -> bool:
        """
        Property to identify if amount is pending.

        Returns:
            True if transaction is pending
        """
        return self._amount_is_pending

    @property
    def atm_fees_detailed(self) -> Optional[str]:
        """
        Property for detailed atm fees.

        Returns:
            ATM fee details
        """
        return self._atm_fees_detailed

    @property
    def attachments(self) -> Optional[str]:
        """
        Property for attachments.

        Returns:
            Attachment details
        """
        return self._attachments

    @property
    def can_add_to_tab(self) -> bool:
        """
        Property to identify if transaction can be added to tab.

        Returns:
            True if transaction can be added to tab otherwise False
        """
        return self._can_add_to_tab

    @property
    def can_be_excluded_from_breakdown(self) -> bool:
        """
        Property to identify if transaction can be excluded from breakdown.

        Returns:
            True if transaction can be excluded from breakdown otherwise False
        """
        return self._can_be_excluded_from_breakdown

    @property
    def can_be_made_subscription(self) -> bool:
        """
        Property to identify if a transaction can be made into a subscription.

        Returns:
            True if transaction can be made into a subscription otherwise False
        """
        return self._can_be_made_subscription

    @property
    def can_match_transactions_in_categorization(self) -> bool:
        """
        Property to identify if transaction could be added to a category.

        Returns:
            True if the transaction could be added to a category otherwise False
        """
        return self._can_match_transactions_in_categorization

    @property
    def can_split_the_bill(self) -> bool:
        """
        Property to identify if a transaction can be split.

        Returns:
            True if a transaction can be split otherwise False
        """
        return self._can_split_the_bill

    @property
    def categories(self) -> Dict[str, Union[int, str]]:
        """
        Property to identify categories a transaction is a member of.

        Returns:
            Dictionary of categories a transaction is a member of
        """
        return self._categories

    @property
    def category(self) -> str:
        """
        Property to identify category a transaction is a member of.

        Returns:
            Category a transaction is a member of
        """
        return self._category

    @property
    def counterparty(self) -> Dict[str, str]:
        """
        Property to identify counterparty.

        #TODO identify what counterparty is

        Returns:
            Counterparty
        """
        return self._counterparty

    @property
    def created(self) -> datetime:
        """
        Property timestamp a transaction was created.

        Returns:
            Transaction time creation timestamp
        """
        return self._created

    @property
    def currency(self) -> str:
        """
        Property to identify transaction currency.

        Returns:
            Currency a transaction is in
        """
        return self._currency

    @property
    def dedupe_id(self) -> str:
        """
        Property for Dedupe ID.

        Returns:
            Dedupe ID for a transaction
        """
        return self._dedupe_id

    @property
    def decline_reason(self) -> str:
        """
        Property for the reason a transaction was declined.

        Returns:
            Decline reason for a transaction or an empty string
        """
        return self._decline_reason

    @property
    def description(self) -> str:
        """
        Property for transaction description.

        Returns:
            Transaction description
        """
        return self._description

    @property
    def fees(self) -> Dict[str, Any]:
        """
        Property for transaction fees.

        Returns:
            Dictionary of fees associated with a transaction
        """
        return self._fees

    @property
    def include_in_spending(self) -> bool:
        """
        Property for to identify if a transaction should be included in spending.

        Returns:
            True if a transaction should be included in spending otherwise False
        """
        return self._include_in_spending

    @property
    def international(self) -> Optional[str]:
        """
        UNCLEAR.

        #TODO identify what this is

        Returns:
            UNCLEAR
        """
        return self._international

    @property
    def is_load(self) -> bool:
        """
        Property for is_load.

        Returns:
            True if a positive transaction was due to a deposit otherwise False
        """
        return self._is_load

    @property
    def labels(self) -> str:
        """
        Property for labels associated with a transaction.

        Returns:
            Labels associated with a transaction
        """
        return self._labels

    @property
    def local_amount(self) -> int:
        """
        Property for the local value of a transaction.

        Returns:
            Local value of a transaction in pence/cents
        """
        return self._local_amount

    @property
    def local_currency(self) -> str:
        """
        Property for the local currency of a transaction.

        Returns:
            Local currency of a transaction
        """
        return self._local_currency

    @property
    def merchant(self) -> str:
        """
        Property for merchant information for a transaction.

        Returns:
            Transaction merchant information
        """
        return self._merchant

    @property
    def metadata(self) -> Dict[str, str]:
        """
        Property for metadata associated with a transaction.

        Returns:
            Transaction metadata information
        """
        return self._metadata

    @property
    def notes(self) -> str:
        """
        Property for notes associated with a transaction.

        Returns:
            Transaction notes
        """
        return self._notes

    @property
    def originator(self) -> bool:
        """
        Property to identify if you are the originator of a transaction.

        Returns:
            True if you are the originator of a transaction otherwise False
        """
        return self._originator

    @property
    def scheme(self) -> str:
        """
        UNCLEAR.

        #TODO identify what this is

        Returns:
            UNCLEAR
        """
        return self._scheme

    @property
    def settled(self) -> Optional[datetime]:
        """
        Property for when a transaction was settled.

        Returns:
            datetime of when the transaction was settled, if None transaction is not settled yet
        """
        return self._settled

    @property
    def transaction_id(self) -> str:
        """
        Property for the transaction ID.

        Returns:
            ID for the transaction
        """
        return self._transaction_id

    @property
    def updated(self) -> Optional[datetime]:
        """
        Property for when a transaction was updated.

        Returns:
            datetime of when the transaction was last updated
        """
        return self._updated

    @property
    def user_id(self) -> str:
        """
        UNKNOWN.

        #TODO Identify what this is

        Returns:
            UNKNOWN
        """
        return self._user_id

    def annotate(
            self,
            key: str,
            value: str = '',
    ):
        """
        Annotate the transaction.

        Functionality on Monzo currently appears to be broken when using custom keys, this works with the Notes key
        however will override the existing notes.

        Args:
            key: Key for the annotation.
            value: Value for annotation, if left blank it will remove the annotation.
        """
        path = f'/transactions/{self.transaction_id}'
        data = {
            f'metadata[{key}]': value,
        }
        res = self._monzo_auth.make_request(path=path, method='PATCH', data=data)
        self._notes = res['data']['transaction']['notes']
        self._metadata = res['data']['transaction']['metadata']

    @classmethod
    def fetch_single(
            cls,
            auth: Authentication,
            transaction_id: str,
            expand_on: str = 'merchant'
    ) -> Optional[Transaction]:
        """
        Fetch a transaction with a specific ID.

        Args:
            auth: Monzo authentication object
            transaction_id: Transaction ID for the transaction to fetch
            expand_on: Field to expand. must be contained in EXPAND_VALID_VALUES

        Returns:
            Transaction if it exists otherwise None
        """
        data = {}
        if expand_on and expand_on.lower() in EXPAND_VALID_VALUES:
            data = {
                'expand[]': expand_on,
            }
        path = f'/transactions/{transaction_id}'
        res = auth.make_request(path=path, data=data)
        if len(res['data'].get('transaction', {})) == 0:
            return None
        return Transaction(auth=auth, transaction_data=res['data']['transaction'])

    @classmethod
    def fetch(
            cls,
            auth: Authentication,
            account_id: str,
            since: Optional[datetime] = None,
            before: Optional[datetime] = None,
            expand=None,
    ) -> List[Transaction]:
        """
        Fetch a list of transaction.

        Args:
            auth: Monzo authentication object
            account_id: ID of the account to fetch transactions for
            since: Datetime object to identify when returned transactions should be made since
            before: Datetime object to identify when returned transactions should be made before
            expand: List if fields to expand on

        Returns:
            List of transaction
        """
        if expand is None:
            expand = []
        data = {
            'account_id': account_id,
        }
        if expand:
            # TODO fix so that this works on the list
            data['expand'] = expand[0]
        if since:
            data['since'] = format_date(since)
        if before:
            data['before'] = format_date(before)
        path = '/transactions'
        res = auth.make_request(path=path, data=data)
        transactions = []
        for transaction_data in res['data']['transactions']:
            transaction = Transaction(auth=auth, transaction_data=transaction_data)
            transactions.append(transaction)
        return transactions
