#!/bin/bash
#
# Regenerate src/supermetrics/_generated/ from the merged openapi-spec.yaml.
#
# Two things about this script are deliberate and worth keeping.
#
# 1. It generates into a temporary directory and only replaces the committed tree
#    once the generator has succeeded. An earlier version deleted _generated/ first
#    and generated second, so any generator failure left the repository with no
#    client at all.
#
# 2. It runs the generator through `uvx` on a pinned interpreter rather than through
#    the project virtualenv. openapi-python-client 0.29.0 pulls in a pydantic that
#    raises `AssertionError` in `_typing_extra.eval_type_backport` under Python 3.14,
#    which is this project's default interpreter. `uvx` keeps that constraint in a
#    throwaway environment instead of pinning the whole project down to 3.12.
#
set -euo pipefail

cd "$(dirname "$0")/.."

SPEC="openapi-spec.yaml"
CONFIG="openapi-python-client-config.yaml"
TARGET="src/supermetrics/_generated"

# Keep the generator version tied to the dev dependency so the two cannot drift.
GENERATOR_VERSION="$(sed -n 's/.*"openapi-python-client==\([^"]*\)".*/\1/p' pyproject.toml | head -1)"
if [ -z "$GENERATOR_VERSION" ]; then
  echo "❌ Error: could not read the openapi-python-client pin from pyproject.toml" >&2
  exit 1
fi

# Interpreter the generator itself runs on. See note 2 above.
GENERATOR_PYTHON="${GENERATOR_PYTHON:-3.12}"

echo "🔄 Regenerating Supermetrics SDK from $SPEC..."
echo "   generator: openapi-python-client==$GENERATOR_VERSION on Python $GENERATOR_PYTHON"

STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT

echo "⚙️  Generating into a staging directory..."
uvx --python "$GENERATOR_PYTHON" --from "openapi-python-client==$GENERATOR_VERSION" \
  openapi-python-client generate \
  --path "$SPEC" \
  --output-path "$STAGING/_generated" \
  --config "$CONFIG"

if [ ! -d "$STAGING/_generated/supermetrics_api_client" ]; then
  echo "❌ Error: SDK generation failed - supermetrics_api_client directory not found" >&2
  echo "   The committed tree in $TARGET has been left untouched." >&2
  exit 1
fi

# The generated project scaffolding is not part of the SDK.
rm -f "$STAGING/_generated/pyproject.toml"

echo "📁 Replacing $TARGET..."
rm -rf "$TARGET"
mv "$STAGING/_generated" "$TARGET"

echo "✓ SDK regenerated successfully"
echo ""
echo "📝 Next steps:"
echo "   1. Review the diff: git diff --stat $TARGET"
echo "      A change that adds endpoints should be additions only."
echo "   2. Run the tests: just test"
echo "   3. Wrap any new endpoints in src/supermetrics/resources/"
echo ""
echo "✅ Regeneration complete!"
