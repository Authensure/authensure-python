"""Envelopes resource for the Authensure SDK."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Envelope, EnvelopeStatus, Recipient


class EnvelopesResource:
    """Resource for envelope operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(self, status: EnvelopeStatus | str | None = None) -> list[Envelope]:
        """
        List all envelopes.

        Args:
            status: Optional status filter.

        Returns:
            List of envelopes.
        """
        query = f"?status={status}" if status else ""
        data = self._http.get(f"/envelopes{query}")
        return [Envelope.model_validate(e) for e in data]

    async def list_async(self, status: EnvelopeStatus | str | None = None) -> list[Envelope]:
        """Async version of list."""
        query = f"?status={status}" if status else ""
        data = await self._http.get_async(f"/envelopes{query}")
        return [Envelope.model_validate(e) for e in data]

    def get(self, envelope_id: str) -> Envelope:
        """
        Get an envelope by ID.

        Args:
            envelope_id: The envelope ID.

        Returns:
            The envelope.
        """
        data = self._http.get(f"/envelopes/{envelope_id}")
        return Envelope.model_validate(data)

    async def get_async(self, envelope_id: str) -> Envelope:
        """Async version of get."""
        data = await self._http.get_async(f"/envelopes/{envelope_id}")
        return Envelope.model_validate(data)

    def create(self, name: str, message: str | None = None) -> Envelope:
        """
        Create a new envelope.

        Args:
            name: Envelope name.
            message: Optional message for recipients.

        Returns:
            The created envelope.
        """
        body = {"name": name}
        if message:
            body["message"] = message
        data = self._http.post("/envelopes", body)
        return Envelope.model_validate(data)

    async def create_async(self, name: str, message: str | None = None) -> Envelope:
        """Async version of create."""
        body = {"name": name}
        if message:
            body["message"] = message
        data = await self._http.post_async("/envelopes", body)
        return Envelope.model_validate(data)

    def update(
        self,
        envelope_id: str,
        name: str | None = None,
        message: str | None = None,
    ) -> Envelope:
        """
        Update an envelope.

        Args:
            envelope_id: The envelope ID.
            name: New envelope name.
            message: New message.

        Returns:
            The updated envelope.
        """
        body = {}
        if name is not None:
            body["name"] = name
        if message is not None:
            body["message"] = message
        data = self._http.patch(f"/envelopes/{envelope_id}", body)
        return Envelope.model_validate(data)

    async def update_async(
        self,
        envelope_id: str,
        name: str | None = None,
        message: str | None = None,
    ) -> Envelope:
        """Async version of update."""
        body = {}
        if name is not None:
            body["name"] = name
        if message is not None:
            body["message"] = message
        data = await self._http.patch_async(f"/envelopes/{envelope_id}", body)
        return Envelope.model_validate(data)

    def delete(self, envelope_id: str) -> dict[str, str]:
        """
        Delete an envelope.

        Args:
            envelope_id: The envelope ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/envelopes/{envelope_id}")

    async def delete_async(self, envelope_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/envelopes/{envelope_id}")

    def add_recipient(
        self,
        envelope_id: str,
        email: str,
        name: str,
        role: str = "signer",
    ) -> Recipient:
        """
        Add a recipient to an envelope.

        Args:
            envelope_id: The envelope ID.
            email: Recipient email.
            name: Recipient name.
            role: Recipient role (default: 'signer').

        Returns:
            The created recipient.
        """
        data = self._http.post(f"/envelopes/{envelope_id}/recipients", {
            "email": email,
            "name": name,
            "role": role,
        })
        return Recipient.model_validate(data)

    async def add_recipient_async(
        self,
        envelope_id: str,
        email: str,
        name: str,
        role: str = "signer",
    ) -> Recipient:
        """Async version of add_recipient."""
        data = await self._http.post_async(f"/envelopes/{envelope_id}/recipients", {
            "email": email,
            "name": name,
            "role": role,
        })
        return Recipient.model_validate(data)

    def remove_recipient(self, envelope_id: str, recipient_id: str) -> dict[str, str]:
        """
        Remove a recipient from an envelope.

        Args:
            envelope_id: The envelope ID.
            recipient_id: The recipient ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/envelopes/{envelope_id}/recipients/{recipient_id}")

    async def remove_recipient_async(self, envelope_id: str, recipient_id: str) -> dict[str, str]:
        """Async version of remove_recipient."""
        return await self._http.delete_async(f"/envelopes/{envelope_id}/recipients/{recipient_id}")

    def send(self, envelope_id: str) -> Envelope:
        """
        Send an envelope for signing.

        Args:
            envelope_id: The envelope ID.

        Returns:
            The sent envelope.
        """
        data = self._http.post(f"/envelopes/{envelope_id}/send")
        return Envelope.model_validate(data)

    async def send_async(self, envelope_id: str) -> Envelope:
        """Async version of send."""
        data = await self._http.post_async(f"/envelopes/{envelope_id}/send")
        return Envelope.model_validate(data)

    def void(self, envelope_id: str, reason: str | None = None) -> Envelope:
        """
        Void an envelope.

        Args:
            envelope_id: The envelope ID.
            reason: Optional reason for voiding.

        Returns:
            The voided envelope.
        """
        body = {"reason": reason} if reason else {}
        data = self._http.post(f"/envelopes/{envelope_id}/void", body)
        return Envelope.model_validate(data)

    async def void_async(self, envelope_id: str, reason: str | None = None) -> Envelope:
        """Async version of void."""
        body = {"reason": reason} if reason else {}
        data = await self._http.post_async(f"/envelopes/{envelope_id}/void", body)
        return Envelope.model_validate(data)

    def get_by_signing_token(self, token: str) -> Envelope:
        """
        Get an envelope by signing token.

        Args:
            token: The signing token.

        Returns:
            The envelope.
        """
        data = self._http.get(f"/envelopes/sign/{token}")
        return Envelope.model_validate(data)

    async def get_by_signing_token_async(self, token: str) -> Envelope:
        """Async version of get_by_signing_token."""
        data = await self._http.get_async(f"/envelopes/sign/{token}")
        return Envelope.model_validate(data)
