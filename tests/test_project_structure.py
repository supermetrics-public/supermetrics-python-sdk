"""Tests for Story 1.1: Initialize Python Project Structure.

This module validates all acceptance criteria for the project initialization story.
"""

import sys
import tomllib
from pathlib import Path

import pytest

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class TestAcceptanceCriteria1:
    """AC1: Repository created with .gitignore, LICENSE (Apache 2.0), and README.md skeleton."""

    def test_gitignore_exists(self):
        """Verify .gitignore exists and contains Python-specific ignores."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        assert gitignore_path.exists(), ".gitignore file must exist"

        content = gitignore_path.read_text()
        # Check for required patterns (accepting common variants)
        assert "__pycache__" in content, ".gitignore must contain '__pycache__'"
        assert ".venv" in content or "venv/" in content, ".gitignore must contain venv pattern"
        assert "*.pyc" in content or "*.py[cod]" in content or "*.py[codz]" in content, \
            ".gitignore must contain compiled Python file pattern"
        assert "*.egg-info" in content or ".egg-info/" in content, \
            ".gitignore must contain egg-info pattern"

    def test_license_exists(self):
        """Verify LICENSE file exists and contains Apache 2.0 license text."""
        license_path = PROJECT_ROOT / "LICENSE"
        assert license_path.exists(), "LICENSE file must exist"

        content = license_path.read_text()
        assert "Apache License" in content or "Apache-2.0" in content, \
            "LICENSE must contain Apache 2.0 license text"
        assert "Version 2.0" in content or "2.0" in content, \
            "LICENSE must specify version 2.0"

    def test_readme_exists(self):
        """Verify README.md exists with project title and basic structure."""
        readme_path = PROJECT_ROOT / "README.md"
        assert readme_path.exists(), "README.md file must exist"

        content = readme_path.read_text()
        assert len(content) > 0, "README.md must not be empty"
        # Check for project name or SDK reference
        assert "supermetrics" in content.lower() or "sdk" in content.lower(), \
            "README.md should mention project name or SDK"


class TestAcceptanceCriteria2:
    """AC2: pyproject.toml configured with project metadata, dependencies, and build system."""

    @pytest.fixture
    def pyproject_data(self):
        """Load and parse pyproject.toml."""
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml must exist"
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)

    def test_build_system_hatchling(self, pyproject_data):
        """Parse pyproject.toml and verify build-system.build-backend = 'hatchling.build'."""
        assert "build-system" in pyproject_data, "pyproject.toml must have [build-system]"
        build_system = pyproject_data["build-system"]
        assert build_system["build-backend"] == "hatchling.build", \
            "Build backend must be hatchling.build"
        assert "hatchling" in build_system["requires"], \
            "Build system must require hatchling"

    def test_project_metadata(self, pyproject_data):
        """Verify project.name, project.version, project.description in pyproject.toml."""
        assert "project" in pyproject_data, "pyproject.toml must have [project] section"
        project = pyproject_data["project"]

        # Verify name is 'supermetrics'
        assert "name" in project, "project.name must be defined"
        assert project["name"].lower() == "supermetrics", \
            "project.name must be 'supermetrics'"

        # Version can be static or dynamic (via versioningit)
        dynamic = project.get("dynamic", [])
        if "version" in dynamic:
            # Version is dynamic, verify versioningit is configured
            hatch_version = pyproject_data.get("tool", {}).get("hatch", {}).get("version", {})
            assert hatch_version.get("source") == "versioningit", \
                "Dynamic version must use versioningit as source"
        else:
            assert project.get("version") == "0.1.0", "project.version must be 0.1.0"

        assert "description" in project, "project.description must be defined"
        assert len(project["description"]) > 0, "project.description must not be empty"

    def test_runtime_dependencies(self, pyproject_data):
        """Verify all 4 runtime dependencies present with correct version constraints."""
        project = pyproject_data["project"]
        dependencies = project.get("dependencies", [])

        required_deps = {
            "httpx": ">=0.25.0",
            "pydantic": ">=2.0.0",
            "python-dateutil": ">=2.8.0",
            "attrs": ">=23.0.0",
        }

        for dep_name, min_version in required_deps.items():
            # Find dependency in list (format: "package>=version")
            found = False
            for dep in dependencies:
                if dep_name in dep.lower():
                    found = True
                    assert ">=" in dep or "==" in dep, \
                        f"{dep_name} must have version constraint"
                    break
            assert found, f"Required dependency '{dep_name}' must be present"

    def test_dev_dependencies(self, pyproject_data):
        """Verify all 6 dev dependencies present in [project.optional-dependencies.dev]."""
        project = pyproject_data["project"]
        optional_deps = project.get("optional-dependencies", {})
        dev_deps = optional_deps.get("dev", [])

        required_dev_deps = [
            "openapi-python-client",
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "ruff",
            "mypy",
        ]

        for dep_name in required_dev_deps:
            found = any(dep_name in dep.lower() for dep in dev_deps)
            assert found, f"Required dev dependency '{dep_name}' must be present"


class TestAcceptanceCriteria3:
    """AC3: Project structure created with required directories."""

    def test_src_supermetrics_exists(self):
        """Verify src/supermetrics/ directory exists."""
        src_path = PROJECT_ROOT / "src" / "supermetrics"

        assert src_path.exists(), \
            "src/supermetrics/ or src/supermetrics/ directory must exist"

    def test_init_file_exists(self):
        """Verify src/supermetrics/__init__.py exists."""
        init_paths = [
            PROJECT_ROOT / "src" / "supermetrics" / "__init__.py",
        ]
        found = any(p.exists() for p in init_paths)
        assert found, "__init__.py must exist in package directory"

    def test_version_file_exists(self):
        """Verify src/supermetrics/__version__.py exists and defines __version__."""
        version_paths = [
            PROJECT_ROOT / "src" / "supermetrics" / "__version__.py",
        ]

        version_path = None
        for p in version_paths:
            if p.exists():
                version_path = p
                break

        assert version_path is not None, "__version__.py must exist"

        content = version_path.read_text()
        assert "__version__" in content, "__version__.py must define __version__"
        assert "0.1.0" in content, "__version__ should be '0.1.0'"

    def test_required_directories_exist(self):
        """Verify tests/, examples/, docs/, scripts/ directories exist."""
        required_dirs = ["tests", "examples", "docs", "scripts"]

        for dir_name in required_dirs:
            dir_path = PROJECT_ROOT / dir_name
            assert dir_path.exists(), f"{dir_name}/ directory must exist"
            assert dir_path.is_dir(), f"{dir_name} must be a directory"


class TestAcceptanceCriteria4:
    """AC4: Python 3.11+ compatibility verified."""

    def test_python_version_3_11_plus(self):
        """Verify python --version returns 3.11+."""
        assert sys.version_info >= (3, 11), \
            f"Python version must be 3.11 or higher (current: {sys.version_info.major}.{sys.version_info.minor})"

    def test_requires_python_setting(self):
        """Verify pyproject.toml has requires-python = '>=3.11'."""
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        requires_python = data["project"].get("requires-python")
        assert requires_python is not None, "requires-python must be set"
        assert "3.11" in requires_python, "requires-python must specify 3.11"
        assert ">=" in requires_python or "==" in requires_python, \
            "requires-python must have version constraint"

    def test_import_supermetrics(self):
        """Verify import supermetrics succeeds."""
        # Add src to path
        src_path = PROJECT_ROOT / "src"
        sys.path.insert(0, str(src_path))

        try:
            import supermetrics
            assert hasattr(supermetrics, "__version__"), \
                "Package must export __version__"
        finally:
            # Clean up sys.path
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))


class TestAcceptanceCriteria5:
    """AC5: Git repository initialized with initial commit."""

    def test_git_directory_exists(self):
        """Verify .git directory exists."""
        git_path = PROJECT_ROOT / ".git"
        assert git_path.exists(), ".git directory must exist"
        assert git_path.is_dir(), ".git must be a directory"

    def test_git_has_commits(self):
        """Verify git log shows at least one commit."""
        import subprocess

        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "git log command must succeed"
        assert len(result.stdout.strip()) > 0, "Git repository must have at least one commit"
