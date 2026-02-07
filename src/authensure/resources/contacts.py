"""Contacts resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Contact, ContactStats


class ContactsResource:
    """Resource for contact operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(
        self,
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Contact]:
        """
        List all contacts.

        Args:
            search: Optional search query.
            limit: Optional limit.
            page: Optional page number.

        Returns:
            List of contacts.
        """
        params = []
        if search:
            params.append(f"search={search}")
        if limit:
            params.append(f"limit={limit}")
        if page:
            params.append(f"page={page}")
        query = f"?{'&'.join(params)}" if params else ""
        data = self._http.get(f"/contacts{query}")
        return [Contact.model_validate(c) for c in data]

    async def list_async(
        self,
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Contact]:
        """Async version of list."""
        params = []
        if search:
            params.append(f"search={search}")
        if limit:
            params.append(f"limit={limit}")
        if page:
            params.append(f"page={page}")
        query = f"?{'&'.join(params)}" if params else ""
        data = await self._http.get_async(f"/contacts{query}")
        return [Contact.model_validate(c) for c in data]

    def get(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: The contact ID.

        Returns:
            The contact.
        """
        data = self._http.get(f"/contacts/{contact_id}")
        return Contact.model_validate(data)

    async def get_async(self, contact_id: str) -> Contact:
        """Async version of get."""
        data = await self._http.get_async(f"/contacts/{contact_id}")
        return Contact.model_validate(data)

    def create(
        self,
        email: str,
        name: str,
        company: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> Contact:
        """
        Create a new contact.

        Args:
            email: Contact email.
            name: Contact name.
            company: Optional company name.
            phone: Optional phone number.
            notes: Optional notes.

        Returns:
            The created contact.
        """
        body: dict[str, Any] = {"email": email, "name": name}
        if company:
            body["company"] = company
        if phone:
            body["phone"] = phone
        if notes:
            body["notes"] = notes
        data = self._http.post("/contacts", body)
        return Contact.model_validate(data)

    async def create_async(
        self,
        email: str,
        name: str,
        company: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> Contact:
        """Async version of create."""
        body: dict[str, Any] = {"email": email, "name": name}
        if company:
            body["company"] = company
        if phone:
            body["phone"] = phone
        if notes:
            body["notes"] = notes
        data = await self._http.post_async("/contacts", body)
        return Contact.model_validate(data)

    def update(
        self,
        contact_id: str,
        name: str | None = None,
        company: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: The contact ID.
            name: New name.
            company: New company.
            phone: New phone.
            notes: New notes.

        Returns:
            The updated contact.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if company is not None:
            body["company"] = company
        if phone is not None:
            body["phone"] = phone
        if notes is not None:
            body["notes"] = notes
        data = self._http.patch(f"/contacts/{contact_id}", body)
        return Contact.model_validate(data)

    async def update_async(
        self,
        contact_id: str,
        name: str | None = None,
        company: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> Contact:
        """Async version of update."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if company is not None:
            body["company"] = company
        if phone is not None:
            body["phone"] = phone
        if notes is not None:
            body["notes"] = notes
        data = await self._http.patch_async(f"/contacts/{contact_id}", body)
        return Contact.model_validate(data)

    def delete(self, contact_id: str) -> dict[str, str]:
        """
        Delete a contact.

        Args:
            contact_id: The contact ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/contacts/{contact_id}")

    async def delete_async(self, contact_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/contacts/{contact_id}")

    def get_stats(self) -> ContactStats:
        """
        Get contact statistics.

        Returns:
            Contact statistics.
        """
        data = self._http.get("/contacts/stats")
        return ContactStats.model_validate(data)

    async def get_stats_async(self) -> ContactStats:
        """Async version of get_stats."""
        data = await self._http.get_async("/contacts/stats")
        return ContactStats.model_validate(data)
