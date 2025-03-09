"""
Utility Functions Module

This module contains utility functions for the aerospace test directory generator.
"""

import os
import logging

def sanitize_filename(text):
    """
    Replace invalid filename characters with safe alternatives.
    
    Args:
        text (str): Input text to sanitize
        
    Returns:
        str: Sanitized text safe for use in filenames
    """
    if not text:
        return "unnamed"
        
    # Replace characters that are problematic in filenames
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        text = text.replace(char, '-')
    
    # Trim excessive whitespace
    text = ' '.join(text.split())
    
    return text

def ensure_directory(directory_path, logger=None):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to directory
        logger (logging.Logger, optional): Logger for recording actions
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        if logger:
            logger.debug(f"Ensured directory exists: {directory_path}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Error creating directory {directory_path}: {e}")
        return False

def safe_file_operation(operation_func, fallback_value=None, logger=None):
    """
    Decorator to safely execute file operations with error handling.
    
    Args:
        operation_func (callable): Function that performs file operation
        fallback_value: Value to return if operation fails
        logger (logging.Logger, optional): Logger for recording errors
        
    Returns:
        callable: Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            if logger:
                logger.error(f"Error in file operation {operation_func.__name__}: {e}")
            return fallback_value
    return wrapper
