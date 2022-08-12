"""Class to manage transactions."""
from __future__ import annotations

from json import dumps
from typing import Any, Dict, List, Optional, Union

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo

RECEIPTS_PATH = '/transaction-receipts'

ITEM_TYPE = Dict[str, Union[float, Optional[int], str, List[Dict[str, Union[float, Optional[int], str]]]]]
MERCHANT_TYPE = Dict[str, Union[bool, str]]
PAYMENT_TYPE = Dict[str, Union[int, str]]
TAX_TYPE = Dict[str, Union[int, str]]


class ReceiptItem(object):
    """
    Class for Receipt Items.

    Class to configure receipt items and sub items.
    """

    __slots__ = (
        '_amount',
        '_currency',
        '_description',
        '_quantity',
        '_sub_items',
        '_tax',
        '_unit',
    )

    def __init__(
            self,
            description: str,
            amount: int,
            currency: str,
            quantity: float = 0,
            unit: str = '',
            tax: int = 0,
    ):
        """
        Initialise ReceiptItem.

        Args:
            description: Item description
            amount: The item amount in pence/cents
            currency: The currency the item amount is in
            quantity: The number of this item purchased or for example the weight
            unit: The unit the quantity is in for example KG
            tax: The tax amount in pence/cents for the individual item
        """
        self._amount = amount
        self._currency = currency
        self._description = description
        self._quantity = quantity
        self._tax = tax
        self._unit = unit
        self._sub_items: List[ReceiptItem] = []

    def add_sub_item(self, sub_item: ReceiptItem):
        """
        Add a sub item to an item. This should not be carried out to a sub item.

        Args:
            sub_item: Instance of ReceiptItem
        """
        self._sub_items.append(sub_item)

    def as_dict(self) -> Any:
        """
        Export the object as a dict.

        Returns:
            Object as a dict
        """
        # TODO remove the need for Any. Easiest time would be when removing support for Python 3.7:x
        item: Any = {
            'amount': self._amount,
            'currency': self._currency,
            'description': self._description,
            'quantity': self._quantity,
            'tax': self._tax,
            'unit': self._unit,
        }
        sub_item_list: List[Any] = [sub_item.as_dict() for sub_item in self._sub_items]

        item['sub_items'] = sub_item_list

        return item


