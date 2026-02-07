#!/usr/bin/env python3
"""
Basic usage example for the Authensure Python SDK.

This example demonstrates:
- Initializing the client
- Creating an envelope
- Adding a recipient
- Sending for signature
"""

import os

from authensure import Authensure


def main() -> None:
    """Run basic usage example."""
    # Get API key from environment
    api_key = os.environ.get("AUTHENSURE_API_KEY")
    if not api_key:
        print("Error: AUTHENSURE_API_KEY environment variable not set")
        print("Set it with: export AUTHENSURE_API_KEY='your_api_key_here'")
        return

    # Initialize the client
    client = Authensure(api_key=api_key)

    print("=== Authensure Python SDK Basic Usage ===\n")

    # Create an envelope
    print("Creating envelope...")
    envelope = client.envelopes.create(
        name="Contract Agreement",
        message="Please review and sign this contract at your earliest convenience.",
    )
    print(f"✓ Created envelope: {envelope.id}")
    print(f"  Name: {envelope.name}")
    print(f"  Status: {envelope.status}")

    # Add a recipient
    print("\nAdding recipient...")
    recipient = client.envelopes.add_recipient(
        envelope_id=envelope.id,
        email="signer@example.com",
        name="John Doe",
        role="signer",
    )
    print(f"✓ Added recipient: {recipient.id}")
    print(f"  Email: {recipient.email}")
    print(f"  Name: {recipient.name}")

    # Get the envelope to see updated state
    print("\nFetching envelope details...")
    envelope = client.envelopes.get(envelope.id)
    print(f"✓ Envelope has {len(envelope.recipients)} recipient(s)")

    # Note: In a real scenario, you would upload documents before sending
    print("\n⚠ Note: Upload documents before sending the envelope")
    print("  See create_envelope_workflow.py for a complete example")

    # List all envelopes
    print("\nListing all envelopes...")
    envelopes = client.envelopes.list()
    print(f"✓ Found {len(envelopes)} envelope(s)")

    # Clean up - delete the test envelope
    print("\nCleaning up...")
    client.envelopes.delete(envelope.id)
    print("✓ Deleted test envelope")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
