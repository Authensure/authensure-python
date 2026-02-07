#!/usr/bin/env python3
"""
Webhook server example using Flask.

This example demonstrates:
- Receiving webhook events from Authensure
- Verifying webhook signatures
- Processing different event types

Requirements:
    pip install flask

Usage:
    export AUTHENSURE_WEBHOOK_SECRET="your_webhook_secret"
    python webhook_server.py
"""

import json
import os
from typing import Any

from flask import Flask, request, jsonify

from authensure.resources.webhooks import WebhooksResource

app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get("AUTHENSURE_WEBHOOK_SECRET", "")


def handle_envelope_created(data: dict[str, Any]) -> None:
    """Handle envelope.created event."""
    envelope_id = data.get("envelopeId")
    envelope_name = data.get("name")
    print(f"📝 Envelope created: {envelope_name} ({envelope_id})")


def handle_envelope_sent(data: dict[str, Any]) -> None:
    """Handle envelope.sent event."""
    envelope_id = data.get("envelopeId")
    recipients = data.get("recipients", [])
    print(f"📤 Envelope sent: {envelope_id}")
    print(f"   Recipients: {len(recipients)}")


def handle_envelope_viewed(data: dict[str, Any]) -> None:
    """Handle envelope.viewed event."""
    envelope_id = data.get("envelopeId")
    recipient_email = data.get("recipientEmail")
    print(f"👁 Envelope viewed: {envelope_id}")
    print(f"   Viewer: {recipient_email}")


def handle_envelope_signed(data: dict[str, Any]) -> None:
    """Handle envelope.signed event."""
    envelope_id = data.get("envelopeId")
    recipient_email = data.get("recipientEmail")
    recipient_name = data.get("recipientName")
    print(f"✍️ Envelope signed: {envelope_id}")
    print(f"   Signer: {recipient_name} ({recipient_email})")


def handle_envelope_completed(data: dict[str, Any]) -> None:
    """Handle envelope.completed event."""
    envelope_id = data.get("envelopeId")
    completed_at = data.get("completedAt")
    print(f"✅ Envelope completed: {envelope_id}")
    print(f"   Completed at: {completed_at}")


def handle_envelope_declined(data: dict[str, Any]) -> None:
    """Handle envelope.declined event."""
    envelope_id = data.get("envelopeId")
    recipient_email = data.get("recipientEmail")
    reason = data.get("declineReason")
    print(f"❌ Envelope declined: {envelope_id}")
    print(f"   By: {recipient_email}")
    print(f"   Reason: {reason}")


def handle_envelope_voided(data: dict[str, Any]) -> None:
    """Handle envelope.voided event."""
    envelope_id = data.get("envelopeId")
    reason = data.get("voidReason")
    print(f"🚫 Envelope voided: {envelope_id}")
    print(f"   Reason: {reason}")


EVENT_HANDLERS = {
    "envelope.created": handle_envelope_created,
    "envelope.sent": handle_envelope_sent,
    "envelope.viewed": handle_envelope_viewed,
    "envelope.signed": handle_envelope_signed,
    "envelope.completed": handle_envelope_completed,
    "envelope.declined": handle_envelope_declined,
    "envelope.voided": handle_envelope_voided,
}


@app.route("/webhooks/authensure", methods=["POST"])
def handle_webhook():
    """Handle incoming webhook from Authensure."""
    # Get the raw payload and signature
    payload = request.get_data()
    signature = request.headers.get("X-Authensure-Signature", "")

    # Verify the signature
    if WEBHOOK_SECRET:
        try:
            event = WebhooksResource.construct_event(payload, signature, WEBHOOK_SECRET)
        except ValueError as e:
            print(f"⚠️ Webhook signature verification failed: {e}")
            return jsonify({"error": "Invalid signature"}), 401
    else:
        # No secret configured, parse without verification (not recommended for production)
        print("⚠️ Warning: No webhook secret configured, skipping signature verification")
        event_data = json.loads(payload)
        from authensure.types import WebhookPayload
        event = WebhookPayload.model_validate(event_data)

    print(f"\n{'=' * 50}")
    print(f"Received webhook event: {event.event}")
    print(f"Timestamp: {event.timestamp}")
    print(f"{'=' * 50}")

    # Handle the event
    handler = EVENT_HANDLERS.get(event.event)
    if handler:
        handler(event.data)
    else:
        print(f"Unhandled event type: {event.event}")
        print(f"Data: {json.dumps(event.data, indent=2)}")

    return jsonify({"received": True}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    if not WEBHOOK_SECRET:
        print("⚠️ Warning: AUTHENSURE_WEBHOOK_SECRET not set")
        print("   Webhook signatures will not be verified")
        print("   Set it with: export AUTHENSURE_WEBHOOK_SECRET='your_secret'")
        print()

    print("🚀 Starting Authensure webhook server...")
    print("   Listening on: http://localhost:5000/webhooks/authensure")
    print("   Health check: http://localhost:5000/health")
    print()
    
    app.run(host="0.0.0.0", port=5000, debug=True)
