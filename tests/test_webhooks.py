"""Tests for the Webhooks resource."""

import hashlib
import hmac
import json

import pytest
import respx
from httpx import Response

from authensure import Authensure, Webhook


class TestWebhooksResource:
    """Tests for webhook operations."""

    def test_list_webhooks(self, client: Authensure, mock_api, sample_webhook: dict):
        """Test listing webhooks."""
        mock_api.get("/webhooks").mock(
            return_value=Response(200, json={"webhooks": [sample_webhook]})
        )
        
        result = client.webhooks.list()
        
        assert len(result["webhooks"]) == 1
        assert isinstance(result["webhooks"][0], Webhook)
        assert result["webhooks"][0].id == "whk_123456"

    def test_get_webhook(self, client: Authensure, mock_api, sample_webhook: dict):
        """Test getting a single webhook."""
        mock_api.get("/webhooks/whk_123456").mock(
            return_value=Response(200, json=sample_webhook)
        )
        
        webhook = client.webhooks.get("whk_123456")
        
        assert isinstance(webhook, Webhook)
        assert webhook.id == "whk_123456"
        assert webhook.url == "https://example.com/webhook"

    def test_create_webhook(self, client: Authensure, mock_api, sample_webhook: dict):
        """Test creating a webhook."""
        mock_api.post("/webhooks").mock(return_value=Response(201, json=sample_webhook))
        
        webhook = client.webhooks.create(
            url="https://example.com/webhook",
            events=["envelope.signed", "envelope.completed"],
        )
        
        assert webhook.url == "https://example.com/webhook"
        assert "envelope.signed" in webhook.events

    def test_update_webhook(self, client: Authensure, mock_api, sample_webhook: dict):
        """Test updating a webhook."""
        updated = {**sample_webhook, "url": "https://new.example.com/webhook"}
        mock_api.patch("/webhooks/whk_123456").mock(return_value=Response(200, json=updated))
        
        webhook = client.webhooks.update("whk_123456", url="https://new.example.com/webhook")
        
        assert webhook.url == "https://new.example.com/webhook"

    def test_delete_webhook(self, client: Authensure, mock_api):
        """Test deleting a webhook."""
        mock_api.delete("/webhooks/whk_123456").mock(
            return_value=Response(200, json={"success": True})
        )
        
        result = client.webhooks.delete("whk_123456")
        
        assert result["success"] is True

    def test_test_webhook(self, client: Authensure, mock_api):
        """Test sending a test webhook."""
        mock_api.post("/webhooks/whk_123456/test").mock(
            return_value=Response(200, json={"success": True, "statusCode": 200})
        )
        
        result = client.webhooks.test("whk_123456")
        
        assert result["success"] is True
        assert result["statusCode"] == 200


class TestWebhookSignatureVerification:
    """Tests for webhook signature verification."""

    def test_verify_valid_signature(self):
        """Test verifying a valid webhook signature."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload = '{"event": "envelope.signed", "data": {}}'
        secret = "whsec_test_secret"
        
        expected_sig = hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        
        signature = f"sha256={expected_sig}"
        
        assert WebhooksResource.verify_signature(payload, signature, secret) is True

    def test_verify_invalid_signature(self):
        """Test verifying an invalid webhook signature."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload = '{"event": "envelope.signed", "data": {}}'
        secret = "whsec_test_secret"
        signature = "sha256=invalid_signature"
        
        assert WebhooksResource.verify_signature(payload, signature, secret) is False

    def test_verify_signature_without_prefix(self):
        """Test verifying a signature without sha256= prefix."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload = '{"event": "envelope.signed", "data": {}}'
        secret = "whsec_test_secret"
        
        expected_sig = hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        
        assert WebhooksResource.verify_signature(payload, expected_sig, secret) is True

    def test_construct_valid_event(self):
        """Test constructing a valid webhook event."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload_dict = {
            "event": "envelope.signed",
            "data": {"envelopeId": "env_123"},
            "timestamp": "2024-01-01T00:00:00Z",
        }
        payload = json.dumps(payload_dict)
        secret = "whsec_test_secret"
        
        signature = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        
        event = WebhooksResource.construct_event(payload, signature, secret)
        
        assert event.event == "envelope.signed"
        assert event.data["envelopeId"] == "env_123"

    def test_construct_event_invalid_signature_raises(self):
        """Test that constructing event with invalid signature raises error."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload = '{"event": "envelope.signed", "data": {}, "timestamp": "2024-01-01T00:00:00Z"}'
        secret = "whsec_test_secret"
        signature = "sha256=invalid"
        
        with pytest.raises(ValueError, match="Invalid webhook signature"):
            WebhooksResource.construct_event(payload, signature, secret)

    def test_verify_bytes_payload(self):
        """Test verifying signature with bytes payload."""
        from authensure.resources.webhooks import WebhooksResource
        
        payload = b'{"event": "envelope.signed", "data": {}}'
        secret = "whsec_test_secret"
        
        expected_sig = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()
        
        signature = f"sha256={expected_sig}"
        
        assert WebhooksResource.verify_signature(payload, signature, secret) is True
