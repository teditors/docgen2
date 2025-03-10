"""
File handling utilities for the aerospace hardware test report generator.
"""

import os
import re
import tempfile
import shutil
from pathlib import Path
import logging

import pdf2image  # For PDF to image conversion


def validate_project_directory(base_dir, pd_number):
    """Validate that the project directory exists.
    
    Args:
        base_dir (str or Path): Base directory to search in
        pd_number (str): Project directory number
    
    Returns:
        Path: Path to the project directory, or None if not found
    """
    logger = logging.getLogger("report_generator")
    base_path = Path(base_dir)
    
    logger.debug(f"Searching for project directory with PD{pd_number} in {base_path}")
    
    # Check if the directory exists
    project_dirs = list(base_path.glob(f"PD{pd_number}*"))
    
    if not project_dirs:
        logger.warning(f"No project directory found matching PD{pd_number} in {base_path}")
        return None
    
    # If multiple matches, use the first one
    logger.debug(f"Found project directory: {project_dirs[0]}")
    return project_dirs[0]


def find_files(directory, pattern):
    """Find files matching a pattern in a directory.
    
    Args:
        directory (str or Path): Directory to search in
        pattern (str): Glob pattern to match
    
    Returns:
        list: List of Path objects for matching files
    """
    logger = logging.getLogger("report_generator")
    directory_path = Path(directory)
    
    if not directory_path.exists():
        logger.warning(f"Directory not found: {directory_path}")
        return []
    
    files = list(directory_path.glob(pattern))
    logger.debug(f"Found {len(files)} files matching pattern '{pattern}' in {directory_path}")
    
    # Log the first few files for debugging
    if files and len(files) <= 5:
        logger.debug(f"Files found: {[f.name for f in files]}")
    elif files:
        logger.debug(f"First 5 files: {[f.name for f in files[:5]]}")
    
    return files


def convert_pdf_to_image(pdf_path, dpi=300, fmt="PNG", output_dir=None):
    """Convert a PDF file to an image format.
    
    Args:
        pdf_path (str or Path): Path to the PDF file
        dpi (int, optional): Resolution in dots per inch
        fmt (str, optional): Output format (PNG, JPEG, etc.)
        output_dir (str or Path, optional): Directory to save the output image
                                           If None, a persistent temp directory is used
    
    Returns:
        Path: Path to the converted image file
    """
    logger = logging.getLogger("report_generator")
    
    # Ensure the PDF path is a Path object
    pdf_path = Path(pdf_path)
    
    # Create a dedicated output directory if none provided
    if output_dir is None:
        # Create a persistent temp directory under the application's temp folder
        app_temp_dir = Path(tempfile.gettempdir()) / "aerospace_report_gen"
        app_temp_dir.mkdir(exist_ok=True)
        
        # Use a directory named after the PDF to avoid collisions
        output_dir = app_temp_dir / f"pdf_images_{pdf_path.stem}"
        output_dir.mkdir(exist_ok=True)
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
    logger.debug(f"Converting PDF to image: {pdf_path} -> {output_dir}")
    
    # Create an output filename based on the PDF name
    pdf_filename = pdf_path.stem
    image_path = output_dir / f"{pdf_filename}.{fmt.lower()}"
    
    try:
        # Check if the image already exists (avoid reconversion)
        if image_path.exists():
            logger.debug(f"Using existing converted image: {image_path}")
            return image_path
            
        # Convert the PDF to image
        logger.debug(f"Converting PDF using dpi={dpi}, format={fmt}")
        images = pdf2image.convert_from_path(
            pdf_path, 
            dpi=dpi, 
            output_folder=str(output_dir),
            fmt=fmt.lower(),
            single_file=True,
            paths_only=True
        )
        
        if not images:
            logger.error(f"PDF conversion produced no images: {pdf_path}")
            raise ValueError(f"Failed to convert PDF: {pdf_path}")
        
        # For simplicity, we'll just use the first page for now
        output_image_path = Path(images[0])
        
        # Rename the file to match our expected pattern if needed
        if output_image_path.name != image_path.name:
            logger.debug(f"Renaming {output_image_path} to {image_path}")
            shutil.move(output_image_path, image_path)
            
        logger.debug(f"Successfully converted PDF to image: {image_path}")
        return image_path
        
    except Exception as e:
        logger.error(f"Error converting PDF to image: {e}", exc_info=True)
        raise RuntimeError(f"Error converting PDF to image: {e}")


