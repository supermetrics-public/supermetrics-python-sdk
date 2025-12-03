"""Resource adapters for Supermetrics API.

This package contains hand-written resource adapters that provide a stable,
Pythonic interface to the Supermetrics API. These adapters wrap the
auto-generated code in _generated/ to provide:

- Stable public API that won't break on OpenAPI regeneration
- Clean, intuitive method signatures
- Comprehensive error handling
- Complete type safety with IDE autocomplete support
"""

from supermetrics.resources.login_links import LoginLinksAsyncResource, LoginLinksResource

__all__ = [
    "LoginLinksResource",
    "LoginLinksAsyncResource",
]
