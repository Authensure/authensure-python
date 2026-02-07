"""Webhooks resource for the Authensure SDK."""

import hashlib
import hmac
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Webhook, WebhookDelivery, WebhookPayload


class WebhooksResource:
    """Resource for webhook operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(self) -> dict[str, list[Webhook]]:
        """
        List all webhooks.

        Returns:
            Dict containing list of webhooks.
        """
        data = self._http.get("/webhooks")
        if isinstance(data, dict) and "webhooks" in data:
            return {"webhooks": [Webhook.model_validate(w) for w in data["webhooks"]]}
        return {"webhooks": [Webhook.model_validate(w) for w in data]}

    async def list_async(self) -> dict[str, list[Webhook]]:
        """Async version of list."""
        data = await self._http.get_async("/webhooks")
        if isinstance(data, dict) and "webhooks" in data:
            return {"webhooks": [Webhook.model_validate(w) for w in data["webhooks"]]}
        return {"webhooks": [Webhook.model_validate(w) for w in data]}

    def get(self, webhook_id: str) -> Webhook:
        """
        Get a webhook by ID.

        Args:
            webhook_id: The webhook ID.

        Returns:
            The webhook.
        """
        data = self._http.get(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(data)

    async def get_async(self, webhook_id: str) -> Webhook:
        """Async version of get."""
        data = await self._http.get_async(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(data)

    def create(self, url: str, events: list[str]) -> Webhook:
        """
        Create a new webhook.

        Args:
            url: Webhook URL.
            events: List of events to subscribe to.

        Returns:
            The created webhook.
        """
        data = self._http.post("/webhooks", {"url": url, "events": events})
        return Webhook.model_validate(data)

    async def create_async(self, url: str, events: list[str]) -> Webhook:
        """Async version of create."""
        data = await self._http.post_async("/webhooks", {"url": url, "events": events})
        return Webhook.model_validate(data)

    def update(
        self,
        webhook_id: str,
        url: str | None = None,
        events: list[str] | None = None,
        is_active: bool | None = None,
    ) -> Webhook:
        """
        Update a webhook.

        Args:
            webhook_id: The webhook ID.
            url: New URL.
            events: New events list.
            is_active: Whether the webhook is active.

        Returns:
            The updated webhook.
        """
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if is_active is not None:
            body["isActive"] = is_active
        data = self._http.patch(f"/webhooks/{webhook_id}", body)
        return Webhook.model_validate(data)

    async def update_async(
        self,
        webhook_id: str,
        url: str | None = None,
        events: list[str] | None = None,
        is_active: bool | None = None,
    ) -> Webhook:
        """Async version of update."""
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if is_active is not None:
            body["isActive"] = is_active
        data = await self._http.patch_async(f"/webhooks/{webhook_id}", body)
        return Webhook.model_validate(data)

    def delete(self, webhook_id: str) -> dict[str, bool]:
        """
        Delete a webhook.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Success status.
        """
        return self._http.delete(f"/webhooks/{webhook_id}")

    async def delete_async(self, webhook_id: str) -> dict[str, bool]:
        """Async version of delete."""
        return await self._http.delete_async(f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str) -> dict[str, Any]:
        """
        Test a webhook.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Test result with success status.
        """
        return self._http.post(f"/webhooks/{webhook_id}/test")

    async def test_async(self, webhook_id: str) -> dict[str, Any]:
        """Async version of test."""
        return await self._http.post_async(f"/webhooks/{webhook_id}/test")

    def get_deliveries(self, webhook_id: str) -> dict[str, list[WebhookDelivery]]:
        """
        Get webhook deliveries.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Dict containing list of deliveries.
        """
        data = self._http.get(f"/webhooks/{webhook_id}/deliveries")
        if isinstance(data, dict) and "deliveries" in data:
            return {"deliveries": [WebhookDelivery.model_validate(d) for d in data["deliveries"]]}
        return {"deliveries": [WebhookDelivery.model_validate(d) for d in data]}

    async def get_deliveries_async(self, webhook_id: str) -> dict[str, list[WebhookDelivery]]:
        """Async version of get_deliveries."""
        data = await self._http.get_async(f"/webhooks/{webhook_id}/deliveries")
        if isinstance(data, dict) and "deliveries" in data:
            return {"deliveries": [WebhookDelivery.model_validate(d) for d in data["deliveries"]]}
        return {"deliveries": [WebhookDelivery.model_validate(d) for d in data]}

    def retry_delivery(self, webhook_id: str, delivery_id: str) -> dict[str, bool]:
        """
        Retry a webhook delivery.

        Args:
            webhook_id: The webhook ID.
            delivery_id: The delivery ID.

        Returns:
            Success status.
        """
        return self._http.post(f"/webhooks/{webhook_id}/deliveries/{delivery_id}/retry")

    async def retry_delivery_async(self, webhook_id: str, delivery_id: str) -> dict[str, bool]:
        """Async version of retry_delivery."""
        return await self._http.post_async(f"/webhooks/{webhook_id}/deliveries/{delivery_id}/retry")

    def get_available_events(self) -> dict[str, list[str]]:
        """
        Get available webhook events.

        Returns:
            Dict containing list of available events.
        """
        return self._http.get("/webhooks/events")

    async def get_available_events_async(self) -> dict[str, list[str]]:
        """Async version of get_available_events."""
        return await self._http.get_async("/webhooks/events")

    @staticmethod
    def verify_signature(payload: str | bytes, signature: str, secret: str) -> bool:
        """
        Verify a webhook signature.

        Args:
            payload: The raw webhook payload.
            signature: The signature from the X-Authensure-Signature header.
            secret: Your webhook secret.

        Returns:
            True if the signature is valid.
        """
        if isinstance(payload, bytes):
            payload_bytes = payload
        else:
            payload_bytes = payload.encode("utf-8")

        expected_signature = hmac.new(
            secret.encode("utf-8"),
            payload_bytes,
            hashlib.sha256,
        ).hexdigest()

        signature_value = signature[7:] if signature.startswith("sha256=") else signature

        return hmac.compare_digest(expected_signature, signature_value)

    @staticmethod
    def construct_event(payload: str | bytes, signature: str, secret: str) -> WebhookPayload:
        """
        Construct and verify a webhook event.

        Args:
            payload: The raw webhook payload.
            signature: The signature from the X-Authensure-Signature header.
            secret: Your webhook secret.

        Returns:
            The verified webhook payload.

        Raises:
            ValueError: If the signature is invalid.
        """
        if not WebhooksResource.verify_signature(payload, signature, secret):
            raise ValueError("Invalid webhook signature")

        if isinstance(payload, bytes):
            payload_str = payload.decode("utf-8")
        else:
            payload_str = payload

        data = json.loads(payload_str)
        return WebhookPayload.model_validate(data)
