# AWS WAF Challenge Bypass Tool

A Python tool designed to bypass AWS WAF challenges and perform brute force login attempts.

## Features

- Automatically solves AWS WAF challenges using Playwright
- Handles cookie management and session persistence
- Supports custom email and password lists
- Rate limiting and request throttling
- Detailed logging of attempts and responses

## Prerequisites

- Python 3.7+
- Playwright
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install required packages:

```bash
pip install -r requirements.txt
playwright install chromium
```

3. Run the script:

```bash
python main.py
```

## Usage

- Configure the target URL, email list, and password list in the script.
- Run the script to start the brute force login attempts.
- The tool will automatically solve any WAF challenges and attempt logins.
- Detailed logs will be generated in the console.

## Notes

- This tool is designed for educational purposes and should be used responsibly.
- Always ensure you have permission to test the target application.
- Consider adding error handling and user feedback for a better user experience.
