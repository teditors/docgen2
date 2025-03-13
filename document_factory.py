"""
Document Factory Module

This module provides a factory for creating document renderers.
"""

import logging
from typing import Optional

from base_document_renderer import DocumentRenderer
from pdf_renderer import PDFRenderer
from image_renderer import ImageRenderer

class DocumentFactory:
    """
    Factory class for creating document renderers based on output format.
    """
    
    @staticmethod
    def create_renderer(output_format: str, logger: Optional[logging.Logger] = None) -> DocumentRenderer:
        """
        Create and return a document renderer for the specified output format.
        
        Args:
            output_format (str): Output format ('pdf', 'jpg', or 'png')
            logger (logging.Logger, optional): Logger instance. Defaults to None.
            
        Returns:
            DocumentRenderer: A renderer for the specified format
            
        Raises:
            ValueError: If the output format is not supported
        """
        output_format = output_format.lower()
        
        if output_format == 'pdf':
            return PDFRenderer(logger)
        elif output_format in ['jpg', 'jpeg']:
            return ImageRenderer(logger, format='jpg')
        elif output_format == 'png':
            return ImageRenderer(logger, format='png')
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
