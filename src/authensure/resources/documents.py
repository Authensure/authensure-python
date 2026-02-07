"""Documents resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Document


class DocumentsResource:
    """Resource for document operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def upload(
        self,
        envelope_id: str,
        file: bytes,
        filename: str,
        mime_type: str = "application/pdf",
    ) -> Document:
        """
        Upload a document to an envelope.

        Args:
            envelope_id: The envelope ID.
            file: File content as bytes.
            filename: Name of the file.
            mime_type: MIME type (default: 'application/pdf').

        Returns:
            The created document.
        """
        data = self._http.upload_file(
            f"/envelopes/{envelope_id}/documents",
            file,
            filename,
            mime_type,
        )
        return Document.model_validate(data)

    async def upload_async(
        self,
        envelope_id: str,
        file: bytes,
        filename: str,
        mime_type: str = "application/pdf",
    ) -> Document:
        """Async version of upload."""
        data = await self._http.upload_file_async(
            f"/envelopes/{envelope_id}/documents",
            file,
            filename,
            mime_type,
        )
        return Document.model_validate(data)

    def get(self, document_id: str) -> Document:
        """
        Get a document by ID.

        Args:
            document_id: The document ID.

        Returns:
            The document.
        """
        data = self._http.get(f"/documents/{document_id}")
        return Document.model_validate(data)

    async def get_async(self, document_id: str) -> Document:
        """Async version of get."""
        data = await self._http.get_async(f"/documents/{document_id}")
        return Document.model_validate(data)

    def get_signed_url(self, document_id: str) -> dict[str, str]:
        """
        Get a signed URL for downloading a document.

        Args:
            document_id: The document ID.

        Returns:
            Dict containing the signed URL.
        """
        return self._http.get(f"/documents/{document_id}/signed-url")

    async def get_signed_url_async(self, document_id: str) -> dict[str, str]:
        """Async version of get_signed_url."""
        return await self._http.get_async(f"/documents/{document_id}/signed-url")

    def download(self, document_id: str) -> bytes:
        """
        Download a document.

        Args:
            document_id: The document ID.

        Returns:
            Document content as bytes.
        """
        return self._http.get(f"/documents/{document_id}/download")

    async def download_async(self, document_id: str) -> bytes:
        """Async version of download."""
        return await self._http.get_async(f"/documents/{document_id}/download")

    def delete(self, document_id: str) -> dict[str, str]:
        """
        Delete a document.

        Args:
            document_id: The document ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/documents/{document_id}")

    async def delete_async(self, document_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/documents/{document_id}")

    def add_field(
        self,
        document_id: str,
        field_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        page: int,
        recipient_id: str | None = None,
        label: str | None = None,
        placeholder: str | None = None,
        required: bool = True,
    ) -> Any:
        """
        Add a field to a document.

        Args:
            document_id: The document ID.
            field_type: Type of field (signature, text, date, checkbox, etc.).
            x: X position.
            y: Y position.
            width: Field width.
            height: Field height.
            page: Page number.
            recipient_id: Optional recipient ID.
            label: Optional field label.
            placeholder: Optional placeholder text.
            required: Whether field is required (default: True).

        Returns:
            The created field.
        """
        body: dict[str, Any] = {
            "type": field_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "page": page,
            "required": required,
        }
        if recipient_id:
            body["recipientId"] = recipient_id
        if label:
            body["label"] = label
        if placeholder:
            body["placeholder"] = placeholder

        return self._http.post(f"/documents/{document_id}/fields", body)

    async def add_field_async(
        self,
        document_id: str,
        field_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        page: int,
        recipient_id: str | None = None,
        label: str | None = None,
        placeholder: str | None = None,
        required: bool = True,
    ) -> Any:
        """Async version of add_field."""
        body: dict[str, Any] = {
            "type": field_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "page": page,
            "required": required,
        }
        if recipient_id:
            body["recipientId"] = recipient_id
        if label:
            body["label"] = label
        if placeholder:
            body["placeholder"] = placeholder

        return await self._http.post_async(f"/documents/{document_id}/fields", body)

    def update_field(self, document_id: str, field_id: str, **kwargs: Any) -> Any:
        """
        Update a document field.

        Args:
            document_id: The document ID.
            field_id: The field ID.
            **kwargs: Field properties to update.

        Returns:
            The updated field.
        """
        return self._http.patch(f"/documents/{document_id}/fields/{field_id}", kwargs)

    async def update_field_async(self, document_id: str, field_id: str, **kwargs: Any) -> Any:
        """Async version of update_field."""
        return await self._http.patch_async(f"/documents/{document_id}/fields/{field_id}", kwargs)

    def delete_field(self, document_id: str, field_id: str) -> dict[str, str]:
        """
        Delete a document field.

        Args:
            document_id: The document ID.
            field_id: The field ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/documents/{document_id}/fields/{field_id}")

    async def delete_field_async(self, document_id: str, field_id: str) -> dict[str, str]:
        """Async version of delete_field."""
        return await self._http.delete_async(f"/documents/{document_id}/fields/{field_id}")
