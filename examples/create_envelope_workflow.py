#!/usr/bin/env python3
"""
Complete envelope creation workflow example.

This example demonstrates the full workflow for:
- Creating an envelope
- Uploading a document
- Adding recipients
- Sending for signatures
- Checking envelope status
"""

import os
from pathlib import Path

from authensure import Authensure, EnvelopeStatus


def main() -> None:
    """Run complete envelope workflow example."""
    api_key = os.environ.get("AUTHENSURE_API_KEY")
    if not api_key:
        print("Error: AUTHENSURE_API_KEY environment variable not set")
        return

    client = Authensure(api_key=api_key)

    print("=== Complete Envelope Workflow ===\n")

    # Step 1: Create an envelope
    print("Step 1: Creating envelope...")
    envelope = client.envelopes.create(
        name="Sales Agreement Q1 2024",
        message="Please review and sign this sales agreement. Contact us if you have any questions.",
    )
    print(f"✓ Created envelope: {envelope.id}")

    # Step 2: Upload a document
    print("\nStep 2: Uploading document...")
    
    # Read a sample PDF file (or create sample content)
    sample_pdf_path = Path("sample_contract.pdf")
    if sample_pdf_path.exists():
        document_content = sample_pdf_path.read_bytes()
        filename = "contract.pdf"
    else:
        # For demo purposes, we'll skip the actual upload
        print("  ⚠ No sample PDF found. In production, you would upload your document here.")
        print("  Skipping document upload for this demo...")
        document = None

    # In a real scenario:
    # document = client.documents.upload(
    #     envelope_id=envelope.id,
    #     file=document_content,
    #     filename="contract.pdf",
    #     mime_type="application/pdf",
    # )
    # print(f"✓ Uploaded document: {document.id}")

    # Step 3: Add recipients
    print("\nStep 3: Adding recipients...")
    
    # Add first signer
    signer1 = client.envelopes.add_recipient(
        envelope_id=envelope.id,
        email="alice@example.com",
        name="Alice Johnson",
        role="signer",
    )
    print(f"✓ Added signer: {signer1.name} ({signer1.email})")

    # Add second signer
    signer2 = client.envelopes.add_recipient(
        envelope_id=envelope.id,
        email="bob@example.com",
        name="Bob Smith",
        role="signer",
    )
    print(f"✓ Added signer: {signer2.name} ({signer2.email})")

    # Add a CC recipient
    cc_recipient = client.envelopes.add_recipient(
        envelope_id=envelope.id,
        email="manager@example.com",
        name="Carol Manager",
        role="cc",
    )
    print(f"✓ Added CC: {cc_recipient.name} ({cc_recipient.email})")

    # Step 4: Review envelope before sending
    print("\nStep 4: Reviewing envelope...")
    envelope = client.envelopes.get(envelope.id)
    print(f"  Envelope: {envelope.name}")
    print(f"  Status: {envelope.status}")
    print(f"  Recipients: {len(envelope.recipients)}")
    for r in envelope.recipients:
        print(f"    - {r.name} ({r.role}): {r.status}")

    # Step 5: Send the envelope (commented out for safety in demo)
    print("\nStep 5: Sending envelope...")
    print("  ⚠ Sending is disabled in this demo to prevent actual emails.")
    print("  In production, you would call:")
    print("  envelope = client.envelopes.send(envelope.id)")
    
    # Uncomment to actually send:
    # envelope = client.envelopes.send(envelope.id)
    # print(f"✓ Envelope sent at: {envelope.sent_at}")

    # Step 6: Monitor envelope status
    print("\nStep 6: Checking envelope status...")
    envelope = client.envelopes.get(envelope.id)
    print(f"  Current status: {envelope.status}")
    
    if envelope.status == EnvelopeStatus.COMPLETED:
        print("  ✓ All signatures collected!")
    elif envelope.status == EnvelopeStatus.SENT:
        print("  ⏳ Waiting for signatures...")
    elif envelope.status == EnvelopeStatus.DRAFT:
        print("  📝 Envelope is still in draft mode")

    # Clean up
    print("\nCleaning up...")
    client.envelopes.delete(envelope.id)
    print("✓ Deleted demo envelope")

    print("\n=== Workflow Complete ===")


if __name__ == "__main__":
    main()
