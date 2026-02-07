"""Authentication resource for the Authensure SDK."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..types import LoginResponse, User


class AuthResource:
    """Resource for authentication operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def login(self, email: str, password: str) -> LoginResponse:
        """
        Login with email and password.

        Args:
            email: User email address.
            password: User password.

        Returns:
            LoginResponse containing access token and user info.
        """
        data = self._http.post("/auth/login", {"email": email, "password": password})
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    async def login_async(self, email: str, password: str) -> LoginResponse:
        """Async version of login."""
        data = await self._http.post_async("/auth/login", {"email": email, "password": password})
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    def register(
        self,
        email: str,
        password: str,
        name: str,
        organization_name: str | None = None,
    ) -> LoginResponse:
        """
        Register a new user.

        Args:
            email: User email address.
            password: User password.
            name: User's full name.
            organization_name: Optional organization name.

        Returns:
            LoginResponse containing access token and user info.
        """
        body: dict[str, Any] = {"email": email, "password": password, "name": name}
        if organization_name:
            body["organizationName"] = organization_name
        data = self._http.post("/auth/register", body)
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    async def register_async(
        self,
        email: str,
        password: str,
        name: str,
        organization_name: str | None = None,
    ) -> LoginResponse:
        """Async version of register."""
        body: dict[str, Any] = {"email": email, "password": password, "name": name}
        if organization_name:
            body["organizationName"] = organization_name
        data = await self._http.post_async("/auth/register", body)
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    def refresh_token(self, refresh_token: str) -> LoginResponse:
        """
        Refresh the access token.

        Args:
            refresh_token: The refresh token.

        Returns:
            LoginResponse with new access token.
        """
        data = self._http.post("/auth/refresh", {"refreshToken": refresh_token})
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    async def refresh_token_async(self, refresh_token: str) -> LoginResponse:
        """Async version of refresh_token."""
        data = await self._http.post_async("/auth/refresh", {"refreshToken": refresh_token})
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    def logout(self) -> dict[str, str]:
        """
        Logout the current user.

        Returns:
            Success message.
        """
        result = self._http.post("/auth/logout")
        self._http.clear_access_token()
        return result

    async def logout_async(self) -> dict[str, str]:
        """Async version of logout."""
        result = await self._http.post_async("/auth/logout")
        self._http.clear_access_token()
        return result

    def me(self) -> User:
        """
        Get the current authenticated user.

        Returns:
            Current user info.
        """
        data = self._http.get("/auth/me")
        return User.model_validate(data)

    async def me_async(self) -> User:
        """Async version of me."""
        data = await self._http.get_async("/auth/me")
        return User.model_validate(data)

    def verify_mfa(self, mfa_token: str, code: str, method: str = "totp") -> LoginResponse:
        """
        Verify MFA code.

        Args:
            mfa_token: The MFA token from login response.
            code: The MFA code.
            method: MFA method (default: 'totp').

        Returns:
            LoginResponse with access token.
        """
        data = self._http.post("/auth/mfa/verify", {
            "mfaToken": mfa_token,
            "code": code,
            "method": method,
        })
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    async def verify_mfa_async(self, mfa_token: str, code: str, method: str = "totp") -> LoginResponse:
        """Async version of verify_mfa."""
        data = await self._http.post_async("/auth/mfa/verify", {
            "mfaToken": mfa_token,
            "code": code,
            "method": method,
        })
        response = LoginResponse.model_validate(data)
        if response.access_token:
            self._http.set_access_token(response.access_token)
        return response

    def request_password_reset(self, email: str) -> dict[str, str]:
        """
        Request a password reset email.

        Args:
            email: User email address.

        Returns:
            Success message.
        """
        return self._http.post("/auth/forgot-password", {"email": email})

    async def request_password_reset_async(self, email: str) -> dict[str, str]:
        """Async version of request_password_reset."""
        return await self._http.post_async("/auth/forgot-password", {"email": email})

    def reset_password(self, token: str, password: str) -> dict[str, str]:
        """
        Reset password with token.

        Args:
            token: Password reset token.
            password: New password.

        Returns:
            Success message.
        """
        return self._http.post("/auth/reset-password", {"token": token, "password": password})

    async def reset_password_async(self, token: str, password: str) -> dict[str, str]:
        """Async version of reset_password."""
        return await self._http.post_async("/auth/reset-password", {"token": token, "password": password})
