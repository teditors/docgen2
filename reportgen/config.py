"""
Configuration settings for the aerospace hardware test report generator.
Contains global settings, paths, and constants.
"""

import os
from pathlib import Path


class Settings:
    """Central configuration class for the report generator."""
    
    # Base directory for test data
    BASE_DIR = os.environ.get("TESTBED_DIR", "testbed")
    
    # Company information
    COMPANY_NAME = "Syrup Heavy Industries"
    COMPANY_ADDRESS = "13191 Dapplegrey Rd, Garden Grove, CA 92843"
        
    # Base directory configuration
    DEFAULT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_INPUT_DIR = os.path.join(DEFAULT_BASE_DIR, "../testbed")
    DEFAULT_OUTPUT_DIR = os.path.join(DEFAULT_BASE_DIR, "reports")
    
    # Report styling
    REPORT_STYLES = {
        "Title": {"font": "Calibri", "size": 18, "bold": True, "alignment": "center"},
        "Heading1": {"font": "Calibri", "size": 16, "bold": True},
        "Heading2": {"font": "Calibri", "size": 14, "bold": True},
        "Heading3": {"font": "Calibri", "size": 12, "bold": True},
        "Normal": {"font": "Calibri", "size": 11},
        "Table": {"font": "Calibri", "size": 10},
        "Caption": {"font": "Calibri", "size": 10, "italic": True},
        "Footer": {"font": "Calibri", "size": 8, "italic": True},
        "Header": {"font": "Calibri", "size": 8},
    }
    
    # File paths and patterns
    ADMIN_PATTERNS = {
        "PO": {"path": "admin/PO", "pattern": "PO*"},
        "quotes": {"path": "admin/quotes", "pattern": "Quote*"},
        "specs": {"path": "admin/specification", "pattern": "spec*"},
    }
    
    TEST_SUBFOLDERS = {
        "data": {"pattern": "*.jpg"},
        "NODs": {"pattern": "NOD_*.pdf"},
        "photographs": {"pattern": "photo_*.jpeg"},
        "worksheets": {"pattern": "TestLog_*.pdf"},
    }
    
    # Footer text
    PROPRIETARY_FOOTER = (
        "PROPRIETARY INFORMATION: This document contains proprietary information of "
        "{company_name} and is not to be disclosed or used without prior written permission."
    )
    
    # Test result options
    TEST_RESULTS = ["PASS", "FAIL", "INCONCLUSIVE", "NOT PERFORMED"]
    

settings = Settings()
