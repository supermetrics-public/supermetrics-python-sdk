"""Guard tests that keep the dedicated end-to-end CI job honest.

`.github/workflows/sdk-lint-test.yml` runs a separate ``e2e`` job as
``pytest tests/e2e -m e2e``, so that job only ever runs the modules carrying the
``e2e`` marker. Pytest is not configured with ``--strict-markers`` and nothing
applies the marker by directory, so a new ``tests/e2e/test_*.py`` that forgets or
misspells ``pytestmark = pytest.mark.e2e`` is silently *deselected* there while
still running under the broader ``test`` job: the build stays green while
covering less than it appears to, and no existing test notices.

These tests notice. They read each module's ``pytestmark`` attribute — the same
thing pytest itself reads when applying module-level marks — and fail by name on
any module that is not opted in.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType

import pytest

pytestmark = pytest.mark.e2e

#: Modules in ``tests/e2e/`` that are deliberately *not* marked ``e2e``.
#:
#: ``test_live_smoke.py`` is marked ``live``: it calls the production API and
#: self-skips without credentials, so it must stay out of the hermetic job.
#:
#: Exemptions are listed here by name, in writing, so that every hole in the
#: dedicated job's coverage is a visible decision rather than an omission that
#: looks exactly like a bug.
MARKER_EXEMPT: frozenset[str] = frozenset({"test_live_smoke.py"})

#: Floor on how many modules discovery must find. Without it, a glob that stops
#: matching anything would make the marker check pass vacuously — the same trap
#: ``tests/test_api_parity.py`` guards against with its resource-count floor.
#:
#: Keep this at the real module count. A floor left trailing well behind it still
#: catches a glob that matches *nothing*, but not one that has quietly stopped
#: matching half the directory — which is the same blind spot in a smaller size.
MINIMUM_MODULES = 17

#: The directory this guard polices: the one it lives in.
E2E_DIR = Path(__file__).parent


def _module_paths() -> list[Path]:
    """Return every ``test_*.py`` in ``tests/e2e/``, sorted for stable messages."""
    return sorted(E2E_DIR.glob("test_*.py"))


def _marker_names(module: ModuleType) -> set[str]:
    """Return the names of the marks in a module's ``pytestmark``.

    ``pytestmark`` is either a single mark or a sequence of them; both forms are
    normalised here so the caller can just ask whether ``"e2e"`` is present.
    """
    declared = getattr(module, "pytestmark", [])
    marks = list(declared) if isinstance(declared, list | tuple) else [declared]
    return {getattr(mark, "name", "") for mark in marks}


class TestE2EMarkerCoverage:
    """Every hermetic module under ``tests/e2e/`` opts into the dedicated CI job."""

    def test_every_module_declares_the_e2e_marker(self) -> None:
        """An e2e module without the marker fails the build and is named in the message."""
        unmarked: list[str] = []
        for path in _module_paths():
            if path.name in MARKER_EXEMPT:
                continue
            module = importlib.import_module(f".{path.stem}", package=__package__)
            if "e2e" not in _marker_names(module):
                unmarked.append(path.name)

        assert not unmarked, (
            "These tests/e2e modules do not declare `pytestmark = pytest.mark.e2e`, so the "
            "dedicated CI job (`pytest tests/e2e -m e2e`) silently skips them while the "
            f"broader test job still runs them: {', '.join(unmarked)}. Add the marker "
            "immediately after the imports, or add the file to MARKER_EXEMPT with a comment "
            "explaining why it is exempt."
        )

    def test_discovery_finds_the_whole_directory(self) -> None:
        """A broken glob cannot make the marker check pass by finding nothing."""
        discovered = [path.name for path in _module_paths()]

        assert len(discovered) >= MINIMUM_MODULES, (
            f"Only {len(discovered)} e2e module(s) discovered in {E2E_DIR} "
            f"({', '.join(discovered) or 'none'}), below the floor of {MINIMUM_MODULES}. "
            "Either discovery is broken — which would make the marker check vacuous — or "
            "modules were removed and MINIMUM_MODULES needs revisiting."
        )
