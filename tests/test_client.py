"""Tests for the main Authensure client."""

import pytest

from authensure import Authensure
from authensure.resources import (
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


class TestAuthensureClient:
    """Tests for the Authensure client initialization."""

    def test_create_with_api_key(self):
        """Test client creation with API key."""
        client = Authensure(api_key="test_key")
        assert client._http.api_key == "test_key"
        assert client._http.access_token is None

    def test_create_with_access_token(self):
        """Test client creation with access token."""
        client = Authensure(access_token="test_token")
        assert client._http.access_token == "test_token"
        assert client._http.api_key is None

    def test_create_without_credentials_raises_error(self):
        """Test that creating client without credentials raises ValueError."""
        with pytest.raises(ValueError, match="Either api_key or access_token must be provided"):
            Authensure()

    def test_create_with_api_key_class_method(self):
        """Test client creation using create_with_api_key class method."""
        client = Authensure.create_with_api_key("test_key")
        assert client._http.api_key == "test_key"

    def test_create_with_token_class_method(self):
        """Test client creation using create_with_token class method."""
        client = Authensure.create_with_token("test_token")
        assert client._http.access_token == "test_token"

    def test_custom_base_url(self):
        """Test client with custom base URL."""
        client = Authensure(api_key="test_key", base_url="https://custom.api.com")
        assert client._http.base_url == "https://custom.api.com"

    def test_custom_timeout(self):
        """Test client with custom timeout."""
        client = Authensure(api_key="test_key", timeout=60.0)
        assert client._http.timeout == 60.0

    def test_custom_retry_settings(self):
        """Test client with custom retry settings."""
        client = Authensure(api_key="test_key", retry_attempts=5, retry_delay=2.0)
        assert client._http.retry_attempts == 5
        assert client._http.retry_delay == 2.0

    def test_debug_mode(self):
        """Test client with debug mode enabled."""
        client = Authensure(api_key="test_key", debug=True)
        assert client._http.debug is True

    def test_resources_initialized(self):
        """Test that all resources are properly initialized."""
        client = Authensure(api_key="test_key")
        
        assert isinstance(client.auth, AuthResource)
        assert isinstance(client.envelopes, EnvelopesResource)
        assert isinstance(client.documents, DocumentsResource)
        assert isinstance(client.templates, TemplatesResource)
        assert isinstance(client.contacts, ContactsResource)
        assert isinstance(client.users, UsersResource)
        assert isinstance(client.organizations, OrganizationsResource)
        assert isinstance(client.webhooks, WebhooksResource)
        assert isinstance(client.api_keys, ApiKeysResource)
        assert isinstance(client.teams, TeamsResource)
        assert isinstance(client.signatures, SignaturesResource)

    def test_set_access_token(self):
        """Test setting access token after initialization."""
        client = Authensure(api_key="test_key")
        client.set_access_token("new_token")
        assert client._http.access_token == "new_token"

    def test_clear_access_token(self):
        """Test clearing access token."""
        client = Authensure(access_token="test_token")
        client.clear_access_token()
        assert client._http.access_token is None

    def test_context_manager(self):
        """Test using client as context manager."""
        with Authensure(api_key="test_key") as client:
            assert isinstance(client, Authensure)

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test using client as async context manager."""
        async with Authensure(api_key="test_key") as client:
            assert isinstance(client, Authensure)
