"""API Keys resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import ApiKey, ApiKeyStats, ApiKeyWithSecret


class ApiKeysResource:
    """Resource for API key operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(self) -> list[ApiKey]:
        """
        List all API keys.

        Returns:
            List of API keys.
        """
        data = self._http.get("/api-keys")
        return [ApiKey.model_validate(k) for k in data]

    async def list_async(self) -> list[ApiKey]:
        """Async version of list."""
        data = await self._http.get_async("/api-keys")
        return [ApiKey.model_validate(k) for k in data]

    def get(self, key_id: str) -> ApiKey:
        """
        Get an API key by ID.

        Args:
            key_id: The API key ID.

        Returns:
            The API key.
        """
        data = self._http.get(f"/api-keys/{key_id}")
        return ApiKey.model_validate(data)

    async def get_async(self, key_id: str) -> ApiKey:
        """Async version of get."""
        data = await self._http.get_async(f"/api-keys/{key_id}")
        return ApiKey.model_validate(data)

    def create(
        self,
        name: str,
        permissions: list[str],
        rate_limit: int | None = None,
        expires_at: str | None = None,
    ) -> ApiKeyWithSecret:
        """
        Create a new API key.

        Args:
            name: Key name.
            permissions: List of permissions.
            rate_limit: Optional rate limit.
            expires_at: Optional expiration date (ISO 8601).

        Returns:
            The created API key with secret.
        """
        body: dict[str, Any] = {"name": name, "permissions": permissions}
        if rate_limit is not None:
            body["rateLimit"] = rate_limit
        if expires_at is not None:
            body["expiresAt"] = expires_at
        data = self._http.post("/api-keys", body)
        return ApiKeyWithSecret.model_validate(data)

    async def create_async(
        self,
        name: str,
        permissions: list[str],
        rate_limit: int | None = None,
        expires_at: str | None = None,
    ) -> ApiKeyWithSecret:
        """Async version of create."""
        body: dict[str, Any] = {"name": name, "permissions": permissions}
        if rate_limit is not None:
            body["rateLimit"] = rate_limit
        if expires_at is not None:
            body["expiresAt"] = expires_at
        data = await self._http.post_async("/api-keys", body)
        return ApiKeyWithSecret.model_validate(data)

    def delete(self, key_id: str) -> dict[str, str]:
        """
        Delete an API key.

        Args:
            key_id: The API key ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/api-keys/{key_id}")

    async def delete_async(self, key_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/api-keys/{key_id}")

    def regenerate(self, key_id: str) -> ApiKeyWithSecret:
        """
        Regenerate an API key.

        Args:
            key_id: The API key ID.

        Returns:
            The regenerated API key with new secret.
        """
        data = self._http.post(f"/api-keys/{key_id}/regenerate")
        return ApiKeyWithSecret.model_validate(data)

    async def regenerate_async(self, key_id: str) -> ApiKeyWithSecret:
        """Async version of regenerate."""
        data = await self._http.post_async(f"/api-keys/{key_id}/regenerate")
        return ApiKeyWithSecret.model_validate(data)

    def get_stats(self) -> ApiKeyStats:
        """
        Get API key statistics.

        Returns:
            API key statistics.
        """
        data = self._http.get("/api-keys/stats")
        return ApiKeyStats.model_validate(data)

    async def get_stats_async(self) -> ApiKeyStats:
        """Async version of get_stats."""
        data = await self._http.get_async("/api-keys/stats")
        return ApiKeyStats.model_validate(data)
