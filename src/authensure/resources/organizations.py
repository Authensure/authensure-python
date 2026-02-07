"""Organizations resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import Organization, OrganizationSettings


class OrganizationsResource:
    """Resource for organization operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def get(self) -> Organization:
        """
        Get the current organization.

        Returns:
            The organization.
        """
        data = self._http.get("/organizations/me")
        return Organization.model_validate(data)

    async def get_async(self) -> Organization:
        """Async version of get."""
        data = await self._http.get_async("/organizations/me")
        return Organization.model_validate(data)

    def update(
        self,
        name: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        size: str | None = None,
    ) -> Organization:
        """
        Update the current organization.

        Args:
            name: New name.
            website: New website.
            industry: New industry.
            size: New size.

        Returns:
            The updated organization.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if website is not None:
            body["website"] = website
        if industry is not None:
            body["industry"] = industry
        if size is not None:
            body["size"] = size
        data = self._http.patch("/organizations/me", body)
        return Organization.model_validate(data)

    async def update_async(
        self,
        name: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        size: str | None = None,
    ) -> Organization:
        """Async version of update."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if website is not None:
            body["website"] = website
        if industry is not None:
            body["industry"] = industry
        if size is not None:
            body["size"] = size
        data = await self._http.patch_async("/organizations/me", body)
        return Organization.model_validate(data)

    def upload_logo(self, file: bytes, filename: str) -> dict[str, str]:
        """
        Upload a new organization logo.

        Args:
            file: Image file content.
            filename: Image filename.

        Returns:
            Dict containing the logo URL.
        """
        return self._http.upload_file("/organizations/me/logo", file, filename, "image/png")

    async def upload_logo_async(self, file: bytes, filename: str) -> dict[str, str]:
        """Async version of upload_logo."""
        return await self._http.upload_file_async("/organizations/me/logo", file, filename, "image/png")

    def delete_logo(self) -> dict[str, str]:
        """
        Delete the organization logo.

        Returns:
            Success message.
        """
        return self._http.delete("/organizations/me/logo")

    async def delete_logo_async(self) -> dict[str, str]:
        """Async version of delete_logo."""
        return await self._http.delete_async("/organizations/me/logo")

    def get_settings(self) -> OrganizationSettings:
        """
        Get organization settings.

        Returns:
            The organization settings.
        """
        data = self._http.get("/organizations/me/settings")
        return OrganizationSettings.model_validate(data)

    async def get_settings_async(self) -> OrganizationSettings:
        """Async version of get_settings."""
        data = await self._http.get_async("/organizations/me/settings")
        return OrganizationSettings.model_validate(data)

    def update_settings(self, **kwargs: Any) -> OrganizationSettings:
        """
        Update organization settings.

        Args:
            **kwargs: Settings to update.

        Returns:
            The updated settings.
        """
        data = self._http.patch("/organizations/me/settings", kwargs)
        return OrganizationSettings.model_validate(data)

    async def update_settings_async(self, **kwargs: Any) -> OrganizationSettings:
        """Async version of update_settings."""
        data = await self._http.patch_async("/organizations/me/settings", kwargs)
        return OrganizationSettings.model_validate(data)

    def get_branding(self) -> dict[str, Any]:
        """
        Get organization branding.

        Returns:
            Branding configuration.
        """
        return self._http.get("/organizations/me/branding")

    async def get_branding_async(self) -> dict[str, Any]:
        """Async version of get_branding."""
        return await self._http.get_async("/organizations/me/branding")

    def update_branding(self, **kwargs: Any) -> dict[str, Any]:
        """
        Update organization branding.

        Args:
            **kwargs: Branding options to update.

        Returns:
            Updated branding configuration.
        """
        return self._http.patch("/organizations/me/branding", kwargs)

    async def update_branding_async(self, **kwargs: Any) -> dict[str, Any]:
        """Async version of update_branding."""
        return await self._http.patch_async("/organizations/me/branding", kwargs)
