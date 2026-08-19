# Supermetrics Python SDK Documentation

Complete documentation for the Supermetrics Python SDK – the Python client for Supermetrics API.

## Documentation Structure

### Core Documentation

| Document | Description |
|----------|-------------|
| [index.md](index.md) | Main documentation homepage with overview and quick start |
| [installation.md](installation.md) | Installation instructions and requirements |
| [usage.md](usage.md) | Quick usage overview and basic examples |

### Comprehensive Guides

| Guide | Description |
|-------|-------------|
| [authentication-and-transport.md](authentication-and-transport.md) | Credentials, dynamic token providers, per-request overrides, response metadata, and the error taxonomy |
| [user-guide.md](user-guide.md) | Complete tutorials covering authentication, querying, async support, and best practices |
| [api-reference.md](api-reference.md) | Full API documentation for all client classes, resources, models, and exceptions |
| [error-handling.md](error-handling.md) | Error handling patterns, common scenarios, and production best practices |
| [openapi-generation.md](openapi-generation.md) | Guide to filtering OpenAPI specs, regenerating client code, and writing resource adapters |

## Quick Navigation

### For New Users

1. Start with [Installation](installation.md) to set up the SDK
2. Read [Usage](usage.md) for a quick introduction
3. Follow the [User Guide](user-guide.md) for comprehensive tutorials
4. Read [Authentication & Transport](authentication-and-transport.md) before wiring the SDK into a multi-tenant service
5. Refer to [API Reference](api-reference.md) as needed

### For Experienced Users

- [API Reference](api-reference.md) - Quick lookup for methods and parameters
- [Error Handling](error-handling.md) - Production error handling patterns
- [Authentication & Transport](authentication-and-transport.md) - Per-request credentials, tracing headers, timeouts, and raw responses
- [Examples](https://github.com/supermetrics-public/SuperPy-SDK/tree/main/examples) - Working code examples

## Documentation Topics

### Client Classes
- [SupermetricsClient](api-reference.md#supermetricsclient) - Synchronous client
- [SupermetricsAsyncClient](api-reference.md#supermetricsasyncclient) - Asynchronous client

### Resources
- [LoginLinksResource](api-reference.md#loginlinksresource) - Manage authentication links
- [LoginsResource](api-reference.md#loginsresource) - Retrieve login credentials
- [AccountsResource](api-reference.md#accountsresource) - List data source accounts
- [QueriesResource](api-reference.md#queriesresource) - Execute data queries
- [BackfillsResource](api-reference.md#backfillsresource) - Backfill historical data
- [DatasourceDetailsResource](api-reference.md#datasourcedetailsresource) - Inspect data source connections
- [DestinationsResource](api-reference.md#destinationsresource) - Manage Data Warehouse destinations
- [TransfersResource](api-reference.md#transfersresource) - Manage Data Warehouse transfers
- [TransferRunsResource](api-reference.md#transferrunsresource) - Inspect individual transfer runs
- [CustomFieldsResource](api-reference.md#customfieldsresource) - Define calculated dimensions and metrics

### Error Handling
- [Exception Hierarchy](error-handling.md#exception-hierarchy)
- [AuthenticationError](error-handling.md#authenticationerror)
- [ValidationError](error-handling.md#validationerror)
- [APIError](error-handling.md#apierror)
- [NetworkError](error-handling.md#networkerror)

### Advanced Topics
- [Async Support](user-guide.md#async-support) - High-performance async operations
- [Best Practices](user-guide.md#best-practices) - Production-ready patterns
- [Common Data Sources](user-guide.md#common-data-sources) - Data source-specific examples

## Examples

All documentation includes practical examples. For complete working code, see the [examples](https://github.com/supermetrics-public/SuperPy-SDK/tree/main/examples) directory:

- `complete_flow.py` - Full sync workflow
- `async_flow.py` - Full async workflow

## Contributing

See [Contributing](https://github.com/supermetrics-public/SuperPy-SDK/blob/main/CONTRIBUTING.md) for guidelines on contributing to the documentation or SDK.

## Version History

## External Resources

- [Supermetrics API Documentation](https://supermetrics.com/docs/)
- [Supermetrics Field Reference](https://supermetrics.com/docs/product-fields/)
- [GitHub Repository](https://github.com/supermetrics-public/supermetrics-python-sdk)
- [PyPI Package](https://pypi.org/project/supermetrics/)

## Support

For questions and issues:
1. Check this documentation first
2. Review the [examples](https://github.com/supermetrics-public/SuperPy-SDK/tree/main/examples) directory
3. Search existing [GitHub issues](https://github.com/supermetrics-public/supermetrics-python-sdk/issues)
4. Create a new issue if needed

## License

Apache License v2 - See LICENSE file for details
