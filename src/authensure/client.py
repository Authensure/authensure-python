"""Main Authensure client."""

from .http_client import HttpClient
from .resources import (
    ApiKeysResource,
    AuthResource,
    ContactsResource,
    DocumentsResource,
    EnvelopesResource,
    OrganizationsResource,
    SignaturesResource,
    TeamsResource,
    TemplatesResource,
    UsersResource,
    WebhooksResource,
)
from .types import AuthensureConfig


class Authensure:
    """
    Main client for the Authensure API.

    Example usage:
        >>> client = Authensure(api_key="your_api_key")
        >>> envelope = client.envelopes.create(name="Contract Agreement")

    Or with access token:
        >>> client = Authensure(access_token="user_access_token")
    """

    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str = "https://api.authensure.app/api",
        timeout: float = 30.0,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        debug: bool = False,
    ) -> None:
        """
        Initialize the Authensure client.

        Args:
            api_key: API key for authentication.
            access_token: JWT access token for authentication.
            base_url: API base URL (default: https://api.authensure.app/api).
            timeout: Request timeout in seconds (default: 30).
            retry_attempts: Number of retry attempts (default: 3).
            retry_delay: Initial retry delay in seconds (default: 1).
            debug: Enable debug logging (default: False).

        Raises:
            ValueError: If neither api_key nor access_token is provided.
        """
        if not api_key and not access_token:
            raise ValueError("Either api_key or access_token must be provided")

        config = AuthensureConfig(
            api_key=api_key,
            access_token=access_token,
            base_url=base_url,
            timeout=timeout,
            retry_attempts=retry_attempts,
            retry_delay=retry_delay,
            debug=debug,
        )

        self._http = HttpClient(config)

        # Initialize resources
        self.auth = AuthResource(self._http)
        self.envelopes = EnvelopesResource(self._http)
        self.documents = DocumentsResource(self._http)
        self.templates = TemplatesResource(self._http)
        self.contacts = ContactsResource(self._http)
        self.users = UsersResource(self._http)
        self.organizations = OrganizationsResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.teams = TeamsResource(self._http)
        self.signatures = SignaturesResource(self._http)

    def set_access_token(self, token: str) -> None:
        """
        Set the access token for authentication.

        Args:
            token: The JWT access token.
        """
        self._http.set_access_token(token)

    def clear_access_token(self) -> None:
        """Clear the access token."""
        self._http.clear_access_token()

    @classmethod
    def create_with_api_key(
        cls,
        api_key: str,
        **kwargs: object,
    ) -> "Authensure":
        """
        Create a client with an API key.

        Args:
            api_key: The API key.
            **kwargs: Additional configuration options.

        Returns:
            Configured Authensure client.
        """
        return cls(api_key=api_key, **kwargs)

    @classmethod
    def create_with_token(
        cls,
        access_token: str,
        **kwargs: object,
    ) -> "Authensure":
        """
        Create a client with an access token.

        Args:
            access_token: The JWT access token.
            **kwargs: Additional configuration options.

        Returns:
            Configured Authensure client.
        """
        return cls(access_token=access_token, **kwargs)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    async def close_async(self) -> None:
        """Close the async HTTP client."""
        await self._http.close_async()

    def __enter__(self) -> "Authensure":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    async def __aenter__(self) -> "Authensure":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close_async()