class Receipt(Monzo):
    """
    Class to manage Receipts.

    Class provides methods create, fetch and delete receipts.
    """

    __slots__ = (
        '_external_id',
        '_transaction_id',
        '_total',
        '_currency',
        '_items',
        '_taxes',
        '_payments',
        '_merchant',
    )

    def __init__(
            self,
            auth: Authentication,
            transaction_id: str,
            external_id: str,
            transaction_total: int,
            transaction_currency: str,
            items: List[ReceiptItem],
    ):
        """
        Initialise Receipt.

        Args:
            auth: Monzo authentication object
            transaction_id: ID of the transaction known to Monzo
            external_id: External ID for the receipt
            transaction_total: The total for the transaction on pence/cents
            transaction_currency: The currency the transaction is in
        """
        self._external_id: str = external_id
        self._transaction_id: str = transaction_id
        self._total = transaction_total
        self._currency = transaction_currency
        self._items: List[ReceiptItem] = items
        self._taxes: List[TAX_TYPE] = []
        self._payments: List[PAYMENT_TYPE] = []
        self._merchant: MERCHANT_TYPE = {}

        super().__init__(auth=auth)

    def add_merchant(
            self,
            name: str,
            online: bool,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            store_name: Optional[str] = None,
            store_address: Optional[str] = None,
            store_postcode: Optional[str] = None,
    ):
        """
        Set the merchant for the receipt.

        Args:
            name: Name of the merchant
            online: True if online store, otherwise False
            phone: Phone number of the store
            email: Email address of the store
            store_name: Name of the store
            store_address: Address of the store
            store_postcode: Postcode of the store
        """
        merchant: MERCHANT_TYPE = {
            'name': name,
            'online': online,
        }
        if phone:
            merchant['phone'] = phone
        if email:
            merchant['email'] = email
        if store_name:
            merchant['store_name'] = store_name
        if store_address:
            merchant['store_address'] = store_address
        if store_postcode:
            merchant['store_postcode'] = store_postcode

        self._merchant = merchant

    def add_tax(
            self,
            description: str,
            amount: int,
            currency: str,
            tax_number: Optional[str] = None,
    ):
        """
        Add receipt tax item.

        Args:
            description: Tax description (such as VAT)
            amount: The tax amount in pence/cents
            currency: The currency the tax is in
            tax_number: The tax number from the receipt
        """
        tax: TAX_TYPE = {
            'description': description,
            'amount': amount,
            'currency': currency,
        }
        if tax_number:
            tax['tax_number'] = tax_number
        self._taxes.append(tax)

    def _create(self) -> None:
        """Create the receipt."""
        data = {
            'transaction_id': self._transaction_id,
            'external_id': self._external_id,
            'total': self._total,
            'currency': self._currency,
            'taxes': self._taxes,
            'payments': self._payments,
            'merchant': self._merchant
        }
        receipt_items: List[ITEM_TYPE] = [item.as_dict() for item in self._items]

        data['items'] = receipt_items

        headers = {
            'Content-Type': 'application/json',
        }

        self._monzo_auth.make_request(
            path=RECEIPTS_PATH,
            authenticated=True,
            method='PUT',
            data=dumps(data),
            headers=headers,
        )

    def _delete(self):
        """Delete the current receipt."""
        data = {
            'external_id': self._external_id
        }
        self._monzo_auth.make_request(path=RECEIPTS_PATH, data=data, method='DELETE')

    @property
    def external_id(self) -> str:
        """
        Property for the receipt external ID.

        Returns:
            External ID as a string
        """
        return self._external_id

    @property
    def receipt_currency(self) -> str:
        """
        Property for the receipt currency.

        Returns:
            Receipt currency as a string
        """
        return self._currency

    @property
    def receipt_items(self) -> List[ReceiptItem]:
        """
        Property for the items in a receipt.

        Returns:
            List of receipt items and sub items
        """
        return self._items

    @property
    def receipt_merchant(self) -> MERCHANT_TYPE:
        """
        Property for the merchants in a receipt.

        Returns:
            List of receipt merchant items
        """
        return self._merchant

    @property
    def receipt_payments(self) -> List[PAYMENT_TYPE]:
        """
        Property for the payments in a receipt.

        Returns:
            List of receipt payment items
        """
        return self._payments

    @property
    def receipt_taxes(self) -> List[TAX_TYPE]:
        """
        Property for the taxes in a receipt.

        Returns:
            List of receipt tax items
        """
        return self._taxes

    @property
    def receipt_total(self) -> int:
        """
        Property for the receipt total.

        Returns:
            Receipt total as an int in pence/cents
        """
        return self._total

    @property
    def transaction_id(self) -> str:
        """
        Property for the Monzo transaction ID.

        Returns:
            Transaction ID as a string
        """
        return self._transaction_id

    @classmethod
    def create(cls, auth: Authentication, receipt: Receipt) -> Receipt:
        """
        Create a receipt.

        Args:
            auth: Monzo authentication object. Left in to conform to the standard
            receipt: Receipt object

        Returns:
            Created receipt
        """
        receipt._monzo_auth = auth
        receipt._create()
        return receipt

    @classmethod
    def delete(cls, receipt: Receipt) -> None:
        """
        Delete an existing Receipt.

        Args:
            receipt: Receipt requiring deletion
        """
        receipt._delete()

    @classmethod
    def fetch(cls, auth: Authentication, external_id: str) -> List[Receipt]:
        """
        Fetch receipt with the given external ID.

        Args:
            auth: Monzo authentication object
            external_id: External ID of the receipt to fetch

        Returns:
            List of receipts objects for the external ID
        """
        data = {'external_id': external_id}
        res = auth.make_request(path=RECEIPTS_PATH, data=data)
        receipt_data = res['data']['receipt']
        receipt_items: List[ReceiptItem] = []
        for item in receipt_data['items']:
            quantity = item['quantity'] if 'quantity' in item else None
            tax = item['tax'] if 'tax' in item else None
            unit = item['unit'] if 'unit' in item else None
            receipt_item: ReceiptItem = ReceiptItem(
                description=item['description'],
                amount=item['amount'],
                currency=item['currency'],
                quantity=quantity,
                unit=unit,
                tax=tax,
            )

            for sub_item in item['sub_items']:
                sub_item_quantity = sub_item['quantity'] if 'quantity' in sub_item else None
                sub_item_tax = sub_item['tax'] if 'tax' in sub_item else None
                sub_item_unit = sub_item['unit'] if 'unit' in sub_item else None
                receipt_sub_item = ReceiptItem(
                    description=sub_item['description'],
                    amount=sub_item['amount'],
                    currency=sub_item['currency'],
                    quantity=sub_item_quantity,
                    unit=sub_item_unit,
                    tax=sub_item_tax,
                )
                receipt_item.add_sub_item(sub_item=receipt_sub_item)

            receipt_items.append(receipt_item)

        receipt: Receipt = Receipt(
            auth=auth,
            transaction_id=receipt_data['transaction_id'],
            external_id=receipt_data['external_id'],
            transaction_total=receipt_data['total'],
            transaction_currency=receipt_data['currency'],
            items=receipt_items,
        )

        if receipt_data['merchant']['name']:
            merchant_data = receipt_data['merchant']
            receipt.add_merchant(
                name=merchant_data['name'],
                online=merchant_data['online'],
                phone=merchant_data['phone'],
                email=merchant_data['email'],
                store_name=merchant_data['store_name'],
                store_address=merchant_data['store_address'],
                store_postcode=merchant_data['store_postcode'],
            )

        if len(receipt_data['taxes']):
            for tax_data in receipt_data['taxes']:
                receipt.add_tax(
                    description=tax_data['description'],
                    amount=tax_data['amount'],
                    currency=tax_data['currency'],
                    tax_number=tax_data['tax_number'],
                )

        return [receipt]
