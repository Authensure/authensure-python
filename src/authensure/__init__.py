"""
Authensure SDK for Python

Official Python SDK for Authensure - the electronic signature and document authentication platform.

Example usage:
    >>> from authensure import Authensure
    >>> client = Authensure(api_key="your_api_key")
    >>> envelope = client.envelopes.create(name="Contract Agreement")
"""

from .client import Authensure
from .errors import (
    AuthensureError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from .http_client import HttpClient
from .types import (
    ApiKey,
    ApiKeyStats,
    ApiKeyWithSecret,
    AuthensureConfig,
    Contact,
    ContactSource,
    ContactStats,
    Document,
    DocumentField,
    Envelope,
    EnvelopeStatus,
    LoginResponse,
    Organization,
    OrganizationSettings,
    Pagination,
    PaginatedResponse,
    PresenceStatus,
    Recipient,
    RecipientStatus,
    SavedSignature,
    Session,
    TeamInvitation,
    TeamMember,
    Template,
    TemplateDocument,
    TemplateField,
    TemplateRole,
    User,
    UserProfile,
    UserRole,
    Webhook,
    WebhookDelivery,
    WebhookPayload,
)

__version__ = "1.0.1"
__all__ = [
    # Main client
    "Authensure",
    "HttpClient",
    # Configuration
    "AuthensureConfig",
    # Errors
    "AuthensureError",
    "AuthenticationError",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    "TimeoutError",
    "ValidationError",
    # Types - Enums
    "ContactSource",
    "EnvelopeStatus",
    "PresenceStatus",
    "RecipientStatus",
    "UserRole",
    # Types - Models
    "ApiKey",
    "ApiKeyStats",
    "ApiKeyWithSecret",
    "Contact",
    "ContactStats",
    "Document",
    "DocumentField",
    "Envelope",
    "LoginResponse",
    "Organization",
    "OrganizationSettings",
    "Pagination",
    "PaginatedResponse",
    "Recipient",
    "SavedSignature",
    "Session",
    "TeamInvitation",
    "TeamMember",
    "Template",
    "TemplateDocument",
    "TemplateField",
    "TemplateRole",
    "User",
    "UserProfile",
    "Webhook",
    "WebhookDelivery",
    "WebhookPayload",
]
