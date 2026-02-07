"""HTTP client for the Authensure SDK."""

import asyncio
import logging
from typing import Any, BinaryIO

import httpx

from .errors import (
    AuthensureError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
)
from .types import AuthensureConfig

logger = logging.getLogger("authensure")

DEFAULT_BASE_URL = "https://api.authensure.app/api"
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0


class HttpClient:
    """HTTP client for making requests to the Authensure API."""

    def __init__(self, config: AuthensureConfig) -> None:
        self.base_url = config.base_url or DEFAULT_BASE_URL
        self.api_key = config.api_key
        self.access_token = config.access_token
        self.timeout = config.timeout or DEFAULT_TIMEOUT
        self.retry_attempts = config.retry_attempts if config.retry_attempts is not None else DEFAULT_RETRY_ATTEMPTS
        self.retry_delay = config.retry_delay if config.retry_delay is not None else DEFAULT_RETRY_DELAY
        self.debug = config.debug or False

        self._client = httpx.Client(timeout=self.timeout)
        self._async_client: httpx.AsyncClient | None = None

    def set_access_token(self, token: str) -> None:
        """Set the access token for authentication."""
        self.access_token = token

    def clear_access_token(self) -> None:
        """Clear the access token."""
        self.access_token = None

    def _get_auth_header(self) -> str | None:
        """Get the authorization header value."""
        if self.access_token:
            return f"Bearer {self.access_token}"
        if self.api_key:
            return f"Bearer {self.api_key}"
        return None

    def _log(self, message: str, data: Any = None) -> None:
        """Log a debug message if debug mode is enabled."""
        if self.debug:
            if data is not None:
                logger.debug("[Authensure SDK] %s %s", message, data)
            else:
                logger.debug("[Authensure SDK] %s", message)

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Check if the request should be retried."""
        if attempt >= self.retry_attempts:
            return False
        return status_code == 429 or status_code >= 500

    def _get_retry_delay(self, attempt: int, retry_after: int | None = None) -> float:
        """Calculate the retry delay with exponential backoff."""
        if retry_after:
            return float(retry_after)
        return self.retry_delay * (2 ** attempt)

    def _create_error(self, status_code: int, data: Any) -> AuthensureError:
        """Create an appropriate error from the response."""
        if isinstance(data, dict):
            message = data.get("message") or data.get("error") or "Request failed"
            retry_after = data.get("retryAfter")
        else:
            message = str(data) if data else "Request failed"
            retry_after = None

        if status_code == 401:
            return AuthenticationError(message)
        if status_code == 404:
            return NotFoundError()
        if status_code == 429:
            return RateLimitError(message, retry_after)
        return AuthensureError.from_response(data if isinstance(data, dict) else {"message": message}, status_code)

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Make a synchronous HTTP request."""
        url = f"{self.base_url}{path}"
        attempt = 0

        while True:
            try:
                request_headers: dict[str, str] = {
                    "Accept": "application/json",
                    **(headers or {}),
                }

                auth_header = self._get_auth_header()
                if auth_header:
                    request_headers["Authorization"] = auth_header

                if body is not None and not isinstance(body, (bytes, BinaryIO)):
                    request_headers["Content-Type"] = "application/json"

                self._log(f"{method} {path}", body if not isinstance(body, bytes) else "[binary]")

                response = self._client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=body if body is not None and not isinstance(body, (bytes, BinaryIO)) else None,
                    content=body if isinstance(body, bytes) else None,
                )

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    data = response.json()
                elif "application/pdf" in content_type or "application/octet-stream" in content_type:
                    data = response.content
                else:
                    data = response.text

                self._log(f"Response {response.status_code}", data if not isinstance(data, bytes) else "[binary]")

                if not response.is_success:
                    error = self._create_error(response.status_code, data)

                    if self._should_retry(response.status_code, attempt):
                        retry_after_header = response.headers.get("Retry-After")
                        delay = self._get_retry_delay(
                            attempt,
                            int(retry_after_header) if retry_after_header else None
                        )
                        self._log(f"Retrying in {delay}s (attempt {attempt + 1}/{self.retry_attempts})")
                        import time
                        time.sleep(delay)
                        attempt += 1
                        continue

                    raise error

                return data

            except httpx.TimeoutException:
                raise TimeoutError()
            except httpx.ConnectError as e:
                raise NetworkError(str(e))
            except AuthensureError:
                raise
            except Exception as e:
                raise NetworkError(f"An unexpected error occurred: {e}")

    async def request_async(
        self,
        method: str,
        path: str,
        body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Make an asynchronous HTTP request."""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(timeout=self.timeout)

        url = f"{self.base_url}{path}"
        attempt = 0

        while True:
            try:
                request_headers: dict[str, str] = {
                    "Accept": "application/json",
                    **(headers or {}),
                }

                auth_header = self._get_auth_header()
                if auth_header:
                    request_headers["Authorization"] = auth_header

                if body is not None and not isinstance(body, (bytes, BinaryIO)):
                    request_headers["Content-Type"] = "application/json"

                self._log(f"{method} {path}", body if not isinstance(body, bytes) else "[binary]")

                response = await self._async_client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=body if body is not None and not isinstance(body, (bytes, BinaryIO)) else None,
                    content=body if isinstance(body, bytes) else None,
                )

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    data = response.json()
                elif "application/pdf" in content_type or "application/octet-stream" in content_type:
                    data = response.content
                else:
                    data = response.text

                self._log(f"Response {response.status_code}", data if not isinstance(data, bytes) else "[binary]")

                if not response.is_success:
                    error = self._create_error(response.status_code, data)

                    if self._should_retry(response.status_code, attempt):
                        retry_after_header = response.headers.get("Retry-After")
                        delay = self._get_retry_delay(
                            attempt,
                            int(retry_after_header) if retry_after_header else None
                        )
                        self._log(f"Retrying in {delay}s (attempt {attempt + 1}/{self.retry_attempts})")
                        await asyncio.sleep(delay)
                        attempt += 1
                        continue

                    raise error

                return data

            except httpx.TimeoutException:
                raise TimeoutError()
            except httpx.ConnectError as e:
                raise NetworkError(str(e))
            except AuthensureError:
                raise
            except Exception as e:
                raise NetworkError(f"An unexpected error occurred: {e}")

    def get(self, path: str, headers: dict[str, str] | None = None) -> Any:
        """Make a GET request."""
        return self.request("GET", path, headers=headers)

    def post(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make a POST request."""
        return self.request("POST", path, body, headers)

    def put(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make a PUT request."""
        return self.request("PUT", path, body, headers)

    def patch(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make a PATCH request."""
        return self.request("PATCH", path, body, headers)

    def delete(self, path: str, headers: dict[str, str] | None = None) -> Any:
        """Make a DELETE request."""
        return self.request("DELETE", path, headers=headers)

    async def get_async(self, path: str, headers: dict[str, str] | None = None) -> Any:
        """Make an async GET request."""
        return await self.request_async("GET", path, headers=headers)

    async def post_async(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make an async POST request."""
        return await self.request_async("POST", path, body, headers)

    async def put_async(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make an async PUT request."""
        return await self.request_async("PUT", path, body, headers)

    async def patch_async(self, path: str, body: Any = None, headers: dict[str, str] | None = None) -> Any:
        """Make an async PATCH request."""
        return await self.request_async("PATCH", path, body, headers)

    async def delete_async(self, path: str, headers: dict[str, str] | None = None) -> Any:
        """Make an async DELETE request."""
        return await self.request_async("DELETE", path, headers=headers)

    def upload_file(
        self,
        path: str,
        file: bytes,
        filename: str,
        mime_type: str,
        additional_fields: dict[str, str] | None = None,
    ) -> Any:
        """Upload a file."""
        url = f"{self.base_url}{path}"

        request_headers: dict[str, str] = {}
        auth_header = self._get_auth_header()
        if auth_header:
            request_headers["Authorization"] = auth_header

        files = {"file": (filename, file, mime_type)}
        data = additional_fields or {}

        self._log(f"POST {path} [file upload: {filename}]")

        response = self._client.post(url, headers=request_headers, files=files, data=data)

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            response_data = response.json()
        else:
            response_data = response.text

        self._log(f"Response {response.status_code}", response_data)

        if not response.is_success:
            raise self._create_error(response.status_code, response_data)

        return response_data

    async def upload_file_async(
        self,
        path: str,
        file: bytes,
        filename: str,
        mime_type: str,
        additional_fields: dict[str, str] | None = None,
    ) -> Any:
        """Upload a file asynchronously."""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(timeout=self.timeout)

        url = f"{self.base_url}{path}"

        request_headers: dict[str, str] = {}
        auth_header = self._get_auth_header()
        if auth_header:
            request_headers["Authorization"] = auth_header

        files = {"file": (filename, file, mime_type)}
        data = additional_fields or {}

        self._log(f"POST {path} [file upload: {filename}]")

        response = await self._async_client.post(url, headers=request_headers, files=files, data=data)

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            response_data = response.json()
        else:
            response_data = response.text

        self._log(f"Response {response.status_code}", response_data)

        if not response.is_success:
            raise self._create_error(response.status_code, response_data)

        return response_data

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
        if self._async_client:
            # Note: For async client, use close_async() in async context
            pass

    async def close_async(self) -> None:
        """Close the async HTTP client."""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> "HttpClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close_async()
