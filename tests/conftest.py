"""Pytest configuration and fixtures."""

import pytest
import respx
from httpx import Response

from authensure import Authensure


@pytest.fixture
def api_key() -> str:
    """Return a test API key."""
    return "test_api_key_12345"


@pytest.fixture
def base_url() -> str:
    """Return the test API base URL."""
    return "https://api.authensure.app/api"


@pytest.fixture
def client(api_key: str, base_url: str) -> Authensure:
    """Create a test client."""
    return Authensure(api_key=api_key, base_url=base_url)


@pytest.fixture
def mock_api(base_url: str):
    """Create a mock API context."""
    with respx.mock(base_url=base_url, assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def sample_user() -> dict:
    """Return sample user data."""
    return {
        "id": "usr_123456",
        "email": "test@example.com",
        "name": "Test User",
        "role": "USER",
        "avatarUrl": None,
        "phone": None,
        "phoneVerified": False,
        "emailVerified": True,
        "company": "Test Corp",
        "jobTitle": "Developer",
        "bio": None,
        "location": None,
        "website": None,
        "organizationId": "org_123456",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_envelope() -> dict:
    """Return sample envelope data."""
    return {
        "id": "env_123456",
        "name": "Test Envelope",
        "status": "DRAFT",
        "message": "Please sign this document",
        "organizationId": "org_123456",
        "createdById": "usr_123456",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
        "sentAt": None,
        "completedAt": None,
        "voidedAt": None,
        "voidReason": None,
        "documents": [],
        "recipients": [],
    }


@pytest.fixture
def sample_template() -> dict:
    """Return sample template data."""
    return {
        "id": "tpl_123456",
        "name": "Test Template",
        "description": "A test template",
        "organizationId": "org_123456",
        "createdById": "usr_123456",
        "isPublic": False,
        "usageCount": 0,
        "documents": [],
        "roles": [],
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_contact() -> dict:
    """Return sample contact data."""
    return {
        "id": "cnt_123456",
        "email": "contact@example.com",
        "name": "Test Contact",
        "company": "Contact Corp",
        "phone": "+1234567890",
        "notes": "Test notes",
        "source": "MANUAL",
        "organizationId": "org_123456",
        "addedById": "usr_123456",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_webhook() -> dict:
    """Return sample webhook data."""
    return {
        "id": "whk_123456",
        "url": "https://example.com/webhook",
        "events": ["envelope.signed", "envelope.completed"],
        "isActive": True,
        "secret": "whsec_test_secret",
        "organizationId": "org_123456",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_api_key() -> dict:
    """Return sample API key data."""
    return {
        "id": "key_123456",
        "name": "Test API Key",
        "keyPrefix": "auth_",
        "permissions": ["envelopes:read", "envelopes:write"],
        "rateLimit": 1000,
        "lastUsedAt": None,
        "expiresAt": None,
        "createdAt": "2024-01-01T00:00:00Z",
    }
