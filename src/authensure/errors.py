"""Custom exceptions for the Authensure SDK."""

from typing import Any


class AuthensureError(Exception):
    """Base exception for all Authensure SDK errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    @classmethod
    def from_response(cls, response: dict[str, Any], status_code: int) -> "AuthensureError":
        """Create an error from an API response."""
        message = response.get("message") or response.get("error") or "An error occurred"
        code = cls._get_code_from_status(status_code)
        return cls(message=message, code=code, status_code=status_code, details=response)

    @staticmethod
    def _get_code_from_status(status_code: int) -> str:
        """Map HTTP status code to error code."""
        status_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "CONFLICT",
            422: "UNPROCESSABLE_ENTITY",
            429: "RATE_LIMITED",
            500: "INTERNAL_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE",
        }
        return status_map.get(status_code, "UNKNOWN_ERROR")

    def __str__(self) -> str:
        return f"AuthensureError({self.code}): {self.message}"

    def __repr__(self) -> str:
        return f"AuthensureError(message={self.message!r}, code={self.code!r}, status_code={self.status_code})"


class AuthenticationError(AuthensureError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, code="AUTHENTICATION_ERROR", status_code=401)


class RateLimitError(AuthensureError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None) -> None:
        super().__init__(message=message, code="RATE_LIMITED", status_code=429)
        self.retry_after = retry_after


class ValidationError(AuthensureError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str,
        validation_errors: dict[str, list[str]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details={"validation_errors": validation_errors} if validation_errors else None,
        )
        self.validation_errors = validation_errors


class NotFoundError(AuthensureError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(message=f"{resource} not found", code="NOT_FOUND", status_code=404)


class NetworkError(AuthensureError):
    """Raised when a network error occurs."""

    def __init__(self, message: str = "Network error occurred") -> None:
        super().__init__(message=message, code="NETWORK_ERROR", status_code=0)


class TimeoutError(AuthensureError):
    """Raised when a request times out."""

    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(message=message, code="TIMEOUT", status_code=0)
