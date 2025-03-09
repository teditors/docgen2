#!/usr/bin/env python3
"""
Aerospace Test Directory Generator

This script creates a realistic test directory structure for aerospace hardware testing,
including engineering results and business paperwork.
"""

import os
import random
import datetime
from pathlib import Path
import string
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO

# Constants
HOME_DIR = str(Path.home())
BASE_DIR = os.path.join(HOME_DIR, "testbed")

# Company name components for generating realistic company names
COMPANY_NAME_PREFIXES = [
    "Advanced", "Precision", "Dynamic", "Orbital", "Stellar", "Quantum", "Integrated", 
    "Alpha", "Global", "NextGen", "Innovative", "Strategic", "Universal", "Apex"
]

COMPANY_NAME_MIDS = [
    "Aerospace", "Propulsion", "Systems", "Engineering", "Technologies", "Dynamics",
    "Materials", "Structures", "Aviation", "Defense", "Space", "Rocket", "Composite"
]

COMPANY_NAME_SUFFIXES = [
    "Solutions", "Industries", "Corporation", "Systems", "Services", "Technologies",
    "Group", "Associates", "International", "Enterprises", "Labs", "Works", "Innovations"
]

# Test project themes for consistency across a project
TEST_THEMES = [
    {
        "name": "Rocket Engine",
        "components": ["Nozzle", "Combustion Chamber", "Turbopump", "Igniter", "Fuel Injector"],
        "data_descriptions": ["Thrust", "Temperature", "Pressure", "Vibration", "Flow Rate", "Ignition Sequence"]
    },
    {
        "name": "Satellite Solar Panel",
        "components": ["PV Array", "Deployment Mechanism", "Power Regulator", "Thermal Control", "Junction Box"],
        "data_descriptions": ["Power Output", "Deployment Angle", "Temperature Cycling", "Radiation Exposure", "Efficiency"]
    },
    {
        "name": "Landing Gear",
        "components": ["Strut", "Actuator", "Wheel Assembly", "Brake System", "Shock Absorber"],
        "data_descriptions": ["Load Test", "Deployment Time", "Shock Response", "Fatigue Test", "Brake Performance"]
    },
    {
        "name": "Avionics System",
        "components": ["Flight Computer", "Navigation Unit", "Communication System", "Power Distribution", "Sensor Array"],
        "data_descriptions": ["Signal Integrity", "Processor Load", "Power Consumption", "Heat Dissipation", "Data Throughput"]
    },
    {
        "name": "Fuel Tank",
        "components": ["Tank Shell", "Baffles", "Fuel Pickup", "Pressure Relief Valve", "Feed Line"],
        "data_descriptions": ["Pressure Test", "Slosh Dynamics", "Temperature Gradient", "Fill/Drain Rate", "Leak Detection"]
    },
    {
        "name": "Heat Shield",
        "components": ["Ablative Layer", "Structural Support", "Temperature Sensor", "Attachment Points", "Edge Seals"],
        "data_descriptions": ["Thermal Protection", "Ablation Rate", "Structural Integrity", "Temperature Profile", "Weight Loss"]
    },
    {
        "name": "Control Surface",
        "components": ["Aileron", "Actuator", "Hinge Mechanism", "Control Linkage", "Deflection Limiter"],
        "data_descriptions": ["Deflection Angle", "Response Time", "Flutter Test", "Load Distribution", "Position Accuracy"]
    },
    {
        "name": "Propellant Valve",
        "components": ["Valve Body", "Actuator", "Seals", "Pressure Sensor", "Flow Restrictor"],
        "data_descriptions": ["Flow Rate", "Opening Time", "Leakage Test", "Pressure Drop", "Cycle Life"]
    },
    {
        "name": "Payload Fairing",
        "components": ["Composite Shell", "Separation System", "Acoustic Blanket", "Vents", "Access Ports"],
        "data_descriptions": ["Separation Test", "Acoustic Transmission", "Thermal Profile", "Venting Performance", "Structural Load"]
    },
    {
        "name": "Docking Mechanism",
        "components": ["Capture System", "Alignment Guides", "Latches", "Seals", "Electrical Connectors"],
        "data_descriptions": ["Capture Envelope", "Alignment Accuracy", "Latch Strength", "Seal Compression", "Connection Test"]
    }
]

