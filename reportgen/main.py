#!/usr/bin/env python3
"""
Aerospace Hardware Test Report Generator

This script automatically generates Word (.docx) test reports from files in a structured directory.
It produces professional reports with proper styling, TOC, cross-references, and section numbering.
"""

import argparse
import os
import sys
import time
from pathlib import Path

from config import settings
from report_generator import ReportGenerator
from utils.file_utils import validate_project_directory
from utils.logger import setup_logger, log_system_info


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate aerospace hardware test reports.")
    parser.add_argument("pd_number", nargs='?', help="Project directory number (PD########)")
    parser.add_argument(
        "test_type",
        nargs='?',
        choices=["Dynamics", "EMIEMC", "Environmental", "all"],
        help="Type of test report to generate",
    )
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--log-dir", help="Directory for log files")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose console output")
    parser.add_argument("--system-info", action="store_true", help="Log system information")
    return parser.parse_args()

def get_user_input():
    """Prompt user for required inputs when not provided via command line."""
    print("No command-line arguments provided. Please enter the required information:")
    
    # Prompt for pd_number
    pd_number = input("Enter pd_number: ")
    
    # Prompt for test_type with options
    print("\nSelect test_type:")
    print("1. Dynamics")
    print("2. EMIEMC")
    print("3. Environmental")
    print("4. all")
    
    test_type_option = input("Enter option number (1-4): ")
    
    # Map option number to test_type
    test_type_map = {
        "1": "Dynamics",
        "2": "EMIEMC",
        "3": "Environmental",
        "4": "all"
    }
    
    if test_type_option in test_type_map:
        test_type = test_type_map[test_type_option]
    else:
        print("Invalid option. Defaulting to 'all'.")
        test_type = "all"
    
    return pd_number, test_type

def main():
    """Main function to run the report generator."""
    # Start timing
    start_time = time.time()
    
    args = parse_arguments()
    
    # If required arguments are missing, get them from user input
    if args.pd_number is None or args.test_type is None:
        pd_number, test_type = get_user_input()
        
        # Update args with user input
        args.pd_number = pd_number
        args.test_type = test_type
    
    # Set default output directory if not provided
    if args.output_dir is None:
        output_dir = Path(settings.DEFAULT_OUTPUT_DIR)
    else:
        output_dir = Path(args.output_dir)
    
    # Setup logging
    log_level = "DEBUG" if args.debug else "INFO"
    console_level = "DEBUG" if args.verbose else log_level
    logger = setup_logger(
        level=log_level, 
        log_dir=args.log_dir, 
        log_prefix=f"report_gen_PD{args.pd_number}",
        console_level=console_level
    )
    
    # Log system information if requested
    if args.system_info:
        log_system_info(logger)
    
    # Now proceed with the original functionality
    logger.info(f"Starting report generation for PD# {args.pd_number}, test type: {args.test_type}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Debug mode: {'enabled' if args.debug else 'disabled'}")
    logger.info(f"Force overwrite: {'enabled' if args.force else 'disabled'}")
    
    # Validate the project directory exists
    project_dirs = list(Path(settings.DEFAULT_INPUT_DIR).glob(f"PD{args.pd_number}*"))
    
    if not project_dirs:
        logger.error(f"No project directory found matching PD# {args.pd_number}")
        print(f"ERROR: No project directory found matching PD# {args.pd_number}")
        print(f"Searched in: {settings.DEFAULT_INPUT_DIR}")
        sys.exit(1)
    
    if len(project_dirs) > 1:
        logger.warning(f"Multiple project directories found for PD# {args.pd_number}: {project_dirs}")
        logger.info(f"Using the first match: {project_dirs[0]}")
        print(f"WARNING: Multiple project directories found for PD# {args.pd_number}")
        print(f"Using: {project_dirs[0]}")
    
    project_dir = project_dirs[0]
    company_name = project_dir.name.replace(f"PD{args.pd_number} ", "")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if output file already exists
    output_filename = f"TR_PH{args.pd_number}_Rev0_{company_name}_{args.test_type}.docx"
    output_path = output_dir / output_filename
    
    if output_path.exists() and not args.force:
        logger.warning(f"Output file already exists: {output_path}")
        print(f"WARNING: Output file already exists: {output_path}")
        overwrite = input("Do you want to overwrite? (y/n): ").lower()
        if overwrite != 'y':
            logger.info("Report generation cancelled by user")
            print("Report generation cancelled")
            sys.exit(0)
    
    # Initialize the report generator
    generator = ReportGenerator(
        project_dir=project_dir,
        pd_number=args.pd_number,
        company_name=company_name,
        test_type=args.test_type,
        output_dir=output_dir,
        logger=logger,
    )
    
    try:
        # Generate the report
        report_path = generator.generate_report()
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        logger.info(f"Report generated successfully: {report_path}")
        logger.info(f"Total execution time: {elapsed_time:.2f} seconds")
        
        print(f"\nReport generated successfully: {report_path}")
        print(f"Total execution time: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        logger.critical(f"Failed to generate report: {e}", exc_info=True)
        print(f"\nERROR: Failed to generate report: {e}")
        print("See log file for details")
        sys.exit(1)
    
if __name__ == "__main__":
    main()
