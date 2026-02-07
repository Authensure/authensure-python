#!/usr/bin/env python3
"""
Async usage example for the Authensure Python SDK.

This example demonstrates:
- Using async/await for API calls
- Running parallel operations
- Using the async context manager

Requirements:
    Python 3.9+
"""

import asyncio
import os

from authensure import Authensure


async def main() -> None:
    """Run async usage examples."""
    api_key = os.environ.get("AUTHENSURE_API_KEY")
    if not api_key:
        print("Error: AUTHENSURE_API_KEY environment variable not set")
        return

    print("=== Authensure Python SDK Async Usage ===\n")

    # Using async context manager for automatic cleanup
    async with Authensure(api_key=api_key) as client:
        
        # Example 1: Basic async operation
        print("1. Creating envelope asynchronously...")
        envelope = await client.envelopes.create_async(
            name="Async Test Envelope",
            message="Created using async/await",
        )
        print(f"   ✓ Created: {envelope.id}")

        # Example 2: Parallel operations
        print("\n2. Running parallel operations...")
        
        # Create multiple recipients in parallel
        recipient_tasks = [
            client.envelopes.add_recipient_async(
                envelope.id,
                email=f"signer{i}@example.com",
                name=f"Signer {i}",
            )
            for i in range(1, 4)
        ]
        
        recipients = await asyncio.gather(*recipient_tasks)
        print(f"   ✓ Added {len(recipients)} recipients in parallel")
        for r in recipients:
            print(f"     - {r.name}: {r.email}")

        # Example 3: Fetching data in parallel
        print("\n3. Fetching data in parallel...")
        
        # Fetch envelope and list templates concurrently
        envelope_task = client.envelopes.get_async(envelope.id)
        templates_task = client.templates.list_async()
        
        envelope_data, templates = await asyncio.gather(
            envelope_task,
            templates_task,
        )
        
        print(f"   ✓ Envelope has {len(envelope_data.recipients)} recipients")
        print(f"   ✓ Found {len(templates)} templates")

        # Example 4: Sequential async with await
        print("\n4. Sequential async operations...")
        
        # Update envelope
        updated = await client.envelopes.update_async(
            envelope.id,
            name="Updated Async Envelope",
        )
        print(f"   ✓ Updated name to: {updated.name}")

        # Get updated envelope
        final = await client.envelopes.get_async(envelope.id)
        print(f"   ✓ Final status: {final.status}")

        # Cleanup
        print("\n5. Cleaning up...")
        await client.envelopes.delete_async(envelope.id)
        print("   ✓ Deleted test envelope")

    print("\n=== Async Example Complete ===")


async def batch_operations_example() -> None:
    """Example of batch operations with rate limiting."""
    api_key = os.environ.get("AUTHENSURE_API_KEY")
    if not api_key:
        return

    print("\n=== Batch Operations Example ===\n")

    async with Authensure(api_key=api_key) as client:
        # Create multiple envelopes with controlled concurrency
        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

        async def create_envelope_limited(index: int):
            async with semaphore:
                envelope = await client.envelopes.create_async(
                    name=f"Batch Envelope {index}",
                )
                print(f"  Created envelope {index}: {envelope.id}")
                return envelope

        # Create 10 envelopes with max 5 concurrent requests
        print("Creating 10 envelopes (max 5 concurrent)...")
        tasks = [create_envelope_limited(i) for i in range(1, 11)]
        envelopes = await asyncio.gather(*tasks)
        print(f"\n✓ Created {len(envelopes)} envelopes")

        # Clean up all envelopes
        print("\nCleaning up...")
        delete_tasks = [
            client.envelopes.delete_async(env.id)
            for env in envelopes
        ]
        await asyncio.gather(*delete_tasks)
        print("✓ All envelopes deleted")


if __name__ == "__main__":
    asyncio.run(main())
    # Uncomment to run batch example:
    # asyncio.run(batch_operations_example())
