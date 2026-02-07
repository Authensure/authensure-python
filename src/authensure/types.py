"""Type definitions for the Authensure SDK."""

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class UserRole(str, Enum):
    """User role types."""
    USER = "USER"
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    SUPERUSER = "SUPERUSER"


class EnvelopeStatus(str, Enum):
    """Envelope status types."""
    DRAFT = "DRAFT"
    SENT = "SENT"
    COMPLETED = "COMPLETED"
    VOIDED = "VOIDED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"


class RecipientStatus(str, Enum):
    """Recipient status types."""
    PENDING = "PENDING"
    SENT = "SENT"
    VIEWED = "VIEWED"
    SIGNED = "SIGNED"
    DECLINED = "DECLINED"


class ContactSource(str, Enum):
    """Contact source types."""
    ENVELOPE = "ENVELOPE"
    PUBLIC_FORM = "PUBLIC_FORM"
    MANUAL = "MANUAL"


class PresenceStatus(str, Enum):
    """User presence status types."""
    ONLINE = "ONLINE"
    AWAY = "AWAY"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


WebhookEvent = Literal[
    "envelope.created",
    "envelope.sent",
    "envelope.viewed",
    "envelope.signed",
    "envelope.completed",
    "envelope.declined",
    "envelope.voided",
    "recipient.signed",
    "recipient.declined",
    "document.uploaded",
]


class AuthensureConfig(BaseModel):
    """Configuration for the Authensure client."""
    model_config = ConfigDict(extra="forbid")

    api_key: str | None = None
    access_token: str | None = None
    base_url: str = "https://api.authensure.app/api"
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    debug: bool = False


