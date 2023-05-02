"""Class to manage Attachments."""
from __future__ import annotations

from datetime import datetime
from os.path import basename, getsize, isfile, splitext
from typing import TYPE_CHECKING

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo
from monzo.exceptions import MonzoGeneralError
from monzo.helpers import create_date

if TYPE_CHECKING:
    from monzo.endpoints.transaction import Transaction

SUPPORTED_ATTACHMENT_EXTENSIONS = {
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpg',
    '.png': 'image/png',
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
            attachment_data: dict[str, str],
    ):
        """
        Initialize Attachment.

        Args:
            auth: Monzo authentication object
            attachment_data: Transaction data as supplied by Monzo
        """
        self._attachment_id = attachment_data['id']
        self._user_id = attachment_data['user_id']
        self._transaction_id = attachment_data['external_id']
        self._url = attachment_data['file_url']
        self._file_type = attachment_data['file_type']
        self._created = create_date(attachment_data['created'])
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
        transaction: Transaction,
        url: str,
        file_path: str,
    ) -> Attachment:
        """
        Create a new image attachment.

        Creates an image attachment, if the URL is a file system URL the file is uploaded, otherwise the URL is used.

        Args:
            auth: Monzo authentication object
            transaction: ID of the transaction to associate the attachment with
            url: URL of the image, if set file_path is ignored
            file_path: File path of the image

        Raise:
            AttributeError: On failure to provide either a url or file path
            MonzoGeneralError: On unsupported file type

        Returns:
            Created attachment
        """
        if not any([url, file_path]):
            raise AttributeError('Either a URL or file path is required.')
        if file_path:
            _, file_extension = splitext(file_path)
            if file_extension not in SUPPORTED_ATTACHMENT_EXTENSIONS:
                raise MonzoGeneralError('Unsupported file type')
            file_type = SUPPORTED_ATTACHMENT_EXTENSIONS[file_extension]
            url = cls._upload_file(
                auth=auth,
                file_path=file_path,
                file_type=file_type
            )
        else:
            _, file_extension = splitext(url)

        if file_extension not in SUPPORTED_ATTACHMENT_EXTENSIONS:
            raise MonzoGeneralError('Unsupported file type')
        file_type = SUPPORTED_ATTACHMENT_EXTENSIONS[file_extension]

        data = {
            'external_id': transaction.transaction_id,
            'file_type': file_type,
            'file_url': url,
        }
        response = auth.make_request(
            path='/attachment/register',
            method='POST',
            data=data
        )

        if response['code'] != 200:
            raise MonzoGeneralError('Failed to create attachment')

        return Attachment(
            auth=auth,
            attachment_data=response['data']['attachment'],
        )

    @classmethod
    def _upload_file(cls, auth: Authentication, file_path: str, file_type: str) -> str:
        """
        Create an upload bucket for the attachment and upload the file.

        Args:
            auth: Monzo authentication object
            file_path: Path for the file to upload
            file_type: Mime type for the file

        Raises:
            MonzoGeneralError: on issue reading file

        Returns:
            URL of the uploaded file
        """
        if not isfile(file_path):
            raise MonzoGeneralError('File does not exist')
        content_length = getsize(file_path)
        data = {
            'file_name': basename(file_path),
            'file_type': file_type,
            'content_length': content_length,
        }

        response = auth.make_request(
            path='/attachment/upload',
            method='POST',
            data=data,
        )
        from monzo.httpio import HttpIO

        upload = HttpIO(url=response['data']['upload_url'])
        upload_headers = {
            'Authorization': f'Bearer {auth.access_token}',
            'Content-Type': file_type,
            'Content-Length': getsize(file_path),
        }
        with open(file_path, 'rb') as fh:
            upload.post(
                path='',
                data=fh,
                headers=upload_headers,
            )
        return response['data']['file_url']