def extract_test_data(test_folder):
    """Extract test data from a test folder.
    
    Args:
        test_folder (Path): Path to the test folder
    
    Returns:
        dict: Dictionary containing test data
    """
    logger = logging.getLogger("report_generator")
    logger.debug(f"Extracting test data from folder: {test_folder}")
    
    # Check for different possible photo extensions
    photos = find_files(test_folder / "photographs", "photo_*.jpg")
    if not photos:
        photos = find_files(test_folder / "photographs", "photo_*.jpeg")
    
    test_data = {
        "name": test_folder.name,
        "worksheets": find_files(test_folder / "worksheets", "TestLog_*.pdf"),
        "nods": find_files(test_folder / "NODs", "NOD_*.pdf"),
        "photos": photos,
        "plots": find_files(test_folder / "data", "*_Description.jpg"),
    }
    
    # Log what we found for debugging
    for key, items in test_data.items():
        if key != "name":
            logger.debug(f"Found {len(items)} {key} in {test_folder}")
    
    return test_data


def get_po_details(po_file):
    """Extract details from a PO file.
    
    Args:
        po_file (Path): Path to the PO file
    
    Returns:
        dict: Dictionary containing PO details
    """
    logger = logging.getLogger("report_generator")
    logger.debug(f"Extracting details from PO file: {po_file}")
    
    # This is a stub function that would be implemented to extract
    # relevant data from the PO file
    
    # In a real implementation, this might use a PDF parser like PyPDF2 or pdfplumber
    # to extract text from the PO and then parse it to find the relevant information
    
    # For now, return placeholder data
    po_details = {
        "po_number": "PO123456",
        "company": "Client Company",
        "date": "2025-01-15",
        "items": [
            {
                "part_number": "XYZ-123",
                "description": "Controller Assembly",
                "quantity": 1,
                "serial_numbers": ["SN001"],
            },
            {
                "part_number": "XYZ-456",
                "description": "Sensor Package",
                "quantity": 2,
                "serial_numbers": ["SN002", "SN003"],
            },
        ],
    }
    
    return po_details


def parse_test_logs(log_file):
    """Parse a test log PDF file to extract test details.
    
    Args:
        log_file (Path): Path to the test log PDF file
    
    Returns:
        dict: Dictionary containing test details
    """
    logger = logging.getLogger("report_generator")
    logger.debug(f"Parsing test log: {log_file}")
    
    # This is a stub function that would be implemented to extract
    # test details from the log file
    
    # In a real implementation, this might use a PDF parser like PyPDF2 or pdfplumber
    # to extract text from the log and then parse it to find test details
    
    # For now, extract some basic info from the filename
    # Format: TestLog_Component_TestProc_YYYYMMDD.pdf
    filename = log_file.stem
    parts = filename.split("_")
    
    test_details = {"filename": filename}
    
    if len(parts) >= 4:
        test_details["component"] = parts[1]
        test_details["test_name"] = parts[2]
        
        # Parse date if available
        date_str = parts[3]
        if len(date_str) == 8 and date_str.isdigit():
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            test_details["date"] = f"{year}-{month}-{day}"
    
    # Add placeholder data for other fields
    test_details.setdefault("test_name", "Unknown Test")
    test_details.setdefault("date", "Unknown")
    test_details.setdefault("specification", "MIL-STD-810H")
    test_details.setdefault("result", "PASS")
    
    logger.debug(f"Extracted test details: {test_details}")
    return test_details
