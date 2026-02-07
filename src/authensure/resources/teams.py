"""Teams resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import TeamInvitation, TeamMember, User, UserRole


class TeamsResource:
    """Resource for team operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def list_members(self) -> list[TeamMember]:
        """
        List all team members.

        Returns:
            List of team members.
        """
        data = self._http.get("/teams/members")
        return [TeamMember.model_validate(m) for m in data]

    async def list_members_async(self) -> list[TeamMember]:
        """Async version of list_members."""
        data = await self._http.get_async("/teams/members")
        return [TeamMember.model_validate(m) for m in data]

    def get_member(self, member_id: str) -> TeamMember:
        """
        Get a team member by ID.

        Args:
            member_id: The member ID.

        Returns:
            The team member.
        """
        data = self._http.get(f"/teams/members/{member_id}")
        return TeamMember.model_validate(data)

    async def get_member_async(self, member_id: str) -> TeamMember:
        """Async version of get_member."""
        data = await self._http.get_async(f"/teams/members/{member_id}")
        return TeamMember.model_validate(data)

    def update_member_role(self, member_id: str, role: UserRole | str) -> TeamMember:
        """
        Update a team member's role.

        Args:
            member_id: The member ID.
            role: New role.

        Returns:
            The updated team member.
        """
        data = self._http.patch(f"/teams/members/{member_id}", {"role": role})
        return TeamMember.model_validate(data)

    async def update_member_role_async(self, member_id: str, role: UserRole | str) -> TeamMember:
        """Async version of update_member_role."""
        data = await self._http.patch_async(f"/teams/members/{member_id}", {"role": role})
        return TeamMember.model_validate(data)

    def remove_member(self, member_id: str) -> dict[str, str]:
        """
        Remove a team member.

        Args:
            member_id: The member ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/teams/members/{member_id}")

    async def remove_member_async(self, member_id: str) -> dict[str, str]:
        """Async version of remove_member."""
        return await self._http.delete_async(f"/teams/members/{member_id}")

    def suspend_member(self, member_id: str) -> TeamMember:
        """
        Suspend a team member.

        Args:
            member_id: The member ID.

        Returns:
            The suspended team member.
        """
        data = self._http.post(f"/teams/members/{member_id}/suspend")
        return TeamMember.model_validate(data)

    async def suspend_member_async(self, member_id: str) -> TeamMember:
        """Async version of suspend_member."""
        data = await self._http.post_async(f"/teams/members/{member_id}/suspend")
        return TeamMember.model_validate(data)

    def reactivate_member(self, member_id: str) -> TeamMember:
        """
        Reactivate a suspended team member.

        Args:
            member_id: The member ID.

        Returns:
            The reactivated team member.
        """
        data = self._http.post(f"/teams/members/{member_id}/reactivate")
        return TeamMember.model_validate(data)

    async def reactivate_member_async(self, member_id: str) -> TeamMember:
        """Async version of reactivate_member."""
        data = await self._http.post_async(f"/teams/members/{member_id}/reactivate")
        return TeamMember.model_validate(data)

    def list_invitations(self) -> list[TeamInvitation]:
        """
        List all pending invitations.

        Returns:
            List of invitations.
        """
        data = self._http.get("/teams/invitations")
        return [TeamInvitation.model_validate(i) for i in data]

    async def list_invitations_async(self) -> list[TeamInvitation]:
        """Async version of list_invitations."""
        data = await self._http.get_async("/teams/invitations")
        return [TeamInvitation.model_validate(i) for i in data]

    def invite_member(self, email: str, role: UserRole | str) -> TeamInvitation:
        """
        Invite a new team member.

        Args:
            email: Email address.
            role: Role for the new member.

        Returns:
            The created invitation.
        """
        data = self._http.post("/teams/invitations", {"email": email, "role": role})
        return TeamInvitation.model_validate(data)

    async def invite_member_async(self, email: str, role: UserRole | str) -> TeamInvitation:
        """Async version of invite_member."""
        data = await self._http.post_async("/teams/invitations", {"email": email, "role": role})
        return TeamInvitation.model_validate(data)

    def cancel_invitation(self, invitation_id: str) -> dict[str, str]:
        """
        Cancel a pending invitation.

        Args:
            invitation_id: The invitation ID.

        Returns:
            Success message.
        """
        return self._http.delete(f"/teams/invitations/{invitation_id}")

    async def cancel_invitation_async(self, invitation_id: str) -> dict[str, str]:
        """Async version of cancel_invitation."""
        return await self._http.delete_async(f"/teams/invitations/{invitation_id}")

    def resend_invitation(self, invitation_id: str) -> TeamInvitation:
        """
        Resend an invitation email.

        Args:
            invitation_id: The invitation ID.

        Returns:
            The invitation.
        """
        data = self._http.post(f"/teams/invitations/{invitation_id}/resend")
        return TeamInvitation.model_validate(data)

    async def resend_invitation_async(self, invitation_id: str) -> TeamInvitation:
        """Async version of resend_invitation."""
        data = await self._http.post_async(f"/teams/invitations/{invitation_id}/resend")
        return TeamInvitation.model_validate(data)

    def accept_invitation(
        self,
        token: str,
        name: str,
        password: str,
    ) -> dict[str, Any]:
        """
        Accept an invitation and create account.

        Args:
            token: Invitation token.
            name: Full name.
            password: Account password.

        Returns:
            Login response with access token.
        """
        return self._http.post("/teams/invitations/accept", {
            "token": token,
            "name": name,
            "password": password,
        })

    async def accept_invitation_async(
        self,
        token: str,
        name: str,
        password: str,
    ) -> dict[str, Any]:
        """Async version of accept_invitation."""
        return await self._http.post_async("/teams/invitations/accept", {
            "token": token,
            "name": name,
            "password": password,
        })