class Pagination(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    total_pages: int = Field(alias="totalPages")


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    pagination: Pagination


class User(BaseModel):
    """User model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str
    name: str
    role: UserRole
    avatar_url: str | None = Field(default=None, alias="avatarUrl")
    phone: str | None = None
    phone_verified: bool = Field(default=False, alias="phoneVerified")
    email_verified: bool = Field(default=False, alias="emailVerified")
    company: str | None = None
    job_title: str | None = Field(default=None, alias="jobTitle")
    bio: str | None = None
    location: str | None = None
    website: str | None = None
    organization_id: str | None = Field(default=None, alias="organizationId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UserProfile(User):
    """User profile with presence information."""
    presence_status: PresenceStatus = Field(alias="presenceStatus")
    last_active_at: datetime | None = Field(default=None, alias="lastActiveAt")


class Organization(BaseModel):
    """Organization model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    slug: str
    logo_url: str | None = Field(default=None, alias="logoUrl")
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class OrganizationSettings(BaseModel):
    """Organization settings model."""
    model_config = ConfigDict(populate_by_name=True)

    default_signature_type: str | None = Field(default=None, alias="defaultSignatureType")
    allowed_signature_types: list[str] | None = Field(default=None, alias="allowedSignatureTypes")
    require_mfa: bool | None = Field(default=None, alias="requireMfa")
    session_timeout: int | None = Field(default=None, alias="sessionTimeout")
    branding_enabled: bool | None = Field(default=None, alias="brandingEnabled")
    primary_color: str | None = Field(default=None, alias="primaryColor")
    logo_url: str | None = Field(default=None, alias="logoUrl")


class DocumentField(BaseModel):
    """Document field model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str
    label: str | None = None
    placeholder: str | None = None
    required: bool
    x: float
    y: float
    width: float
    height: float
    page: int
    recipient_id: str | None = Field(default=None, alias="recipientId")
    value: str | None = None


class Document(BaseModel):
    """Document model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    file_url: str = Field(alias="fileUrl")
    file_cid: str | None = Field(default=None, alias="fileCid")
    mime_type: str = Field(alias="mimeType")
    size: int
    page_count: int | None = Field(default=None, alias="pageCount")
    envelope_id: str = Field(alias="envelopeId")
    fields: list[DocumentField] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class Recipient(BaseModel):
    """Recipient model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str
    name: str
    role: str
    order_index: int = Field(alias="orderIndex")
    status: RecipientStatus
    signed_at: datetime | None = Field(default=None, alias="signedAt")
    viewed_at: datetime | None = Field(default=None, alias="viewedAt")
    signing_token: str | None = Field(default=None, alias="signingToken")
    envelope_id: str = Field(alias="envelopeId")


class Envelope(BaseModel):
    """Envelope model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    status: EnvelopeStatus
    message: str | None = None
    organization_id: str = Field(alias="organizationId")
    created_by_id: str = Field(alias="createdById")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    sent_at: datetime | None = Field(default=None, alias="sentAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    voided_at: datetime | None = Field(default=None, alias="voidedAt")
    void_reason: str | None = Field(default=None, alias="voidReason")
    documents: list[Document] = []
    recipients: list[Recipient] = []


class TemplateField(BaseModel):
    """Template field model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str
    label: str | None = None
    placeholder: str | None = None
    required: bool
    x: float
    y: float
    width: float
    height: float
    page: int
    role_id: str | None = Field(default=None, alias="roleId")


class TemplateDocument(BaseModel):
    """Template document model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    file_url: str = Field(alias="fileUrl")
    template_id: str = Field(alias="templateId")
    fields: list[TemplateField] = []


class TemplateRole(BaseModel):
    """Template role model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    order_index: int = Field(alias="orderIndex")
    template_id: str = Field(alias="templateId")


class Template(BaseModel):
    """Template model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    description: str | None = None
    organization_id: str = Field(alias="organizationId")
    created_by_id: str = Field(alias="createdById")
    is_public: bool = Field(alias="isPublic")
    usage_count: int = Field(alias="usageCount")
    documents: list[TemplateDocument] = []
    roles: list[TemplateRole] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class Contact(BaseModel):
    """Contact model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str
    name: str
    company: str | None = None
    phone: str | None = None
    notes: str | None = None
    source: ContactSource
    organization_id: str = Field(alias="organizationId")
    added_by_id: str | None = Field(default=None, alias="addedById")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ContactStats(BaseModel):
    """Contact statistics model."""
    model_config = ConfigDict(populate_by_name=True)

    total: int
    by_source: dict[str, int] = Field(alias="bySource")
    added_last_24h: int = Field(alias="addedLast24h")
    change_24h: int = Field(alias="change24h")
    change_percent: float = Field(alias="changePercent")


class ApiKey(BaseModel):
    """API key model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    key_prefix: str = Field(alias="keyPrefix")
    permissions: list[str]
    rate_limit: int | None = Field(default=None, alias="rateLimit")
    last_used_at: datetime | None = Field(default=None, alias="lastUsedAt")
    expires_at: datetime | None = Field(default=None, alias="expiresAt")
    created_at: datetime = Field(alias="createdAt")


class ApiKeyWithSecret(ApiKey):
    """API key model with the secret key included."""
    key: str


class ApiKeyStats(BaseModel):
    """API key statistics model."""
    model_config = ConfigDict(populate_by_name=True)

    total_keys: int = Field(alias="totalKeys")
    active_keys: int = Field(alias="activeKeys")
    total_requests: int = Field(alias="totalRequests")
    requests_today: int = Field(alias="requestsToday")


class Webhook(BaseModel):
    """Webhook model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    url: str
    events: list[str]
    is_active: bool = Field(alias="isActive")
    secret: str
    organization_id: str = Field(alias="organizationId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class WebhookDelivery(BaseModel):
    """Webhook delivery model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    webhook_id: str = Field(alias="webhookId")
    event: str
    payload: dict[str, Any]
    status_code: int | None = Field(default=None, alias="statusCode")
    response: str | None = None
    success: bool
    attempt_count: int = Field(alias="attemptCount")
    created_at: datetime = Field(alias="createdAt")


class TeamMember(BaseModel):
    """Team member model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    user: User
    role: UserRole
    status: Literal["ACTIVE", "SUSPENDED", "PENDING"]
    joined_at: datetime = Field(alias="joinedAt")


class TeamInvitation(BaseModel):
    """Team invitation model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str
    role: UserRole
    token: str
    expires_at: datetime = Field(alias="expiresAt")
    invited_by_id: str = Field(alias="invitedById")
    organization_id: str = Field(alias="organizationId")
    created_at: datetime = Field(alias="createdAt")


class SavedSignature(BaseModel):
    """Saved signature model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    image_data: str = Field(alias="imageData")
    is_default: bool = Field(alias="isDefault")
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")


class Session(BaseModel):
    """Session model."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    ip_address: str = Field(alias="ipAddress")
    user_agent: str = Field(alias="userAgent")
    browser: str | None = None
    os: str | None = None
    device: str | None = None
    is_current: bool = Field(alias="isCurrent")
    created_at: datetime = Field(alias="createdAt")
    last_active_at: datetime = Field(alias="lastActiveAt")


class LoginResponse(BaseModel):
    """Login response model."""
    model_config = ConfigDict(populate_by_name=True)

    access_token: str = Field(alias="accessToken")
    refresh_token: str | None = Field(default=None, alias="refreshToken")
    user: User
    requires_mfa: bool | None = Field(default=None, alias="requiresMfa")
    mfa_token: str | None = Field(default=None, alias="mfaToken")
    available_mfa_methods: list[str] | None = Field(default=None, alias="availableMfaMethods")


class WebhookPayload(BaseModel):
    """Webhook payload model."""
    event: str
    data: dict[str, Any]
    timestamp: str
