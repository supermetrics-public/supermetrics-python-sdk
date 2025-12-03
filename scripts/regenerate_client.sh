#!/bin/bash
set -e

echo "🔄 Regenerating Supermetrics SDK from OpenAPI specification..."

# Remove old generated code
echo "📁 Removing old generated code..."
rm -rf src/supermetrics/_generated

# Generate new code
echo "⚙️  Generating new SDK code..."
openapi-python-client generate \
  --path openapi-spec.yaml \
  --output-path src/supermetrics/_generated

# Verify generation succeeded
if [ ! -d "src/supermetrics/_generated/supermetrics_api_client" ]; then
  echo "❌ Error: SDK generation failed - supermetrics_api_client directory not found"
  exit 1
fi

echo "✓ SDK regenerated successfully"
echo ""
echo "📝 Next steps:"
echo "   1. Review generated code in src/supermetrics/_generated/"
echo "   2. Run tests to verify compatibility: pytest tests/"
echo "   3. Check for any breaking changes in API endpoints"
echo ""
echo "✅ Regeneration complete!"
