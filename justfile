# Justfile for supermetrics

# Show available commands
list:
    @just --list

# Format code with ruff
format:
    uv run --extra dev ruff format .

# Lint code with ruff (auto-fix safe issues)
lint:
    uv run --extra dev ruff check . --fix

# Run type checking with mypy
typecheck:
    uv run --extra dev mypy src/supermetrics --ignore-missing-imports

# Run all the formatting, linting, and testing commands
qa: format lint typecheck
    uv run --extra dev pytest .

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.11 --extra dev pytest
    uv run --python=3.12 --extra dev pytest
    uv run --python=3.13 --extra dev pytest
    uv run --python=3.14 --extra dev pytest

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --extra dev pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --extra dev pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb {{ARGS}}

# Run coverage, and build to HTML
coverage:
    uv run --extra dev coverage run -m pytest .
    uv run --extra dev coverage report -m
    uv run --extra dev coverage html

# Build the project, useful for checking that packaging is correct
build:
    rm -rf build
    rm -rf dist
    uv build

VERSION := `grep -m1 '^version' pyproject.toml | sed -E 's/version = "(.*)"/\1/'`

# Print the current version of the project
version:
    @echo "Current version is {{VERSION}}"

# Tag the current version in git and push to github
tag:
    echo "Tagging version v{{VERSION}}"
    git tag -a v{{VERSION}} -m "Creating version v{{VERSION}}"
    git push origin v{{VERSION}}

# Remove all build, test, coverage and Python artifacts
clean:
    rm -fr build/ dist/ .eggs/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +
    rm -f .coverage
    rm -fr htmlcov/
    rm -fr .pytest_cache
