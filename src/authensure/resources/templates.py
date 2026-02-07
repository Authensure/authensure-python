"""Templates resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Envelope, Template, TemplateDocument, TemplateField, TemplateRole


class TemplatesResource:
    """Resource for template operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list(self) -> list[Template]:
        """
        List all templates.

        Returns:
            List of templates.
        """
        data = self._http.get("/templates")
        return [Template.model_validate(t) for t in data]

    async def list_async(self) -> list[Template]:
        """Async version of list."""
        data = await self._http.get_async("/templates")
        return [Template.model_validate(t) for t in data]

    def get(self, template_id: str) -> Template:
        """
        Get a template by ID.

        Args:
            template_id: The template ID.

        Returns:
            The template.
        """
        data = self._http.get(f"/templates/{template_id}")
        return Template.model_validate(data)

    async def get_async(self, template_id: str) -> Template:
        """Async version of get."""
        data = await self._http.get_async(f"/templates/{template_id}")
        return Template.model_validate(data)

    def create(self, name: str, description: str | None = None) -> Template:
        """
        Create a new template.

        Args:
            name: Template name.
            description: Optional description.

        Returns:
            The created template.
        """
        body: dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        data = self._http.post("/templates", body)
        return Template.model_validate(data)

    async def create_async(self, name: str, description: str | None = None) -> Template:
        """Async version of create."""
        body: dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        data = await self._http.post_async("/templates", body)
        return Template.model_validate(data)

    def update(
        self,
        template_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Template:
        """
        Update a template.

        Args:
            template_id: The template ID.
            name: New name.
            description: New description.

        Returns:
            The updated template.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        data = self._http.patch(f"/templates/{template_id}", body)
        return Template.model_validate(data)

    async def update_async(
        self,
        template_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Template:
        """Async version of update."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        data = await self._http.patch_async(f"/templates/{template_id}", body)
        return Template.model_validate(data)

    def delete(self, template_id: str) -> dict[str, str]:
        """
        Delete a template.

        Args:
            template_id: The template ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/templates/{template_id}")

    async def delete_async(self, template_id: str) -> dict[str, str]:
        """Async version of delete."""
        return await self._http.delete_async(f"/templates/{template_id}")

    def get_usage(self) -> dict[str, int]:
        """
        Get template usage statistics.

        Returns:
            Usage stats with used, limit, and remaining.
        """
        return self._http.get("/templates/usage")

    async def get_usage_async(self) -> dict[str, int]:
        """Async version of get_usage."""
        return await self._http.get_async("/templates/usage")

    def get_marketplace(self, category: str | None = None) -> list[Template]:
        """
        Get marketplace templates.

        Args:
            category: Optional category filter.

        Returns:
            List of marketplace templates.
        """
        query = f"?category={category}" if category else ""
        data = self._http.get(f"/templates/marketplace{query}")
        return [Template.model_validate(t) for t in data]

    async def get_marketplace_async(self, category: str | None = None) -> list[Template]:
        """Async version of get_marketplace."""
        query = f"?category={category}" if category else ""
        data = await self._http.get_async(f"/templates/marketplace{query}")
        return [Template.model_validate(t) for t in data]

    def add_marketplace_template(self, template_id: str) -> Template:
        """
        Add a marketplace template to your templates.

        Args:
            template_id: The marketplace template ID.

        Returns:
            The added template.
        """
        data = self._http.post(f"/templates/marketplace/{template_id}/add")
        return Template.model_validate(data)

    async def add_marketplace_template_async(self, template_id: str) -> Template:
        """Async version of add_marketplace_template."""
        data = await self._http.post_async(f"/templates/marketplace/{template_id}/add")
        return Template.model_validate(data)

    def add_role(
        self,
        template_id: str,
        name: str,
        order_index: int | None = None,
    ) -> TemplateRole:
        """
        Add a role to a template.

        Args:
            template_id: The template ID.
            name: Role name.
            order_index: Optional order index.

        Returns:
            The created role.
        """
        body: dict[str, Any] = {"name": name}
        if order_index is not None:
            body["orderIndex"] = order_index
        data = self._http.post(f"/templates/{template_id}/roles", body)
        return TemplateRole.model_validate(data)

    async def add_role_async(
        self,
        template_id: str,
        name: str,
        order_index: int | None = None,
    ) -> TemplateRole:
        """Async version of add_role."""
        body: dict[str, Any] = {"name": name}
        if order_index is not None:
            body["orderIndex"] = order_index
        data = await self._http.post_async(f"/templates/{template_id}/roles", body)
        return TemplateRole.model_validate(data)

    def update_role(
        self,
        template_id: str,
        role_id: str,
        name: str | None = None,
        order_index: int | None = None,
    ) -> TemplateRole:
        """
        Update a template role.

        Args:
            template_id: The template ID.
            role_id: The role ID.
            name: New name.
            order_index: New order index.

        Returns:
            The updated role.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if order_index is not None:
            body["orderIndex"] = order_index
        data = self._http.patch(f"/templates/{template_id}/roles/{role_id}", body)
        return TemplateRole.model_validate(data)

    async def update_role_async(
        self,
        template_id: str,
        role_id: str,
        name: str | None = None,
        order_index: int | None = None,
    ) -> TemplateRole:
        """Async version of update_role."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if order_index is not None:
            body["orderIndex"] = order_index
        data = await self._http.patch_async(f"/templates/{template_id}/roles/{role_id}", body)
        return TemplateRole.model_validate(data)

    def delete_role(self, template_id: str, role_id: str) -> dict[str, str]:
        """
        Delete a template role.

        Args:
            template_id: The template ID.
            role_id: The role ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/templates/{template_id}/roles/{role_id}")

    async def delete_role_async(self, template_id: str, role_id: str) -> dict[str, str]:
        """Async version of delete_role."""
        return await self._http.delete_async(f"/templates/{template_id}/roles/{role_id}")

    def upload_document(
        self,
        template_id: str,
        file: bytes,
        filename: str,
        mime_type: str = "application/pdf",
    ) -> TemplateDocument:
        """
        Upload a document to a template.

        Args:
            template_id: The template ID.
            file: File content as bytes.
            filename: Name of the file.
            mime_type: MIME type (default: 'application/pdf').

        Returns:
            The created template document.
        """
        data = self._http.upload_file(
            f"/templates/{template_id}/documents",
            file,
            filename,
            mime_type,
        )
        return TemplateDocument.model_validate(data)

    async def upload_document_async(
        self,
        template_id: str,
        file: bytes,
        filename: str,
        mime_type: str = "application/pdf",
    ) -> TemplateDocument:
        """Async version of upload_document."""
        data = await self._http.upload_file_async(
            f"/templates/{template_id}/documents",
            file,
            filename,
            mime_type,
        )
        return TemplateDocument.model_validate(data)

    def add_field(
        self,
        template_id: str,
        document_id: str,
        field_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        page: int,
        role_id: str | None = None,
        label: str | None = None,
        placeholder: str | None = None,
        required: bool = True,
    ) -> TemplateField:
        """
        Add a field to a template document.

        Args:
            template_id: The template ID.
            document_id: The document ID.
            field_type: Type of field.
            x: X position.
            y: Y position.
            width: Field width.
            height: Field height.
            page: Page number.
            role_id: Optional role ID.
            label: Optional field label.
            placeholder: Optional placeholder text.
            required: Whether field is required.

        Returns:
            The created field.
        """
        body: dict[str, Any] = {
            "type": field_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "page": page,
            "required": required,
        }
        if role_id:
            body["roleId"] = role_id
        if label:
            body["label"] = label
        if placeholder:
            body["placeholder"] = placeholder

        data = self._http.post(
            f"/templates/{template_id}/documents/{document_id}/fields",
            body,
        )
        return TemplateField.model_validate(data)

    async def add_field_async(
        self,
        template_id: str,
        document_id: str,
        field_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        page: int,
        role_id: str | None = None,
        label: str | None = None,
        placeholder: str | None = None,
        required: bool = True,
    ) -> TemplateField:
        """Async version of add_field."""
        body: dict[str, Any] = {
            "type": field_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "page": page,
            "required": required,
        }
        if role_id:
            body["roleId"] = role_id
        if label:
            body["label"] = label
        if placeholder:
            body["placeholder"] = placeholder

        data = await self._http.post_async(
            f"/templates/{template_id}/documents/{document_id}/fields",
            body,
        )
        return TemplateField.model_validate(data)

    def update_field(
        self,
        template_id: str,
        document_id: str,
        field_id: str,
        **kwargs: Any,
    ) -> TemplateField:
        """
        Update a template field.

        Args:
            template_id: The template ID.
            document_id: The document ID.
            field_id: The field ID.
            **kwargs: Field properties to update.

        Returns:
            The updated field.
        """
        data = self._http.patch(
            f"/templates/{template_id}/documents/{document_id}/fields/{field_id}",
            kwargs,
        )
        return TemplateField.model_validate(data)

    async def update_field_async(
        self,
        template_id: str,
        document_id: str,
        field_id: str,
        **kwargs: Any,
    ) -> TemplateField:
        """Async version of update_field."""
        data = await self._http.patch_async(
            f"/templates/{template_id}/documents/{document_id}/fields/{field_id}",
            kwargs,
        )
        return TemplateField.model_validate(data)

    def delete_field(
        self,
        template_id: str,
        document_id: str,
        field_id: str,
    ) -> dict[str, str]:
        """
        Delete a template field.

        Args:
            template_id: The template ID.
            document_id: The document ID.
            field_id: The field ID.

        Returns:
            Success message.
        """
        return self._http.delete(
            f"/templates/{template_id}/documents/{document_id}/fields/{field_id}"
        )

    async def delete_field_async(
        self,
        template_id: str,
        document_id: str,
        field_id: str,
    ) -> dict[str, str]:
        """Async version of delete_field."""
        return await self._http.delete_async(
            f"/templates/{template_id}/documents/{document_id}/fields/{field_id}"
        )

    def use(
        self,
        template_id: str,
        name: str,
        recipients: list[dict[str, str]],
    ) -> Envelope:
        """
        Create an envelope from a template.

        Args:
            template_id: The template ID.
            name: Name for the new envelope.
            recipients: List of recipient dicts with roleId, email, and name.

        Returns:
            The created envelope.
        """
        data = self._http.post(f"/templates/{template_id}/use", {
            "name": name,
            "recipients": recipients,
        })
        return Envelope.model_validate(data)

    async def use_async(
        self,
        template_id: str,
        name: str,
        recipients: list[dict[str, str]],
    ) -> Envelope:
        """Async version of use."""
        data = await self._http.post_async(f"/templates/{template_id}/use", {
            "name": name,
            "recipients": recipients,
        })
        return Envelope.model_validate(data)

    def get_submissions(self, template_id: str) -> list[Any]:
        """
        Get template submissions.

        Args:
            template_id: The template ID.

        Returns:
            List of submissions.
        """
        return self._http.get(f"/templates/{template_id}/submissions")

    async def get_submissions_async(self, template_id: str) -> list[Any]:
        """Async version of get_submissions."""
        return await self._http.get_async(f"/templates/{template_id}/submissions")

    def review_submission(
        self,
        template_id: str,
        submission_id: str,
        action: str,
        notes: str | None = None,
    ) -> dict[str, str]:
        """
        Review a template submission.

        Args:
            template_id: The template ID.
            submission_id: The submission ID.
            action: 'approve' or 'reject'.
            notes: Optional notes.

        Returns:
            Success message.
        """
        body: dict[str, Any] = {"action": action}
        if notes:
            body["notes"] = notes
        return self._http.post(
            f"/templates/{template_id}/submissions/{submission_id}/review",
            body,
        )

    async def review_submission_async(
        self,
        template_id: str,
        submission_id: str,
        action: str,
        notes: str | None = None,
    ) -> dict[str, str]:
        """Async version of review_submission."""
        body: dict[str, Any] = {"action": action}
        if notes:
            body["notes"] = notes
        return await self._http.post_async(
            f"/templates/{template_id}/submissions/{submission_id}/review",
            body,
        )
