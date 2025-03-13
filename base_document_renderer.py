"""
Base Document Renderer Module

This module provides the base abstract class for document renderers.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class DocumentRenderer(ABC):
    """
    Abstract base class for document renderers.
    This defines the interface that all renderers must implement.
    """
    
    def __init__(self, logger=None):
        """Initialize the renderer."""
        self.logger = logger
        # The content generator will be imported and initialized in the subclasses
        # to avoid circular imports
        self.content_generator = None
    
    @abstractmethod
    def create_purchase_order(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """
        Create a purchase order document.
        
        Args:
            filepath: Directory to save the document
            filename: Base filename (without extension)
            project_theme: Project theme dictionary
            
        Returns:
            str: Full path to the created document
        """
        pass
    
    @abstractmethod
    def create_quote(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """
        Create a quote document.
        
        Args:
            filepath: Directory to save the document
            filename: Base filename (without extension)
            project_theme: Project theme dictionary
            
        Returns:
            str: Full path to the created document
        """
        pass
    
    @abstractmethod
    def create_nod(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """
        Create a Notice Of Deviation document.
        
        Args:
            filepath: Directory to save the document
            filename: Base filename (without extension)
            project_theme: Project theme dictionary
            
        Returns:
            str: Full path to the created document
        """
        pass
    
    @abstractmethod
    def create_specification(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """
        Create a specification document.
        
        Args:
            filepath: Directory to save the document
            filename: Base filename (without extension)
            project_theme: Project theme dictionary
            
        Returns:
            str: Full path to the created document
        """
        pass
    
    @abstractmethod
    def create_test_log(self, filepath: str, test_type: str, project_theme: Dict) -> str:
        """
        Create a test log document.
        
        Args:
            filepath: Directory to save the document
            test_type: Type of test (from TEST_TYPES)
            project_theme: Project theme dictionary
            
        Returns:
            str: Full path to the created document
        """
        pass
