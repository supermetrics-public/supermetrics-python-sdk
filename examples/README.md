# Supermetrics SDK - POC Examples

This directory contains examples demonstrating the complete Supermetrics SDK workflow for POC validation.

## Available Examples

### `complete_flow.py` - Synchronous Complete Workflow
Demonstrates the full customer onboarding flow from client initialization through authentication, account discovery, and data querying using the synchronous client.

### `async_flow.py` - Asynchronous Complete Workflow
Same workflow as `complete_flow.py` but using async/await for non-blocking operations.

## Prerequisites

1. **Python 3.11 or higher**
   ```bash
   python --version  # Should show 3.11+
   ```

2. **Supermetrics API key**
   - Copy your API key

## Setup

### 1. Install the SDK

```bash
pip install supermetrics-sdk
```

### 2. Set your API key

```bash
export SUPERMETRICS_API_KEY="your_api_key_here"
```

## Running the Examples

### Synchronous Example

```bash
python examples/complete_flow.py
```

### Asynchronous Example

```bash
python examples/async_flow.py
```

## What to Expect

When you run either example:

1. **Client initialized** - SDK client created
2. **Login link created** - You'll see a URL to visit
3. **Visit the URL** - Authenticate in your browser
4. **Authentication complete** - Script detects completion automatically
5. **Login details retrieved** - Username and data source info displayed
6. **Accounts discovered** - List of available accounts shown
7. **Query executed** - Data query runs for the first account
8. **Results displayed** - Sample data rows printed

**Typical execution time:** 1-6 minutes (mostly waiting for authentication)

### Example Output

```
✓ Client initialized
✓ Login link created: https://auth.supermetrics.com/...
  Link ID: link_abc123
  Status: OPEN

Please visit the login URL to authenticate your data source account.
After authentication, this script will continue automatically.

  Waiting for authentication... (0s elapsed)
✓ Authentication complete! Login ID: login_xyz789
✓ Login details retrieved:
  Username: user@example.com
  Data Source: Google Analytics 4

✓ Found 3 accounts:
  - My Website (ID: 12345678)
  - Mobile App (ID: 87654321)

✓ Query executed:
  Status: completed

Retrieved 7 rows
Sample data (first 5 rows):
  Row 1: {'Date': '2024-12-05', 'Sessions': '1234', 'Users': '567'}
  ...

✅ POC complete! All steps executed successfully.
```
