"""
Directory Generator Module

This module handles the generation of the directory structure and files.
"""

import os
import random
import datetime
import string
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Import custom modules
from config import (
    COMPANY_NAME_PREFIXES,
    COMPANY_NAME_MIDS,
    COMPANY_NAME_SUFFIXES,
    TEST_TYPES
)
from document_factory import DocumentFactory
from hardware_generator_main import HardwareImageGenerator
from logger import setup_logger
from utility_functions import sanitize_filename, ensure_directory, safe_file_operation

class DirectoryGenerator:
    """Main class for generating the test directory structure."""
    
    def __init__(self, base_dir, num_projects=10, available_themes=None, logger=None, output_format="pdf"):
        """
        Initialize the generator.
        
        Args:
            base_dir (str): Base directory for the test structure
            num_projects (int, optional): Number of projects to create. Defaults to 10.
            available_themes (list, optional): List of themes to use. Defaults to None (all themes).
            logger (logging.Logger, optional): Logger to use. Defaults to None.
            output_format (str, optional): Format for document files ("pdf", "jpg", or "png"). Defaults to "pdf".
        """
        self.base_dir = base_dir
        self.num_projects = num_projects
        self.available_themes = available_themes
        self.logger = logger
        self.output_format = output_format.lower()
        
        # Initialize the appropriate document renderer based on output format
        self.doc_renderer = DocumentFactory.create_renderer(self.output_format, logger)
        self.hardware_image_generator = HardwareImageGenerator(logger)
        
        self.ensure_base_dir()
    
    def ensure_base_dir(self):
        """Ensure the base directory exists."""
        ensure_directory(self.base_dir, self.logger)
        if self.logger:
            self.logger.info(f"Base directory created at: {self.base_dir}")
    
    def generate_structure(self):
        """Generate the full directory structure."""
        # Create project folders
        for i in range(self.num_projects):
            if self.logger:
                self.logger.info(f"Creating project {i+1} of {self.num_projects}")
            
            try:
                self._create_project()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error creating project {i+1}: {e}")
                # Continue with next project instead of stopping entirely
                continue
    
    def _create_project(self):
        """Create a single project folder with all subfolders and files."""
        # Select a random theme for this project
        project_theme = random.choice(self.available_themes)
        
        # Generate project ID and company name
        project_id = 'PD' + ''.join(random.choices(string.digits, k=8))
        company_name = self._generate_company_name()
        project_dir_name = f"{project_id} {company_name}"
        project_path = os.path.join(self.base_dir, project_dir_name)
        
        if self.logger:
            self.logger.info(f"Creating project: {project_dir_name}")
            self.logger.info(f"Project theme: {project_theme['name']}")
        
        ensure_directory(project_path, self.logger)
        
        # Create admin, testing, and receiving folders
        admin_path = os.path.join(project_path, "admin")
        testing_path = os.path.join(project_path, "testing")
        receiving_path = os.path.join(project_path, "receiving")
        
        ensure_directory(admin_path, self.logger)
        ensure_directory(testing_path, self.logger)
        ensure_directory(receiving_path, self.logger)
        
        # Create admin subfolders and files
        self._create_admin_folders(admin_path, project_theme)
        
        # Create testing subfolders and files
        self._create_testing_folders(testing_path, project_theme)
        
        # Create receiving folder with hardware images
        self._create_receiving_folder(receiving_path, project_theme)
    
    def _generate_company_name(self):
        """Generate a random aerospace company name."""
        prefix = random.choice(COMPANY_NAME_PREFIXES)
        mid = random.choice(COMPANY_NAME_MIDS)
        suffix = random.choice(COMPANY_NAME_SUFFIXES)
        
        # 50% chance to use all three parts, 50% chance to use just two parts
        if random.random() < 0.5:
            return f"{prefix} {mid} {suffix}"
        else:
            # Equal chance of prefix+mid or mid+suffix
            if random.random() < 0.5:
                return f"{prefix} {mid}"
            else:
                return f"{mid} {suffix}"
    
    def _create_admin_folders(self, admin_path, project_theme):
        """Create the admin folders and their contents."""
        # Create PO folder and possibly a PO file
        po_path = os.path.join(admin_path, "PO")
        ensure_directory(po_path, self.logger)
        po_number = ''.join(random.choices(string.digits, k=6))
        self.doc_renderer.create_purchase_order(po_path, f"PO{po_number}", project_theme)
        
        # Create quotes folder and possibly a quote file
        quotes_path = os.path.join(admin_path, "quotes")
        ensure_directory(quotes_path, self.logger)
        quote_number = ''.join(random.choices(string.digits, k=6))
        self.doc_renderer.create_quote(quotes_path, f"Quote{quote_number}", project_theme)
        
        # Create specification folder and possibly a spec file
        spec_path = os.path.join(admin_path, "specification")
        ensure_directory(spec_path, self.logger)
        spec_number = ''.join(random.choices(string.digits, k=6))
        self.doc_renderer.create_specification(spec_path, f"spec{spec_number}", project_theme)
    
    def _create_testing_folders(self, testing_path, project_theme):
        """Create the testing folders and their contents."""
        # Create test type folders (Dynamics, EMIEMC, Environmental)
        for test_type in TEST_TYPES.keys():
            test_type_path = os.path.join(testing_path, test_type)
            ensure_directory(test_type_path, self.logger)
            
            # Create 0-5 PHB folders within each test type folder
            for _ in range(random.randint(0, 5)):
                phb_id = 'PHB' + ''.join(random.choices(string.digits, k=8))
                phb_path = os.path.join(test_type_path, phb_id)
                ensure_directory(phb_path, self.logger)
                
                # Create standard subfolders within each PHB folder
                try:
                    self._create_phb_subfolders(phb_path, test_type, project_theme)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Error creating PHB subfolders for {phb_id}: {e}")
                    continue
    
    def _create_phb_subfolders(self, phb_path, test_type, project_theme):
        """Create the standard subfolders within a PHB folder."""
        # Create data folder with data files
        data_path = os.path.join(phb_path, "data")
        ensure_directory(data_path, self.logger)
        
        # Create 0-10 data files
        num_data_files = random.randint(0, 10)
        for i in range(num_data_files):
            file_num = f"{i+1:03d}"
            description = self._generate_data_description(test_type, project_theme)
            try:
                self._create_data_graph(data_path, f"{file_num}_{description}.jpg", description, test_type)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error creating data graph {file_num}_{description}.jpg: {e}")
                continue
        
        # Create NODs folder possibly with NOD files
        nods_path = os.path.join(phb_path, "NODs")
        ensure_directory(nods_path, self.logger)
        
        # 20% chance to create 1-3 NOD files
        if random.random() < 0.2:
            num_nod_files = random.randint(1, 3)
            for _ in range(num_nod_files):
                try:
                    date = self._generate_random_date()
                    # Use the document renderer to create NOD files
                    self.doc_renderer.create_nod(nods_path, f"NOD_{date.strftime('%m.%d.%Y')}", project_theme)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Error creating NOD file: {e}")
                    continue
        
        # Create photographs folder with photos
        photos_path = os.path.join(phb_path, "photographs")
        ensure_directory(photos_path, self.logger)
        
        # Create 1-10 photograph files
        num_photos = random.randint(1, 10)
        for i in range(num_photos):
            try:
                component = sanitize_filename(random.choice(project_theme["components"]))
                orientation = "landscape" if random.random() < 0.5 else "portrait"
                self.hardware_image_generator.generate_hardware_image(
                    photos_path, f"photo_{i+1:03d}_{component}", orientation
                )
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error creating photograph: {e}")
                continue
        
        # Create worksheets folder with test logs
        worksheets_path = os.path.join(phb_path, "worksheets")
        ensure_directory(worksheets_path, self.logger)
        
        # Create 1-2 test log documents
        num_logs = random.randint(1, 2)
        for _ in range(num_logs):
            try:
                self.doc_renderer.create_test_log(worksheets_path, test_type, project_theme)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error creating test log: {e}")
                continue
    
    def _create_receiving_folder(self, receiving_path, project_theme):
        """Create the receiving folder with hardware images."""
        # Create 1-5 hardware images of components
        num_images = random.randint(1, 5)
        try:
            self.hardware_image_generator.generate_multiple_images(
                receiving_path, project_theme["components"], count=num_images
            )
            if self.logger:
                self.logger.info(f"Created {num_images} hardware images in receiving folder")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating hardware images: {e}")
    
    def _generate_data_description(self, test_type, project_theme):
        """Generate a relevant data description based on test type and project theme."""
        test_specifics = TEST_TYPES[test_type]
        test_specific = random.choice(test_specifics)
        
        component = random.choice(project_theme["components"])
        data_type = random.choice(project_theme["data_descriptions"])
        
        # Sanitize component, data_type, and test_specific to replace slashes with hyphens
        component = sanitize_filename(component)
        data_type = sanitize_filename(data_type)
        test_specific = sanitize_filename(test_specific)
        
        return f"{component}_{data_type}_{test_specific}"
    
    def _generate_random_date(self):
        """Generate a random date within the last 3 years."""
        today = datetime.date.today()
        days_back = random.randint(1, 3 * 365)  # Up to 3 years back
        return today - datetime.timedelta(days=days_back)
    
    @safe_file_operation
    def _create_data_graph(self, path, filename, description, test_type):
        """Create a dummy data graph as a JPG file."""
        if self.logger:
            self.logger.debug(f"Creating data graph: {filename}")
        
        # Ensure path exists
        ensure_directory(path, self.logger)
        
        # Create a simple matplotlib graph
        plt.figure(figsize=(10, 6))
        
        # Generate some fake data based on the test type
        x = np.linspace(0, 10, 100)
        
        if "Vibration" in description or "Shock" in description:
            # Create a damped oscillation for vibration/shock data
            y = np.exp(-0.2 * x) * np.sin(5 * x) + 0.1 * np.random.randn(100)
            plt.ylabel("Acceleration (g)")
        elif "Temperature" in description or "Thermal" in description:
            # Create a temperature profile with plateaus
            y = 20 + 5 * np.sin(x) + 50 * (x > 3) * (x < 7) + 0.5 * np.random.randn(100)
            plt.ylabel("Temperature (°C)")
        elif "Pressure" in description or "Flow" in description:
            # Create a pressure or flow rate profile
            y = 100 + 20 * np.sin(x/2) + 10 * (x > 5) + np.random.randn(100)
            plt.ylabel("Pressure (kPa)")
        else:
            # Generic oscillating data with noise
            y = 50 + 20 * np.sin(x/2) + 5 * np.cos(3*x) + 2 * np.random.randn(100)
            plt.ylabel("Measurement")
        
        plt.plot(x, y)
        plt.title(description)
        plt.xlabel("Time (s)")
        plt.grid(True)
        
        # Ensure the filename is safe
        safe_filename = sanitize_filename(filename)
        
        # Save the figure to the specified path
        plt.savefig(os.path.join(path, safe_filename), dpi=100)
        plt.close()