# Test types and their common measurements
TEST_TYPES = {
    "Dynamics": ["Vibration", "Shock", "Modal Analysis", "Acoustic", "Random Vibration"],
    "EMIEMC": ["Conducted Emissions", "Radiated Emissions", "Susceptibility", "ESD", "Lightning"],
    "Environmental": ["Thermal Cycling", "Vacuum", "Salt Fog", "Humidity", "Altitude"]
}


class DirectoryGenerator:
    """Main class for generating the test directory structure."""
    
    def __init__(self):
        """Initialize the generator."""
        self.ensure_base_dir()
    
    def ensure_base_dir(self):
        """Ensure the base directory exists."""
        os.makedirs(BASE_DIR, exist_ok=True)
        print(f"Base directory created at: {BASE_DIR}")
    
    def generate_structure(self):
        """Generate the full directory structure."""
        # Create 10 project folders
        for _ in range(10):
            self._create_project()
    
    def _create_project(self):
        """Create a single project folder with all subfolders and files."""
        # Select a random theme for this project
        project_theme = random.choice(TEST_THEMES)
        
        # Generate project ID and company name
        project_id = 'PD' + ''.join(random.choices(string.digits, k=8))
        company_name = self._generate_company_name()
        project_dir_name = f"{project_id} {company_name}"
        project_path = os.path.join(BASE_DIR, project_dir_name)
        
        print(f"Creating project: {project_dir_name}")
        os.makedirs(project_path, exist_ok=True)
        
        # Create admin and testing folders
        admin_path = os.path.join(project_path, "admin")
        testing_path = os.path.join(project_path, "testing")
        os.makedirs(admin_path, exist_ok=True)
        os.makedirs(testing_path, exist_ok=True)
        
        # Create admin subfolders and files
        self._create_admin_folders(admin_path, project_theme)
        
        # Create testing subfolders and files
        self._create_testing_folders(testing_path, project_theme)
    
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
        os.makedirs(po_path, exist_ok=True)
        if random.random() < 0.8:  # 80% chance to create a PO file
            po_number = ''.join(random.choices(string.digits, k=6))
            self._create_dummy_pdf(po_path, f"PO{po_number}", project_theme)
        
        # Create quotes folder and possibly a quote file
        quotes_path = os.path.join(admin_path, "quotes")
        os.makedirs(quotes_path, exist_ok=True)
        if random.random() < 0.8:  # 80% chance to create a quote file
            quote_number = ''.join(random.choices(string.digits, k=6))
            self._create_dummy_pdf(quotes_path, f"Quote{quote_number}", project_theme)
        
        # Create specification folder and possibly a spec file
        spec_path = os.path.join(admin_path, "specification")
        os.makedirs(spec_path, exist_ok=True)
        if random.random() < 0.8:  # 80% chance to create a spec file
            spec_number = ''.join(random.choices(string.digits, k=6))
            self._create_dummy_pdf(spec_path, f"spec{spec_number}", project_theme)
    
    def _create_testing_folders(self, testing_path, project_theme):
        """Create the testing folders and their contents."""
        # Create test type folders (Dynamics, EMIEMC, Environmental)
        for test_type in TEST_TYPES.keys():
            test_type_path = os.path.join(testing_path, test_type)
            os.makedirs(test_type_path, exist_ok=True)
            
            # Create 1-5 PHB folders within each test type folder
            for _ in range(random.randint(1, 5)):
                phb_id = 'PHB' + ''.join(random.choices(string.digits, k=8))
                phb_path = os.path.join(test_type_path, phb_id)
                os.makedirs(phb_path, exist_ok=True)
                
                # Create standard subfolders within each PHB folder
                self._create_phb_subfolders(phb_path, test_type, project_theme)
    
    def _create_phb_subfolders(self, phb_path, test_type, project_theme):
        """Create the standard subfolders within a PHB folder."""
        # Create data folder with data files
        data_path = os.path.join(phb_path, "data")
        os.makedirs(data_path, exist_ok=True)
        
        # Create 0-20 data files
        num_data_files = random.randint(0, 20)
        for i in range(num_data_files):
            file_num = f"{i+1:03d}"
            description = self._generate_data_description(test_type, project_theme)
            self._create_data_graph(data_path, f"{file_num}_{description}.jpg", description, test_type)
        
        # Create NODs folder possibly with NOD files
        nods_path = os.path.join(phb_path, "NODs")
        os.makedirs(nods_path, exist_ok=True)
        
        # 20% chance to create 1-5 NOD files
        if random.random() < 0.2:
            num_nod_files = random.randint(1, 5)
            for _ in range(num_nod_files):
                date = self._generate_random_date()
                self._create_dummy_pdf(nods_path, f"NOD_{date.strftime('%m.%d.%Y')}", project_theme)
        
        # Create photographs folder with photos
        photos_path = os.path.join(phb_path, "photographs")
        os.makedirs(photos_path, exist_ok=True)
        
        # Create 1-25 photograph files
        num_photos = random.randint(1, 25)
        for i in range(num_photos):
            component = random.choice(project_theme["components"])
            orientation = "landscape" if random.random() < 0.5 else "portrait"
            self._create_dummy_photo(photos_path, f"photo_{i+1:03d}_{component}.jpeg", component, orientation)
        
        # Create worksheets folder
        worksheets_path = os.path.join(phb_path, "worksheets")
        os.makedirs(worksheets_path, exist_ok=True)
    
    def _generate_data_description(self, test_type, project_theme):
        """Generate a relevant data description based on test type and project theme."""
        test_specifics = TEST_TYPES[test_type]
        test_specific = random.choice(test_specifics)
        
        component = random.choice(project_theme["components"])
        data_type = random.choice(project_theme["data_descriptions"])
        
        return f"{component}_{data_type}_{test_specific}"
    
    def _generate_random_date(self):
        """Generate a random date within the last 3 years."""
        today = datetime.date.today()
        days_back = random.randint(1, 3 * 365)  # Up to 3 years back
        return today - datetime.timedelta(days=days_back)
    
    def _create_dummy_pdf(self, path, filename, project_theme):
        """Create a dummy .pdf file (actually a text file with .pdf extension)."""
        with open(os.path.join(path, f"{filename}.pdf"), 'w') as f:
            f.write(f"Dummy PDF file for {filename}\n")
            f.write(f"Project: {project_theme['name']}\n")
            f.write(f"Components: {', '.join(project_theme['components'])}\n")
            f.write(f"Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _create_data_graph(self, path, filename, description, test_type):
        """Create a dummy data graph as a JPG file."""
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
        
        # Save the figure to the specified path
        plt.savefig(os.path.join(path, filename), dpi=100)
        plt.close()
    
    def _create_dummy_photo(self, path, filename, component, orientation):
        """Create a dummy photo (simple image with component name)."""
        # Set dimensions based on orientation
        if orientation == "landscape":
            width, height = 800, 600
        else:
            width, height = 600, 800
        
        # Create a new image with a light gray background
        image = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple representation of the component
        draw.rectangle(
            [(width * 0.2, height * 0.2), (width * 0.8, height * 0.8)],
            outline=(0, 0, 0),
            fill=(220, 220, 220)
        )
        
        # Add some simple shapes within the component to make it look like test equipment
        draw.line([(width * 0.3, height * 0.3), (width * 0.7, height * 0.3)], fill=(0, 0, 0), width=2)
        draw.line([(width * 0.3, height * 0.4), (width * 0.7, height * 0.4)], fill=(0, 0, 0), width=2)
        draw.rectangle(
            [(width * 0.4, height * 0.5), (width * 0.6, height * 0.7)],
            outline=(0, 0, 0),
            fill=(200, 200, 200)
        )
        
        # Add the component name as text
        draw.text((width * 0.1, height * 0.1), f"Test Setup: {component}", fill=(0, 0, 0))
        draw.text((width * 0.1, height * 0.85), f"Orientation: {orientation}", fill=(0, 0, 0))
        
        # Save the image
        image.save(os.path.join(path, filename))


if __name__ == "__main__":
    generator = DirectoryGenerator()
    generator.generate_structure()
    print("Directory structure generation complete.")
