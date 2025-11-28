"""Shared pytest configuration and fixtures for supermetrics-sdk tests."""

import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session", autouse=True)
def add_src_to_path(project_root):
    """Add src directory to Python path for imports."""
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    yield
    # Cleanup
    if src_path in sys.path:
        sys.path.remove(src_path)


@pytest.fixture
def test_api_key() -> str:
    """Provide a test API key for testing.

    Returns:
        A test API key string.
    """
    return "test-api-key-12345"


@pytest.fixture
def expected_headers(test_api_key: str) -> dict[str, str]:
    """Provide expected default headers for testing.

    Args:
        test_api_key: The test API key fixture.

    Returns:
        Dictionary of expected HTTP headers.
    """
    # Note: Actual User-Agent will include version and Python version
    # This is a simplified version for basic testing
    return {
        "Authorization": f"Bearer {test_api_key}",
        # User-Agent is dynamic, so we'll test it separately
    }
