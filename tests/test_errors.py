"""Tests for error handling."""

import pytest
import respx
from httpx import Response

from authensure import (
    Authensure,
    AuthensureError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from authensure.errors import NetworkError, TimeoutError


class TestErrorClasses:
    """Tests for error classes."""

    def test_authensure_error_creation(self):
        """Test creating a base AuthensureError."""
        error = AuthensureError(
            message="Test error",
            code="TEST_ERROR",
            status_code=400,
            details={"field": "value"},
        )
        
        assert error.message == "Test error"
        assert error.code == "TEST_ERROR"
        assert error.status_code == 400
        assert error.details == {"field": "value"}
        assert str(error) == "AuthensureError(TEST_ERROR): Test error"

    def test_authensure_error_from_response(self):
        """Test creating error from API response."""
        response = {"message": "Bad request", "statusCode": 400}
        error = AuthensureError.from_response(response, 400)
        
        assert error.message == "Bad request"
        assert error.code == "BAD_REQUEST"
        assert error.status_code == 400

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError()
        
        assert error.message == "Authentication failed"
        assert error.code == "AUTHENTICATION_ERROR"
        assert error.status_code == 401

    def test_authentication_error_custom_message(self):
        """Test AuthenticationError with custom message."""
        error = AuthenticationError("Invalid API key")
        
        assert error.message == "Invalid API key"

    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError(retry_after=60)
        
        assert error.message == "Rate limit exceeded"
        assert error.code == "RATE_LIMITED"
        assert error.status_code == 429
        assert error.retry_after == 60

    def test_validation_error(self):
        """Test ValidationError."""
        validation_errors = {"email": ["Invalid email format"]}
        error = ValidationError("Validation failed", validation_errors)
        
        assert error.message == "Validation failed"
        assert error.code == "VALIDATION_ERROR"
        assert error.status_code == 422
        assert error.validation_errors == validation_errors

    def test_not_found_error(self):
        """Test NotFoundError."""
        error = NotFoundError("Envelope")
        
        assert error.message == "Envelope not found"
        assert error.code == "NOT_FOUND"
        assert error.status_code == 404

    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError("Connection refused")
        
        assert error.message == "Connection refused"
        assert error.code == "NETWORK_ERROR"
        assert error.status_code == 0

    def test_timeout_error(self):
        """Test TimeoutError."""
        error = TimeoutError()
        
        assert error.message == "Request timed out"
        assert error.code == "TIMEOUT"
        assert error.status_code == 0


class TestHttpErrorHandling:
    """Tests for HTTP error handling."""

    def test_401_raises_authentication_error(self, client: Authensure, mock_api):
        """Test that 401 response raises AuthenticationError."""
        mock_api.get("/envelopes").mock(
            return_value=Response(401, json={"message": "Invalid API key"})
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            client.envelopes.list()
        
        assert exc_info.value.message == "Invalid API key"

    def test_404_raises_not_found_error(self, client: Authensure, mock_api):
        """Test that 404 response raises NotFoundError."""
        mock_api.get("/envelopes/invalid_id").mock(
            return_value=Response(404, json={"message": "Envelope not found"})
        )
        
        with pytest.raises(NotFoundError):
            client.envelopes.get("invalid_id")

    def test_429_raises_rate_limit_error(self, client: Authensure, mock_api):
        """Test that 429 response raises RateLimitError."""
        mock_api.get("/envelopes").mock(
            return_value=Response(
                429,
                json={"message": "Rate limit exceeded", "retryAfter": 60},
            )
        )
        
        # Disable retries for this test
        client._http.retry_attempts = 0
        
        with pytest.raises(RateLimitError) as exc_info:
            client.envelopes.list()
        
        assert exc_info.value.retry_after == 60

    def test_500_raises_authensure_error(self, client: Authensure, mock_api):
        """Test that 500 response raises AuthensureError."""
        mock_api.get("/envelopes").mock(
            return_value=Response(500, json={"message": "Internal server error"})
        )
        
        # Disable retries for this test
        client._http.retry_attempts = 0
        
        with pytest.raises(AuthensureError) as exc_info:
            client.envelopes.list()
        
        assert exc_info.value.status_code == 500

    def test_error_preserves_details(self, client: Authensure, mock_api):
        """Test that error response details are preserved."""
        mock_api.get("/envelopes").mock(
            return_value=Response(
                400,
                json={
                    "message": "Validation failed",
                    "errors": {"name": ["Required field"]},
                },
            )
        )
        
        with pytest.raises(AuthensureError) as exc_info:
            client.envelopes.list()
        
        assert "errors" in exc_info.value.details
