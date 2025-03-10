"""
Logging configuration for the aerospace hardware test report generator.
"""

import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path


class CustomFormatter(logging.Formatter):
    """Custom formatter that colorizes the output when printed to the console."""
    
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[91m\033[1m',  # Bold Red
        'RESET': '\033[0m'      # Reset color
    }
    
    def format(self, record):
        log_message = super().format(record)
        # Only colorize if outputting to terminal
        if sys.stdout.isatty() and hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            log_message = f"{color}{log_message}{reset}"
        return log_message


def setup_logger(level="INFO", log_file=None, log_dir=None, log_prefix="report_generator", 
                include_timestamp=True, console_level=None):
    """Configure and return a logger.
    
    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str, optional): Path to log file. If None, logs to a default location.
        log_dir (str or Path, optional): Directory for log files. If None, uses ./logs
        log_prefix (str, optional): Prefix for log filenames
        include_timestamp (bool, optional): Whether to include timestamp in log filename
        console_level (str, optional): Separate logging level for console. If None, uses `level`
    
    Returns:
        Logger: Configured logger
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Set console level to the same as file level if not specified
    if console_level is None:
        console_numeric_level = numeric_level
    else:
        console_numeric_level = getattr(logging, console_level.upper(), numeric_level)
    
    # Create logger
    logger = logging.getLogger("report_generator")
    logger.setLevel(min(numeric_level, console_numeric_level))  # Set to the most verbose level
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create formatters
    verbose_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    
    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Add console handler with colorized output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_numeric_level)
    console_handler.setFormatter(CustomFormatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_file is None:
        # Create logs directory if it doesn't exist
        if log_dir is None:
            logs_dir = Path("logs")
        else:
            logs_dir = Path(log_dir)
            
        logs_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate log filename with timestamp if requested
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"{log_prefix}_{timestamp}.log"
        else:
            log_file = logs_dir / f"{log_prefix}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(verbose_formatter)
    logger.addHandler(file_handler)
    
    # Log initialization information
    logger.info(f"Logging initialized at level {level} (file) / {console_level or level} (console)")
    logger.info(f"Log file: {log_file}")
    
    # Add custom exception hook to log unhandled exceptions
    def exception_handler(exc_type, exc_value, exc_traceback):
        """Handle unhandled exceptions by logging them."""
        if issubclass(exc_type, KeyboardInterrupt):
            # Call the original exception handler for KeyboardInterrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        # Log the exception
        logger.critical("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
        
        # Call the original exception handler
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    # Set the exception hook
    sys.excepthook = exception_handler
    
    return logger


def log_system_info(logger):
    """Log system information for debugging purposes.
    
    Args:
        logger: Logger instance
    """
    import platform
    import sys
    
    logger.info("System Information:")
    logger.info(f"  Platform: {platform.platform()}")
    logger.info(f"  Python Version: {platform.python_version()}")
    logger.info(f"  Python Implementation: {platform.python_implementation()}")
    logger.info(f"  System: {platform.system()} {platform.release()}")
    
    try:
        # Try to get more detailed information
        import psutil
        
        # Memory information
        mem = psutil.virtual_memory()
        logger.info(f"  RAM: Total={mem.total / (1024**3):.2f}GB, Available={mem.available / (1024**3):.2f}GB")
        
        # CPU information
        logger.info(f"  CPU Cores: {psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count()} Logical")
        
        # Disk information
        disk = psutil.disk_usage('/')
        logger.info(f"  Disk Space: Total={disk.total / (1024**3):.2f}GB, Free={disk.free / (1024**3):.2f}GB")
    except ImportError:
        logger.debug("psutil not available for extended system information")
