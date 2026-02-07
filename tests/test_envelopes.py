"""Tests for the Envelopes resource."""

import pytest
import respx
from httpx import Response

from authensure import Authensure, Envelope, EnvelopeStatus


class TestEnvelopesResource:
    """Tests for envelope operations."""

    def test_list_envelopes(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test listing envelopes."""
        mock_api.get("/envelopes").mock(return_value=Response(200, json=[sample_envelope]))
        
        envelopes = client.envelopes.list()
        
        assert len(envelopes) == 1
        assert isinstance(envelopes[0], Envelope)
        assert envelopes[0].id == "env_123456"
        assert envelopes[0].name == "Test Envelope"

    def test_list_envelopes_with_status_filter(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test listing envelopes with status filter."""
        mock_api.get("/envelopes?status=DRAFT").mock(return_value=Response(200, json=[sample_envelope]))
        
        envelopes = client.envelopes.list(status="DRAFT")
        
        assert len(envelopes) == 1
        assert envelopes[0].status == EnvelopeStatus.DRAFT

    def test_get_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test getting a single envelope."""
        mock_api.get("/envelopes/env_123456").mock(return_value=Response(200, json=sample_envelope))
        
        envelope = client.envelopes.get("env_123456")
        
        assert isinstance(envelope, Envelope)
        assert envelope.id == "env_123456"
        assert envelope.name == "Test Envelope"

    def test_create_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test creating an envelope."""
        mock_api.post("/envelopes").mock(return_value=Response(201, json=sample_envelope))
        
        envelope = client.envelopes.create(name="Test Envelope", message="Please sign")
        
        assert isinstance(envelope, Envelope)
        assert envelope.name == "Test Envelope"

    def test_update_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test updating an envelope."""
        updated = {**sample_envelope, "name": "Updated Envelope"}
        mock_api.patch("/envelopes/env_123456").mock(return_value=Response(200, json=updated))
        
        envelope = client.envelopes.update("env_123456", name="Updated Envelope")
        
        assert envelope.name == "Updated Envelope"

    def test_delete_envelope(self, client: Authensure, mock_api):
        """Test deleting an envelope."""
        mock_api.delete("/envelopes/env_123456").mock(
            return_value=Response(200, json={"message": "Envelope deleted"})
        )
        
        result = client.envelopes.delete("env_123456")
        
        assert result["message"] == "Envelope deleted"

    def test_add_recipient(self, client: Authensure, mock_api):
        """Test adding a recipient to an envelope."""
        recipient_data = {
            "id": "rec_123456",
            "email": "signer@example.com",
            "name": "John Doe",
            "role": "signer",
            "orderIndex": 1,
            "status": "PENDING",
            "signedAt": None,
            "viewedAt": None,
            "signingToken": None,
            "envelopeId": "env_123456",
        }
        mock_api.post("/envelopes/env_123456/recipients").mock(
            return_value=Response(201, json=recipient_data)
        )
        
        recipient = client.envelopes.add_recipient(
            "env_123456",
            email="signer@example.com",
            name="John Doe",
        )
        
        assert recipient.id == "rec_123456"
        assert recipient.email == "signer@example.com"

    def test_remove_recipient(self, client: Authensure, mock_api):
        """Test removing a recipient from an envelope."""
        mock_api.delete("/envelopes/env_123456/recipients/rec_123456").mock(
            return_value=Response(200, json={"message": "Recipient removed"})
        )
        
        result = client.envelopes.remove_recipient("env_123456", "rec_123456")
        
        assert result["message"] == "Recipient removed"

    def test_send_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test sending an envelope."""
        sent_envelope = {**sample_envelope, "status": "SENT", "sentAt": "2024-01-01T12:00:00Z"}
        mock_api.post("/envelopes/env_123456/send").mock(
            return_value=Response(200, json=sent_envelope)
        )
        
        envelope = client.envelopes.send("env_123456")
        
        assert envelope.status == EnvelopeStatus.SENT
        assert envelope.sent_at is not None

    def test_void_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test voiding an envelope."""
        voided_envelope = {
            **sample_envelope,
            "status": "VOIDED",
            "voidedAt": "2024-01-01T12:00:00Z",
            "voidReason": "Test reason",
        }
        mock_api.post("/envelopes/env_123456/void").mock(
            return_value=Response(200, json=voided_envelope)
        )
        
        envelope = client.envelopes.void("env_123456", reason="Test reason")
        
        assert envelope.status == EnvelopeStatus.VOIDED
        assert envelope.void_reason == "Test reason"

    def test_get_by_signing_token(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test getting an envelope by signing token."""
        mock_api.get("/envelopes/sign/token_12345").mock(
            return_value=Response(200, json=sample_envelope)
        )
        
        envelope = client.envelopes.get_by_signing_token("token_12345")
        
        assert isinstance(envelope, Envelope)
        assert envelope.id == "env_123456"


class TestEnvelopesResourceAsync:
    """Tests for async envelope operations."""

    @pytest.mark.asyncio
    async def test_list_envelopes_async(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test async listing envelopes."""
        mock_api.get("/envelopes").mock(return_value=Response(200, json=[sample_envelope]))
        
        envelopes = await client.envelopes.list_async()
        
        assert len(envelopes) == 1
        assert envelopes[0].id == "env_123456"

    @pytest.mark.asyncio
    async def test_create_envelope_async(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test async creating an envelope."""
        mock_api.post("/envelopes").mock(return_value=Response(201, json=sample_envelope))
        
        envelope = await client.envelopes.create_async(name="Test Envelope")
        
        assert envelope.name == "Test Envelope"
