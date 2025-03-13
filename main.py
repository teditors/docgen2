#!/usr/bin/env python3
"""
Aerospace Test Directory Generator

This script creates a realistic test directory structure for aerospace hardware testing,
including engineering results and business paperwork.
"""

import os
import sys
import random
import argparse
import datetime
from pathlib import Path

# Import custom modules
from config import DEFAULT_OUTPUT_DIR, TEST_THEMES
from directory_generator import DirectoryGenerator
from logger import setup_logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate a realistic aerospace test directory structure.'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default=DEFAULT_OUTPUT_DIR,
        help='Output directory for the test structure. Defaults to "testbed" in the current directory.'
    )
    
    parser.add_argument(
        '--projects', 
        type=int, 
        default=5,
        help='Number of project folders to create. Default is 5.'
    )
    
    parser.add_argument(
        '--seed', 
        type=int,
        help='Random seed for reproducible generation.'
    )
    
    parser.add_argument(
        '--log-file', 
        type=str,
        help='Path to the log file. Defaults to "generator_TIMESTAMP.log" in the script directory.'
    )
    
    parser.add_argument(
        '--log-level', 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help='Logging level for console output. Default is INFO.'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output.'
    )
    
    parser.add_argument(
        '--themes',
        type=str,
        help='Comma-separated list of theme indices to use (0-9). Default is all themes.'
    )
        
    parser.add_argument(
        '--output-format',
        type=str,
        default='pdf',
        choices=['pdf', 'jpg', 'png'],
        help='Format for document files. Use "jpg" or "png" on platforms without PDF support (like Android). Default is "pdf".'
    )
    
    return parser.parse_args()

def main():
    """Main function to run the application."""
    args = parse_arguments()
    
    # Set the random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else args.log_level
    logger = setup_logger(args.log_file, log_level)
    
    logger.info("Starting Aerospace Test Directory Generator")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Number of projects: {args.projects}")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Determine which themes to use
    available_themes = TEST_THEMES.copy()
    if args.themes:
        try:
            theme_indices = [int(idx) for idx in args.themes.split(',')]
            selected_themes = [available_themes[idx] for idx in theme_indices if 0 <= idx < len(available_themes)]
            if not selected_themes:
                logger.warning("No valid theme indices provided. Using all themes.")
            else:
                available_themes = selected_themes
                logger.info(f"Using selected themes: {[theme['name'] for theme in selected_themes]}")
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing theme indices: {e}. Using all themes.")
    
    # Initialize and run the directory generator
    generator = DirectoryGenerator(
        base_dir=args.output_dir,
        num_projects=args.projects,
        available_themes=available_themes,
        logger=logger,
        output_format=args.output_format 
    )
    
    generator.generate_structure()
    
    logger.info("Directory structure generation complete")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
