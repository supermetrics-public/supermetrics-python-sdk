# Supermetrics Python SDK Setup Guide

This guide explains how to set up a test project to use the Supermetrics Python SDK.

## Directory Structure

Your workspace should look like this:

```
workspace/
├── supermetrics-python-sdk/  # SDK repository (this repo)
│   ├── src/
│   ├── examples/
│   │   └── complete_flow.py
│   ├── ...
│
└── SDK-POC/                  # Your test project
    ├── .venv/                # Virtual environment
    ├── .env                  # API key configuration (optional)
    ├── complete_flow.py      # Copied example
    └── ...                   # Your custom scripts
```

## Setup Instructions

### 1. Clone the SDK Repository

Clone the supermetrics-python-sdk repository in your workspace

### 2. Create Your Test Project

Create a new folder at the same level as the SDK

### 3. Create and Activate Virtual Environment

Go to the root folder of your POC (e.g., SDK-POC):

Using Python 3.13 (or your preferred version):

```bash
# Create virtual environment
/opt/homebrew/bin/python3.13 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 4. Install Dependencies

Install the SDK in editable mode and required packages:

```bash
pip install -e ../supermetrics-python-sdk
pip install python-dotenv
```

### 5. Copy the Example File

```bash
cp ../supermetrics-python-sdk/examples/complete_flow.py complete_flow.py
```

### 6. Run the Example

#### Option A: Manual API Key Entry (Default)

Simply run the example, and it will prompt you for the API key:

```bash
python3.13 complete_flow.py
```

#### Option B: Using Environment Variable (Recommended)

1. Create a `.env` file in the SDK-POC root:

```bash
echo "SUPERMETRICS_API_KEY=YOUR_API_KEY_HERE" > .env
```

2. Edit `complete_flow.py` and modify the API key handling:

**Uncomment lines 52-54:**
```python
api_key = os.getenv("SUPERMETRICS_API_KEY")
if not api_key:
    raise ValueError("SUPERMETRICS_API_KEY environment variable is required")
```

**Comment out lines 56-57:**
```python
# api_key = getpass("Enter your API key: ")
# print("API key received.")
```

3. Run the example:

```bash
python3.13 complete_flow.py
```

