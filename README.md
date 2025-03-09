# Aerospace Test Directory Generator

This tool generates a realistic directory structure for aerospace hardware testing data, including engineering results and business paperwork.

## Features

- Creates a structured folder hierarchy for multiple aerospace testing projects
- Generates realistic project names with aerospace company naming conventions
- Builds consistent themes throughout each project (e.g., rocket engines, satellites, landing gear)
- Creates business documents like purchase orders, quotes, and specifications as PDFs
- Generates simulated test data graphs that are relevant to the test types
- Creates dummy photographs with correct orientations
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
│   └── testing/
│       ├── Dynamics/
│       │   └── PHB########/
│       │       ├── data/
│       │       │   └── ###_Description.jpg (data graphs)
│       │       ├── NODs/
│       │       │   └── NOD_mm.dd.yyyy.pdf (deviation notices)
│       │       ├── photographs/
│       │       │   └── photo_###_Component.jpeg (test photos)
│       │       └── worksheets/
│       ├── EMIEMC/
│       └── Environmental/
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
  --projects PROJECTS   Number of project folders to create. Default is 10.
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

## Extending the Generator

The modular design makes it easy to extend the generator:

- Add new themes in `config.py`
- Create new document types in `pdf_generator.py`
- Add different test types in `config.py`
- Implement new file generators in `directory_generator.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
