"""Users resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import SavedSignature, Session, User, UserProfile


class UsersResource:
    """Resource for user operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def get_profile(self) -> UserProfile:
        """
        Get the current user's profile.

        Returns:
            The user profile.
        """
        data = self._http.get("/users/me")
        return UserProfile.model_validate(data)

    async def get_profile_async(self) -> UserProfile:
        """Async version of get_profile."""
        data = await self._http.get_async("/users/me")
        return UserProfile.model_validate(data)

    def update_profile(
        self,
        name: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        job_title: str | None = None,
        bio: str | None = None,
        location: str | None = None,
        website: str | None = None,
    ) -> User:
        """
        Update the current user's profile.

        Args:
            name: New name.
            phone: New phone number.
            company: New company.
            job_title: New job title.
            bio: New bio.
            location: New location.
            website: New website.

        Returns:
            The updated user.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if phone is not None:
            body["phone"] = phone
        if company is not None:
            body["company"] = company
        if job_title is not None:
            body["jobTitle"] = job_title
        if bio is not None:
            body["bio"] = bio
        if location is not None:
            body["location"] = location
        if website is not None:
            body["website"] = website
        data = self._http.patch("/users/me", body)
        return User.model_validate(data)

    async def update_profile_async(
        self,
        name: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        job_title: str | None = None,
        bio: str | None = None,
        location: str | None = None,
        website: str | None = None,
    ) -> User:
        """Async version of update_profile."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if phone is not None:
            body["phone"] = phone
        if company is not None:
            body["company"] = company
        if job_title is not None:
            body["jobTitle"] = job_title
        if bio is not None:
            body["bio"] = bio
        if location is not None:
            body["location"] = location
        if website is not None:
            body["website"] = website
        data = await self._http.patch_async("/users/me", body)
        return User.model_validate(data)

    def change_password(self, current_password: str, new_password: str) -> dict[str, str]:
        """
        Change the current user's password.

        Args:
            current_password: Current password.
            new_password: New password.

        Returns:
            Success message.
        """
        return self._http.post("/users/me/password", {
            "currentPassword": current_password,
            "newPassword": new_password,
        })

    async def change_password_async(self, current_password: str, new_password: str) -> dict[str, str]:
        """Async version of change_password."""
        return await self._http.post_async("/users/me/password", {
            "currentPassword": current_password,
            "newPassword": new_password,
        })

    def upload_avatar(self, file: bytes, filename: str) -> dict[str, str]:
        """
        Upload a new avatar.

        Args:
            file: Image file content.
            filename: Image filename.

        Returns:
            Dict containing the avatar URL.
        """
        return self._http.upload_file("/users/me/avatar", file, filename, "image/jpeg")

    async def upload_avatar_async(self, file: bytes, filename: str) -> dict[str, str]:
        """Async version of upload_avatar."""
        return await self._http.upload_file_async("/users/me/avatar", file, filename, "image/jpeg")

    def delete_avatar(self) -> dict[str, str]:
        """
        Delete the current avatar.

        Returns:
            Success message.
        """
        return self._http.delete("/users/me/avatar")

    async def delete_avatar_async(self) -> dict[str, str]:
        """Async version of delete_avatar."""
        return await self._http.delete_async("/users/me/avatar")

    def get_sessions(self) -> list[Session]:
        """
        Get all active sessions.

        Returns:
            List of sessions.
        """
        data = self._http.get("/users/me/sessions")
        return [Session.model_validate(s) for s in data]

    async def get_sessions_async(self) -> list[Session]:
        """Async version of get_sessions."""
        data = await self._http.get_async("/users/me/sessions")
        return [Session.model_validate(s) for s in data]

    def terminate_session(self, session_id: str) -> dict[str, str]:
        """
        Terminate a session.

        Args:
            session_id: The session ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/users/me/sessions/{session_id}")

    async def terminate_session_async(self, session_id: str) -> dict[str, str]:
        """Async version of terminate_session."""
        return await self._http.delete_async(f"/users/me/sessions/{session_id}")

    def terminate_all_sessions(self) -> dict[str, str]:
        """
        Terminate all other sessions.

        Returns:
            Success message.
        """
        return self._http.delete("/users/me/sessions")

    async def terminate_all_sessions_async(self) -> dict[str, str]:
        """Async version of terminate_all_sessions."""
        return await self._http.delete_async("/users/me/sessions")

    def get_signatures(self) -> list[SavedSignature]:
        """
        Get saved signatures.

        Returns:
            List of saved signatures.
        """
        data = self._http.get("/users/me/signatures")
        return [SavedSignature.model_validate(s) for s in data]

    async def get_signatures_async(self) -> list[SavedSignature]:
        """Async version of get_signatures."""
        data = await self._http.get_async("/users/me/signatures")
        return [SavedSignature.model_validate(s) for s in data]

    def create_signature(
        self,
        name: str,
        image_data: str,
        is_default: bool = False,
    ) -> SavedSignature:
        """
        Create a saved signature.

        Args:
            name: Signature name.
            image_data: Base64 encoded image data.
            is_default: Whether this is the default signature.

        Returns:
            The created signature.
        """
        data = self._http.post("/users/me/signatures", {
            "name": name,
            "imageData": image_data,
            "isDefault": is_default,
        })
        return SavedSignature.model_validate(data)

    async def create_signature_async(
        self,
        name: str,
        image_data: str,
        is_default: bool = False,
    ) -> SavedSignature:
        """Async version of create_signature."""
        data = await self._http.post_async("/users/me/signatures", {
            "name": name,
            "imageData": image_data,
            "isDefault": is_default,
        })
        return SavedSignature.model_validate(data)

    def delete_signature(self, signature_id: str) -> dict[str, str]:
        """
        Delete a saved signature.

        Args:
            signature_id: The signature ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/users/me/signatures/{signature_id}")

    async def delete_signature_async(self, signature_id: str) -> dict[str, str]:
        """Async version of delete_signature."""
        return await self._http.delete_async(f"/users/me/signatures/{signature_id}")

    def set_default_signature(self, signature_id: str) -> SavedSignature:
        """
        Set a signature as default.

        Args:
            signature_id: The signature ID.

        Returns:
            The updated signature.
        """
        data = self._http.post(f"/users/me/signatures/{signature_id}/default")
        return SavedSignature.model_validate(data)

    async def set_default_signature_async(self, signature_id: str) -> SavedSignature:
        """Async version of set_default_signature."""
        data = await self._http.post_async(f"/users/me/signatures/{signature_id}/default")
        return SavedSignature.model_validate(data)
