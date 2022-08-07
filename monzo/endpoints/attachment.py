"""Class to manage Attachments."""
from __future__ import annotations

from datetime import datetime
from os.path import getsize, isfile, splitext
from urllib.parse import urlparse

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo
from monzo.exceptions import MonzoGeneralError
from monzo.helpers import create_date

SUPPORTED_ATTACHMENT_EXTENSIONS = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpg',
    'png': 'image/png',
}


class Attachment(Monzo):
    """
    Class to manage attachments.

    Class provides methods to manage attachments.
    """

    __slots__ = [
        '_attachment_id',
        '_user_id',
        '_transaction_id',
        '_url',
        '_file_type',
        '_created',
    ]

    def __init__(
            self,
            auth: Authentication,
            attachment_id: str,
            user_id: str,
            transaction_id: str,
            url: str,
            file_type: str,
            created: datetime
    ):
        """
        Initialize Attachment.

        Args:
            auth: Monzo authentication object
            attachment_id: The unique ID for the attachment
            user_id: User ID transaction is associated with
            transaction_id: Transaction ID for the transaction attachment is associated with
            url: URL of the image attachment
            file_type: File type for attachment
            created: Datetime object identifying whe the attachment was created
        """
        self._attachment_id = attachment_id
        self._user_id = user_id
        self._transaction_id = transaction_id
        self._url = url
        self._file_type = file_type
        self._created = created
        super().__init__(auth=auth)

    @property
    def attachment_id(self) -> str:
        """
        Property to output attachment ID.

        Returns:
            Attachment ID
        """
        return self._attachment_id

    @property
    def transaction_id(self) -> str:
        """
        Property to output transaction ID.

        Returns:
            Transaction ID
        """
        return self._transaction_id

    @property
    def url(self) -> str:
        """
        Property to output attachment URL.

        Returns:
            Attachment URL
        """
        return self._url

    @property
    def file_type(self) -> str:
        """
        Property to output attachment file type.

        Returns:
            Attachment file type
        """
        return self._transaction_id

    @property
    def created(self) -> datetime:
        """
        Property to output attachment creation time.

        Returns:
            Attachment creation datetime
        """
        return self._created

    def delete(self) -> None:
        """Delete the attachment."""
        data = {
            'id': self.attachment_id
        }
        self._monzo_auth.make_request(
            path='/attachment/deregister',
            method='POST',
            data=data,
        )

    @classmethod
    def create_attachment(
        cls,
        auth: Authentication,
        transaction_id: str,
        url: str
    ) -> Attachment:
        """
        Create a new image attachment.

        Creates an image attachment, if the URL is a file system URL the file is uploaded, otherwise the URL is used.

        Args:
            auth: Monzo authentication object
            transaction_id: ID of the transaction to associate the attachment with
            url: URL of the transaction

        Returns:
            Created attachment
        """
        file_url = urlparse(url)
        _, file_extension = splitext(url)
        if file_extension not in SUPPORTED_ATTACHMENT_EXTENSIONS:
            raise MonzoGeneralError('Unsupported file type')
        file_type = SUPPORTED_ATTACHMENT_EXTENSIONS[file_extension]
        if file_url.netloc:
            file_type = Attachment._upload_file(auth=auth, url=url, file_type=file_type)

        data = {
            'external_id': transaction_id,
            'file_type': file_type,
            'file_url': file_url,
        }
        response = auth.make_request(
            path='',
            method='POST',
            data=data
        )

        if response['code'] != 200:
            raise MonzoGeneralError('Failed to create attachment')

        return Attachment(
            auth=auth,
            attachment_id=response['data']['attachment']['id'],
            user_id=response['data']['attachment']['user_id'],
            transaction_id=response['data']['attachment']['external_id'],
            url=response['data']['attachment']['file_url'],
            file_type=response['data']['attachment']['file_type'],
            created=create_date(response['data']['attachment']['created']),
        )

    @classmethod
    def _upload_file(cls, auth: Authentication, url: str, file_type: str) -> str:
        """
        Create an upload bucket for the attachment and upload the file.

        Args:
            auth: Monzo authentication object
            url: URL for the file to upload
            file_type: Mime type for the file

        Returns:
            URL of the uploaded file
        """
        if not isfile(url):
            raise MonzoGeneralError('File does not exist')
        content_length = getsize(url)
        data = {
            'file_name': None,
            'file_type': file_type,
            'content_length': content_length,
        }
        response = auth.make_request(
            path='',
            method='POST',
            data=data,
        )
        #  TODO upload file
        return response['data']['file_url']
