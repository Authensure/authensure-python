"""Signatures resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import SavedSignature


class SignaturesResource:
    """Resource for signature operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(self) -> list[SavedSignature]:
        """
        List all saved signatures.

        Returns:
            List of saved signatures.
        """
        data = self._http.get("/signatures")
        return [SavedSignature.model_validate(s) for s in data]

    async def list_async(self) -> list[SavedSignature]:
        """Async version of list."""
        data = await self._http.get_async("/signatures")
        return [SavedSignature.model_validate(s) for s in data]

    def get(self, signature_id: str) -> SavedSignature:
        """
        Get a saved signature by ID.

        Args:
            signature_id: The signature ID.

        Returns:
            The saved signature.
        """
        data = self._http.get(f"/signatures/{signature_id}")
        return SavedSignature.model_validate(data)

    async def get_async(self, signature_id: str) -> SavedSignature:
        """Async version of get."""
        data = await self._http.get_async(f"/signatures/{signature_id}")
        return SavedSignature.model_validate(data)

    def create(
        self,
        name: str,
        image_data: str,
        is_default: bool = False,
    ) -> SavedSignature:
        """
        Create a new saved signature.

        Args:
            name: Signature name.
            image_data: Base64 encoded signature image.
            is_default: Whether this is the default signature.

        Returns:
            The created signature.
        """
        data = self._http.post("/signatures", {
            "name": name,
            "imageData": image_data,
            "isDefault": is_default,
        })
        return SavedSignature.model_validate(data)

    async def create_async(
        self,
        name: str,
        image_data: str,
        is_default: bool = False,
    ) -> SavedSignature:
        """Async version of create."""
        data = await self._http.post_async("/signatures", {
            "name": name,
            "imageData": image_data,
            "isDefault": is_default,
        })
        return SavedSignature.model_validate(data)

    def update(
        self,
        signature_id: str,
        name: str | None = None,
        image_data: str | None = None,
        is_default: bool | None = None,
    ) -> SavedSignature:
        """
        Update a saved signature.

        Args:
            signature_id: The signature ID.
            name: New name.
            image_data: New image data.
            is_default: New default status.

        Returns:
            The updated signature.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if image_data is not None:
            body["imageData"] = image_data
        if is_default is not None:
            body["isDefault"] = is_default
        data = self._http.patch(f"/signatures/{signature_id}", body)
        return SavedSignature.model_validate(data)

    async def update_async(
        self,
        signature_id: str,
        name: str | None = None,
        image_data: str | None = None,
        is_default: bool | None = None,
    ) -> SavedSignature:
        """Async version of update."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if image_data is not None:
            body["imageData"] = image_data
        if is_default is not None:
            body["isDefault"] = is_default
        data = await self._http.patch_async(f"/signatures/{signature_id}", body)
        return SavedSignature.model_validate(data)

    def delete(self, signature_id: str) -> dict[str, str]:
        """
        Delete a saved signature.

        Args:
            signature_id: The signature ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/signatures/{signature_id}")

    async def delete_async(self, signature_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/signatures/{signature_id}")

    def set_default(self, signature_id: str) -> SavedSignature:
        """
        Set a signature as the default.

        Args:
            signature_id: The signature ID.

        Returns:
            The updated signature.
        """
        data = self._http.post(f"/signatures/{signature_id}/default")
        return SavedSignature.model_validate(data)

    async def set_default_async(self, signature_id: str) -> SavedSignature:
        """Async version of set_default."""
        data = await self._http.post_async(f"/signatures/{signature_id}/default")
        return SavedSignature.model_validate(data)
