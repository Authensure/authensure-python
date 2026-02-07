# Authensure Python SDK Examples

This directory contains example scripts demonstrating how to use the Authensure Python SDK.

## Prerequisites

1. Install the SDK:
   ```bash
   pip install authensure
   ```

2. Set your API key as an environment variable:
   ```bash
   export AUTHENSURE_API_KEY="your_api_key_here"
   ```

## Examples

### Basic Usage (`basic_usage.py`)

Demonstrates basic SDK operations including:
- Client initialization
- Creating an envelope
- Adding recipients
- Sending for signature

```bash
python basic_usage.py
```

### Create Envelope Workflow (`create_envelope_workflow.py`)

Complete workflow for creating and sending an envelope:
- Creating an envelope with documents
- Adding multiple recipients
- Setting up signature fields
- Sending for signatures
- Checking envelope status

```bash
python create_envelope_workflow.py
```

### Webhook Server (`webhook_server.py`)

Flask-based webhook server demonstrating:
- Receiving webhook events
- Verifying webhook signatures
- Processing different event types

```bash
pip install flask
python webhook_server.py
```

### Async Usage (`async_usage.py`)

Demonstrates async/await usage for high-performance applications:
- Async client operations
- Parallel API calls
- Context manager usage

```bash
python async_usage.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AUTHENSURE_API_KEY` | Your Authensure API key |
| `AUTHENSURE_BASE_URL` | API base URL (optional, defaults to production) |

## Getting Help

- [SDK Documentation](https://authensure.app/docs/sdk/python)
- [API Reference](https://authensure.app/dashboard/developers)
- [Support](mailto:support@authensure.app)
