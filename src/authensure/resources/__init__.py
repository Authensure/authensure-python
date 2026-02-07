"""Resource modules for the Authensure SDK."""

from .api_keys import ApiKeysResource
from .auth import AuthResource
from .contacts import ContactsResource
from .documents import DocumentsResource
from .envelopes import EnvelopesResource
from .organizations import OrganizationsResource
from .signatures import SignaturesResource
from .teams import TeamsResource
from .templates import TemplatesResource
from .users import UsersResource
from .webhooks import WebhooksResource

__all__ = [
    "ApiKeysResource",
    "AuthResource",
    "ContactsResource",
    "DocumentsResource",
    "EnvelopesResource",
    "OrganizationsResource",
    "SignaturesResource",
    "TeamsResource",
    "TemplatesResource",
    "UsersResource",
    "WebhooksResource",
]
