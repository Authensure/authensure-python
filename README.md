# Authensure Python SDK

[![PyPI version](https://badge.fury.io/py/authensure.svg)](https://pypi.org/project/authensure/)
[![Python Versions](https://img.shields.io/pypi/pyversions/authensure.svg)](https://pypi.org/project/authensure/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for [Authensure](https://authensure.app) - the electronic signature and document authentication platform.

## Features

- 🔐 **Full API Coverage** - Access all Authensure API endpoints
- 🐍 **Type Hints** - Complete type annotations with Pydantic models
- ⚡ **Async Support** - Native async/await for high-performance applications
- 🔄 **Automatic Retries** - Built-in exponential backoff for transient errors
- ⏱️ **Rate Limit Handling** - Automatic rate limit detection and backoff
- 🔗 **Webhook Verification** - Easy webhook signature verification
- 📁 **File Uploads** - Simplified document upload handling
- 🐛 **Debug Mode** - Detailed logging for development

## Installation

```bash
pip install authensure
```

## Quick Start

```python
from authensure import Authensure

# Initialize with API key
client = Authensure(api_key="your_api_key_here")

# Or with access token
client = Authensure.create_with_token("your_access_token")

# Create an envelope
envelope = client.envelopes.create(
    name="Contract Agreement",
    message="Please sign this document",
)

# Add a recipient
client.envelopes.add_recipient(
    envelope_id=envelope.id,
    email="signer@example.com",
    name="John Doe",
    role="signer",
)

# Send for signing
client.envelopes.send(envelope.id)
```

## Async Usage

```python
import asyncio
from authensure import Authensure

async def main():
    async with Authensure(api_key="your_api_key") as client:
        # Create envelope asynchronously
        envelope = await client.envelopes.create_async(
            name="Contract Agreement",
        )
        
        # Add recipients in parallel
        await asyncio.gather(
            client.envelopes.add_recipient_async(envelope.id, "alice@example.com", "Alice"),
            client.envelopes.add_recipient_async(envelope.id, "bob@example.com", "Bob"),
        )

asyncio.run(main())
```

## Authentication

### Using API Key

```python
client = Authensure(api_key="your_api_key")
```

### Using Email/Password Login

```python
client = Authensure(access_token="temporary")

response = client.auth.login("user@example.com", "password")
# Token is automatically set for subsequent requests
```

## Configuration Options

```python
client = Authensure(
    api_key="your_api_key",              # API key for authentication
    access_token="your_token",           # JWT access token
    base_url="https://api.authensure.app/api",  # API base URL
    timeout=30.0,                        # Request timeout in seconds
    retry_attempts=3,                    # Number of retry attempts
    retry_delay=1.0,                     # Initial retry delay in seconds
    debug=False,                         # Enable debug logging
)
```

## API Reference

### Envelopes

```python
# List envelopes
envelopes = client.envelopes.list(status="DRAFT")

# Get an envelope
envelope = client.envelopes.get("envelope_id")

# Create an envelope
envelope = client.envelopes.create(name="My Contract", message="Please sign")

# Add a recipient
recipient = client.envelopes.add_recipient(
    envelope_id="envelope_id",
    email="signer@example.com",
    name="John Doe",
    role="signer",
)

# Send for signing
envelope = client.envelopes.send("envelope_id")

# Void an envelope
envelope = client.envelopes.void("envelope_id", reason="Contract cancelled")
```

### Documents

```python
# Upload a document
with open("contract.pdf", "rb") as f:
    document = client.documents.upload(
        envelope_id="envelope_id",
        file=f.read(),
        filename="contract.pdf",
    )

# Get signed document URL
result = client.documents.get_signed_url("document_id")
print(result["url"])

# Download a document
content = client.documents.download("document_id")
```

### Templates

```python
# List templates
templates = client.templates.list()

# Create from template
envelope = client.templates.use(
    template_id="template_id",
    name="New Contract",
    recipients=[
        {"roleId": "role_1", "email": "signer@example.com", "name": "John Doe"}
    ],
)
```

### Contacts

```python
# List contacts
contacts = client.contacts.list(search="acme", limit=20)

# Create a contact
contact = client.contacts.create(
    email="contact@example.com",
    name="Jane Smith",
    company="Acme Inc",
)
```

### Webhooks

```python
# Create a webhook
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/authensure",
    events=["envelope.signed", "envelope.completed"],
)

# Verify webhook signature
from authensure.resources.webhooks import WebhooksResource

is_valid = WebhooksResource.verify_signature(
    payload=request_body,
    signature=request.headers["X-Authensure-Signature"],
    secret="your_webhook_secret",
)

# Construct verified event
event = WebhooksResource.construct_event(
    payload=request_body,
    signature=signature,
    secret="your_webhook_secret",
)
print(f"Event type: {event.event}")
print(f"Data: {event.data}")
```

## Error Handling

```python
from authensure import (
    Authensure,
    AuthensureError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
)

try:
    envelope = client.envelopes.get("invalid_id")
except NotFoundError:
    print("Envelope not found")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after} seconds")
except ValidationError as e:
    print(f"Validation errors: {e.validation_errors}")
except AuthensureError as e:
    print(f"API error: {e.message} (code: {e.code})")
```

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=src/authensure --cov-report=html
```

### Type checking

```bash
mypy src/authensure
```

### Linting

```bash
ruff check src/authensure
```

## Resources

- [Documentation](https://authensure.app/docs/sdk/python)
- [API Reference](https://authensure.app/dashboard/developers)
- [GitHub Repository](https://github.com/Authensure/authensure-python)
- [PyPI Package](https://pypi.org/project/authensure/)
- [Report Issues](https://github.com/Authensure/authensure-python/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
