"""
Logging module for the Aerospace Test Directory Generator.

This module handles setting up and configuring logging for the application.
"""

import os
import logging
import datetime
from pathlib import Path
from config import LOG_LEVEL, LOG_FORMAT, DEFAULT_LOG_FILE

def setup_logger(log_file=None, console_level="INFO", file_level="DEBUG"):
    """
    Set up and configure the logger.
    
    Args:
        log_file (str, optional): Path to the log file. Defaults to the value in config.
        console_level (str, optional): Logging level for console output. Defaults to "INFO".
        file_level (str, optional): Logging level for file output. Defaults to "DEBUG".
    
    Returns:
        logging.Logger: Configured logger object.
    """
    # Use the default log file from config if none provided
    if log_file is None:
        log_file = DEFAULT_LOG_FILE
    
    # Create a timestamp-based log file if using the default
    if log_file == DEFAULT_LOG_FILE:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.dirname(DEFAULT_LOG_FILE)
        log_file = os.path.join(log_dir, f"generator_{timestamp}.log")
    
    # Create the directory for the log file if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('aerospace_generator')
    logger.setLevel(logging.DEBUG)  # Set to lowest level to catch everything
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, console_level))
    console_handler.setFormatter(formatter)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, file_level))
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.debug("Logger setup complete")
    
    return logger
