# Aerospace Test Directory Generator

This tool generates a realistic directory structure for aerospace hardware testing data, including engineering results and business paperwork.

## Features

- Creates a comprehensive folder hierarchy for multiple aerospace testing projects
- Generates realistic project names with aerospace company naming conventions
- Builds consistent themes throughout each project (e.g., rocket engines, satellites, landing gear)
- Creates detailed business documents as PDFs:
  - Purchase orders with technical requirements and procurement details
  - Quotes with pricing breakdowns and delivery schedules
  - Technical specifications with comprehensive requirements
  - Notices of Deviation (NODs) with technical justifications
- Produces test logs with realistic test procedures and measurements
- Generates realistic hardware photographs specific to each component type
- Creates simulated test data graphs that are relevant to the test types
- Maintains comprehensive logging for all operations

## Directory Structure

The generator creates the following structure:

```
testbed/
├── PD######## Company Name 1/
│   ├── admin/
│   │   ├── PO/
│   │   │   └── PO###### (PDF file)
│   │   ├── quotes/
│   │   │   └── Quote###### (PDF file)
│   │   └── specification/
│   │       └── spec###### (PDF file)
│   ├── testing/
│   │   ├── Dynamics/
│   │   │   └── PHB########/
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
├── PD######## Company Name 2/
...
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/aerospace-test-directory-generator.git
cd aerospace-test-directory-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the generator with default settings:

```bash
python main.py
```

This will create a `testbed` directory in the current folder with 10 randomly generated aerospace test projects.

### Command Line Options

```
usage: main.py [-h] [--output-dir OUTPUT_DIR] [--projects PROJECTS] [--seed SEED]
               [--log-file LOG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--verbose] [--themes THEMES]

Generate a realistic aerospace test directory structure.

optional arguments:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Output directory for the test structure. Defaults to "testbed" in the current directory.
  --output-format OUTPUT_FORMAT
                        Output format for document artifacts.  Default is 'pdf'
  --projects PROJECTS   Number of project folders to create. Default is 5.
  --seed SEED           Random seed for reproducible generation.
  --log-file LOG_FILE   Path to the log file. Defaults to "generator_TIMESTAMP.log" in the script directory.
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level for console output. Default is INFO.
  --verbose             Enable verbose output.
  --themes THEMES       Comma-separated list of theme indices to use (0-9). Default is all themes.
```

### Examples

Generate 5 projects with a specific seed for reproducibility:
```bash
python main.py --projects 5 --seed 12345
```

Generate projects with only specific themes (rocket engines and avionics):
```bash
python main.py --themes 0,3
```

Change the output directory:
```bash
python main.py --output-dir ~/aerospace_data
```

Change the output format for document artifacts:
```bash
python main.py --output-format png
```

## Project Themes

The generator includes the following aerospace test themes:

1. Rocket Engine
2. Satellite Solar Panel
3. Landing Gear
4. Avionics System
5. Fuel Tank
6. Heat Shield
7. Control Surface
8. Propellant Valve
9. Payload Fairing
10. Docking Mechanism

Each theme has its own set of components, test procedures, and data types to ensure consistency within projects.

## Modules Overview

The project consists of several modules:

- **main.py**: Main entry point with command-line argument parsing
- **config.py**: Configuration settings for the generator
- **logger.py**: Logging setup and configuration
- **directory_generator.py**: Main directory structure creation
- **pdf_generator.py**: PDF document generation for POs, quotes, specs, etc.
- **test_log_generator.py**: Generation of test log PDFs
- **hardware_image_generator.py**: Interface for hardware image generation
- **hardware_generator_main.py**: Main implementation of hardware image generation
- **component_drawers_1.py** & **component_drawers_2.py**: Component-specific drawing functions
- **hardware_image_config.py**: Configuration for hardware images
- **drawer_utils.py**: Utilities for drawing operations
- **utility_functions.py**:Utility functions for the test directory generator

## Extending the Generator

The modular design makes it easy to extend the generator:

- Add new themes in `config.py`
- Create new document types in `pdf_generator.py`
- Add different test types in `config.py`
- Implement new file generators in `directory_generator.py`
- Add new hardware component types in `hardware_image_config.py`
- Create drawing functions for new components in component drawer modules

## Error Handling

The generator includes comprehensive error handling:
- Path sanitization to handle special characters
- Try/except blocks to prevent crashes from individual file operations
- Detailed logging of all operations and errors
- Safe file operation decorators

## License

This project is licensed under the MIT License - see the LICENSE file for details.
