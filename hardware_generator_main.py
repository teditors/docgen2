"""
Hardware Image Generator Main Module

This module provides the main interface for generating hardware images.
It uses the component-specific drawing functions from component_drawers
modules to generate realistic hardware images.
"""

import os
import random
import logging
from PIL import Image, ImageDraw, ImageFont

# Import configuration and utilities
from hardware_image_config import (
    COLOR_SCHEMES, 
    COMPONENT_TYPE_MAPPING, 
    IMAGE_SIZES, 
    DEFAULT_BACKGROUND,
    BORDER_SETTINGS,
    FONT_SETTINGS
)
from utility_functions import sanitize_filename, ensure_directory, safe_file_operation

# Import drawing functions
from component_drawers_1 import (
    draw_rocket_engine,
    draw_solar_panel,
    draw_landing_gear,
    draw_avionics,
    draw_fuel_tank
)
from component_drawers_2 import (
    draw_heat_shield,
    draw_control_surface,
    draw_propellant_valve,
    draw_payload_fairing,
    draw_docking_mechanism
)

# Create a mapping from component type to drawing function
DRAWER_FUNCTIONS = {
    "rocket_engine": draw_rocket_engine,
    "solar_panel": draw_solar_panel,
    "landing_gear": draw_landing_gear,
    "avionics": draw_avionics,
    "fuel_tank": draw_fuel_tank,
    "heat_shield": draw_heat_shield,
    "control_surface": draw_control_surface,
    "propellant_valve": draw_propellant_valve,
    "payload_fairing": draw_payload_fairing,
    "docking_mechanism": draw_docking_mechanism
}

class HardwareImageGenerator:
    """Class for generating realistic hardware images."""
    
    def __init__(self, logger=None):
        """Initialize the hardware image generator."""
        self.logger = logger or logging.getLogger(__name__)
        self.color_schemes = COLOR_SCHEMES
    
    def _get_component_drawer(self, component_name):
        """
        Determine the appropriate drawing function based on the component name.
        
        Args:
            component_name (str): Name of the component
            
        Returns:
            tuple: (drawer_function, color_scheme_name)
        """
        component_lower = component_name.lower()
        
        # Check if the component matches any of the defined types
        for component_type, config in COMPONENT_TYPE_MAPPING.items():
            if any(keyword in component_lower for keyword in config["keywords"]):
                drawer_name = config["drawer"]
                color_scheme_name = config["color_scheme"]
                return DRAWER_FUNCTIONS[drawer_name], color_scheme_name
        
        # Default to avionics if no match
        self.logger.debug(f"No specific drawer found for '{component_name}', using avionics default")
        return draw_avionics, "electronic"
    
    @safe_file_operation
    def generate_hardware_image(self, filepath, component_name, orientation="landscape", theme_name=None):
        """
        Generate a hardware image based on the component name.
        
        Args:
            filepath (str): Directory to save the image in
            component_name (str): Name of the component
            orientation (str): "landscape" or "portrait"
            theme_name (str, optional): Specific color theme to use
            
        Returns:
            str: Path to the created image file, or None if creation failed
        """
        # Sanitize component name for safe filepath
        component_name = sanitize_filename(component_name)
        
        # Ensure the directory exists
        ensure_directory(filepath, self.logger)
        
        # Set up the image size based on orientation
        if orientation.lower() == "landscape":
            width, height = IMAGE_SIZES["landscape"]
        else:
            width, height = IMAGE_SIZES["portrait"]
        
        # Create a new image with the default background color
        image = Image.new('RGB', (width, height), color=DEFAULT_BACKGROUND)
        draw = ImageDraw.Draw(image)
        
        # Get the appropriate drawing function and color scheme
        drawer_function, auto_color_scheme = self._get_component_drawer(component_name)
        
        # Use the provided theme if specified, otherwise use the auto-detected one
        color_scheme_name = theme_name if theme_name in self.color_schemes else auto_color_scheme
        color_scheme = self.color_schemes[color_scheme_name]
        
        # Draw the component
        self.logger.debug(f"Drawing component '{component_name}' using {drawer_function.__name__}")
        drawer_function(draw, width, height, color_scheme)
        
        # Add a border
        draw.rectangle(
            [(0, 0), (width-1, height-1)],
            fill=None, 
            outline=BORDER_SETTINGS["color"], 
            width=BORDER_SETTINGS["width"]
        )
        
        # Add component name as text
        try:
            # Try to use a nicer font if available
            font = ImageFont.truetype(FONT_SETTINGS["default_font"], FONT_SETTINGS["size"])
        except IOError:
            # Fall back to default font
            font = ImageFont.load_default()
            
        text_color = FONT_SETTINGS["color"]
        text = f"Component: {component_name}"
        
        # Handle text width for centering
        if hasattr(draw, 'textlength'):
            text_width = draw.textlength(text, font=font)
        else:
            text_width = font.getsize(text)[0]
            
        text_x = (width - text_width) // 2
        text_y = height - FONT_SETTINGS["y_position"]
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        # Save the image to the specified path
        image_filename = f"hardware_{component_name}_{random.randint(1000, 9999)}.jpeg"
        full_path = os.path.join(filepath, image_filename)
        image.save(full_path)
        
        self.logger.debug(f"Hardware image created: {full_path}")
        return full_path
    
    def generate_multiple_images(self, filepath, component_names, count=1):
        """
        Generate multiple hardware images for a set of components.
        
        Args:
            filepath (str): Directory to save the images in
            component_names (list): List of component names to choose from
            count (int): Number of images to generate
            
        Returns:
            list: Paths to the created image files
        """
        created_files = []
        
        # Ensure the directory exists
        if not ensure_directory(filepath, self.logger):
            self.logger.error(f"Failed to create directory: {filepath}")
            return created_files
        
        # Generate the requested number of images
        self.logger.info(f"Generating {count} hardware images in {filepath}")
        
        for i in range(count):
            try:
                # Select a random component and orientation
                component = random.choice(component_names)
                orientation = random.choice(["landscape", "portrait"])
                
                self.logger.debug(f"Generating image {i+1}/{count} for component '{component}'")
                created_file = self.generate_hardware_image(filepath, component, orientation)
                
                if created_file:
                    created_files.append(created_file)
                    
            except Exception as e:
                self.logger.error(f"Error generating image {i+1}/{count}: {e}")
                # Continue with next image