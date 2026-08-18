"""Shared pytest configuration and fixtures for supermetrics-sdk tests."""

import os
import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).parent.parent


def _load_dotenv(path: Path) -> None:
    """Load ``KEY=value`` pairs from a local ``.env`` file into the environment.

    Only the live smoke tests in ``tests/e2e/test_live_smoke.py`` read anything from
    the environment; every other test is hermetic. This runs at import time so the
    values are in place before test modules are collected.

    Real environment variables always win, so ``SUPERMETRICS_API_KEY=... pytest``
    and CI secrets override whatever is in the file. Deliberately dependency-free:
    the SDK has no runtime dependency on python-dotenv and the test suite should
    not add one for a dozen lines of parsing.

    Args:
        path: The ``.env`` file to read. Missing files are ignored.
    """
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(_PROJECT_ROOT / ".env")


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
