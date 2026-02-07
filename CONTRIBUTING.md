# Contributing to Authensure Python SDK

Thank you for your interest in contributing to the Authensure Python SDK! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository**

   Click the "Fork" button on the [GitHub repository](https://github.com/Authensure/authensure-python).

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/authensure-python.git
   cd authensure-python
   ```

3. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

5. **Verify setup**

   ```bash
   pytest
   ```

## Development Workflow

### Creating a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Making Changes

1. **Write tests first** (TDD approach)
   - Add tests for new functionality
   - Ensure existing tests still pass

2. **Implement your changes**
   - Follow the existing code style
   - Add type hints to all functions
   - Document public APIs with docstrings

3. **Run the test suite**

   ```bash
   pytest
   ```

4. **Check code quality**

   ```bash
   # Type checking
   mypy src/authensure
   
   # Linting
   ruff check src/authensure
   
   # Auto-fix linting issues
   ruff check --fix src/authensure
   ```

### Code Style Guidelines

- **Type Hints**: All functions must have complete type annotations
- **Docstrings**: Use Google-style docstrings for all public methods
- **Line Length**: Maximum 100 characters
- **Imports**: Use absolute imports, sorted with `isort`
- **Naming**: 
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `SCREAMING_SNAKE_CASE` for constants

### Example Code Style

```python
from typing import Any

from authensure.types import Envelope


class EnvelopesResource:
    """Resource for envelope operations."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http

    def create(
        self,
        name: str,
        message: str | None = None,
    ) -> Envelope:
        """
        Create a new envelope.

        Args:
            name: The envelope name.
            message: Optional message for recipients.

        Returns:
            The created envelope.

        Raises:
            ValidationError: If the name is empty.
            AuthenticationError: If authentication fails.
        """
        body: dict[str, Any] = {"name": name}
        if message:
            body["message"] = message
        data = self._http.post("/envelopes", body)
        return Envelope.model_validate(data)
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use pytest fixtures from `conftest.py`
- Mock external API calls using `respx`

Example test:

```python
import pytest
import respx
from httpx import Response

from authensure import Authensure, Envelope


class TestEnvelopesResource:
    def test_create_envelope(self, client: Authensure, mock_api, sample_envelope: dict):
        """Test creating an envelope."""
        mock_api.post("/envelopes").mock(
            return_value=Response(201, json=sample_envelope)
        )
        
        envelope = client.envelopes.create(name="Test Envelope")
        
        assert isinstance(envelope, Envelope)
        assert envelope.name == "Test Envelope"
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add template marketplace support

- Add get_marketplace() method to TemplatesResource
- Add add_marketplace_template() method
- Add tests for marketplace functionality
```

Prefixes:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `chore:` Build/tooling changes

### Submitting a Pull Request

1. **Push your changes**

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

3. **PR Requirements**

   - All tests must pass
   - Code must be properly typed (mypy)
   - Code must pass linting (ruff)
   - Documentation must be updated if needed
   - At least one maintainer review required

## Reporting Issues

### Bug Reports

Include:
- Python version
- SDK version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

### Feature Requests

Include:
- Use case description
- Proposed API design
- Any relevant examples

## Questions?

- Open a GitHub Discussion
- Email: support@authensure.app

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Authensure! 🎉
