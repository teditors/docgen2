# Aerospace Hardware Test Report Generator

A Python-based tool for automatically generating aerospace hardware test reports from structured directory data.

## Overview

This application automates the creation of professional Word (.docx) test reports for aerospace hardware testing. It extracts data from a specified directory structure containing test logs, photographs, deviation notices, and data plots, and compiles them into a comprehensive report with proper formatting, styles, and structure.

## Features

- Automatically generates Word documents with proper styling and formatting
- Creates tables of contents, cross references, and section numbering
- Embeds images, PDFs (converted to images), and other data
- Organizes content into structured sections
- Supports multiple test types (Dynamics, EMIEMC, Environmental, or all)
- Includes standardized headers, footers, cover page, and end page
- Maintains proper document structure with consistent formatting

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`
- Poppler (for PDF to image conversion)

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install Poppler (required for PDF conversion):

On Ubuntu/Debian:
```bash
sudo apt-get install poppler-utils
```

On macOS:
```bash
brew install poppler
```

On Windows:
- Download the binaries from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- Add the `bin` directory to your PATH

## Usage

Run the script with the following command:

```bash
python main.py PD12345678 Dynamics
```

### Command-line Arguments

- `pd_number`: Project directory number (PD########)
- `test_type`: Type of test report to generate (Dynamics, EMIEMC, Environmental, or all)
- `--output-dir`: Output directory for the generated report (default: "reports")
- `--debug`: Enable debug logging

## Project Structure

```
├── main.py                   # Main script entry point
├── config.py                 # Configuration settings
├── report_generator.py       # Core report generation functionality
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── utils/                    # Utility modules
│   ├── __init__.py           # Package initialization
│   ├── docx_utils.py         # Document formatting utilities
│   ├── file_utils.py         # File operation utilities
│   └── logger.py             # Logging configuration
```

## Expected Directory Structure

The script expects the following directory structure:

```
testbed/
├── PD######## Company Name 1/ (project folder)
│   ├── admin/
│   │   ├── PO/
│   │   │   └── PO###### (PDF file)
│   │   ├── quotes/
│   │   │   └── Quote###### (PDF file)
│   │   └── specification/
│   │       └── spec###### (PDF file)
│   ├── testing/
│   │   ├── Dynamics/
│   │   │   └── PHB########/ (test folder)
│   │   │       ├── data/
│   │   │       │   └── ###_Description.jpg (data graphs)
│   │   │       ├── NODs/
│   │   │       │   └── NOD_mm.dd.yyyy.pdf (deviation notices)
│   │   │       ├── photographs/
│   │   │       │   └── photo_###_Component.jpeg (test photos)
│   │   │       └── worksheets/
│   │   │           └── TestLog_Component_TestProc_YYYYMMDD.pdf (test logs)
│   │   ├── EMIEMC/
│   │   └── Environmental/
│   └── receiving/
│       └── hardware_Component_####.jpeg (component photos)
```

## Report Structure

The generated report follows this structure:

1. **Cover Page**: Title, company information, signatures
2. **Administrative Information (1.0)**:
   - Units Under Test Table (1.1)
   - Tests Performed Table (1.2)
   - Details (1.3)
3. **Test Sections (2.0-N.0)** (one section per test):
   - Procedure (N.1)
   - Result (N.2)
   - Datasheets (N.3)
   - NODs (N.4)
   - Photographs (N.5)
   - Plots (N.6) - in landscape orientation
4. **End Page**: "END OF REPORT"

## Extending the Project

This project is designed to be extensible. Some areas for future enhancement:

1. Improved PDF parsing for better data extraction
2. Support for additional file formats
3. Integration with test databases
4. Generation of executive summaries
5. Customizable report templates
6. Integration with version control systems
7. Web interface for easier report generation
8. Support for multiple standards and specifications

## License

[Specify your license]
