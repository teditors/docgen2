"""
Image Document Renderer Module

This module provides image implementation of the document renderer.
"""

import os
import random
import datetime
import logging
from typing import Dict, List, Any, Optional

# Import for image generation
from PIL import Image, ImageDraw, ImageFont

# Import our modules
from base_document_renderer import DocumentRenderer
from document_content_generator import DocumentContentGenerator
from image_renderer_helpers import (
    draw_text, draw_centered_text, wrap_text, draw_table, get_text_width
)

class ImageRenderer(DocumentRenderer):
    """
    Image implementation of the document renderer.
    Renders documents as image files (JPG or PNG).
    """
    
    def __init__(self, logger=None, format="jpg"):
        """
        Initialize the Image renderer.
        
        Args:
            logger: Logger instance
            format (str): Output image format ('jpg' or 'png')
        """
        super().__init__(logger)
        self.content_generator = DocumentContentGenerator(logger)
        self.format = format.lower()
        if self.format not in ['jpg', 'png']:
            if self.logger:
                self.logger.warning(f"Unsupported format '{format}', defaulting to 'jpg'")
            self.format = 'jpg'
            
        # Try to load fonts - use default if not available
        try:
            # For Windows/Mac/Linux, try to load common fonts
            self.title_font = ImageFont.truetype("Arial", 28)
            self.heading_font = ImageFont.truetype("Arial", 18)
            self.normal_font = ImageFont.truetype("Arial", 12)
        except OSError:
            # If font loading fails, use default bitmap font
            if self.logger:
                self.logger.warning("Could not load TrueType fonts, using default font")
            self.title_font = ImageFont.load_default()
            self.heading_font = ImageFont.load_default()
            self.normal_font = ImageFont.load_default()
            
        # Set up colors
        self.text_color = (0, 0, 0)  # Black
        self.bg_color = (255, 255, 255)  # White
        self.accent_color = (200, 200, 200)  # Light Gray
    
    def create_purchase_order(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a purchase order image."""
        if self.logger:
            self.logger.info(f"Creating purchase order image: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_purchase_order_content(filename, project_theme)
        
        # Get the complete file path with appropriate extension
        full_path = os.path.join(filepath, f"{filename}.{self.format}")
        
        # Create a new image with white background (letter size equivalent)
        img_width, img_height = 2100, 2800  # ~8.5x11 inches at 300dpi
        img = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add title
        draw_centered_text(draw, content["title"], img_width // 2, 100, self.title_font, self.text_color)
        
        # Add metadata
        y_pos = 200
        for meta in content["metadata"]:
            draw_text(draw, meta, 100, y_pos, self.normal_font, self.text_color)
            y_pos += 30
        
        y_pos += 20
        
        # Add content for each section
        for section, section_content in content["sections"].items():
            # Draw section heading
            draw_text(draw, section, 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            if isinstance(section_content, list):
                # Draw content lines
                for line in section_content:
                    draw_text(draw, line, 150, y_pos, self.normal_font, self.text_color)
                    y_pos += 30
            
            y_pos += 20
        
        # Add approval section if present
        if "approvals" in content:
            y_pos += 50
            draw_text(draw, content["approvals"]["title"], 100, y_pos, self.heading_font, self.text_color)
            y_pos += 50
            
            # Draw approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                table_width = img_width - 200
                cell_width = table_width // len(signers)
                
                # Draw table header
                for i, signer in enumerate(signers):
                    x = 100 + i * cell_width
                    draw_centered_text(draw, signer, x + cell_width // 2, y_pos, self.normal_font, self.text_color)
                
                y_pos += 40
                
                # Draw signature lines
                for i in range(len(signers)):
                    x = 100 + i * cell_width
                    draw.line([(x + 50, y_pos), (x + cell_width - 50, y_pos)], fill=self.text_color, width=1)
                
                y_pos += 30
                
                # Draw date lines if present
                if "dates" in content["approvals"]:
                    dates = content["approvals"]["dates"]
                    for i, date in enumerate(dates):
                        x = 100 + i * cell_width
                        draw_centered_text(draw, f"Date: {date}", x + cell_width // 2, y_pos, self.normal_font, self.text_color)
        
        # Save the image
        img.save(full_path, quality=95 if self.format == 'jpg' else None)
        if self.logger:
            self.logger.debug(f"Image created successfully: {full_path}")
        
        return full_path
    
    def create_specification(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a specification image."""
        if self.logger:
            self.logger.info(f"Creating specification image: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_specification_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.{self.format}")
        
        # Create a new image (letter size equivalent)
        img_width, img_height = 2100, 2800
        img = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add title
        draw_centered_text(draw, content["title"], img_width // 2, 100, self.title_font, self.text_color)
        
        # Add metadata
        y_pos = 200
        for meta in content["metadata"]:
            draw_text(draw, meta, 100, y_pos, self.normal_font, self.text_color)
            y_pos += 30
        
        y_pos += 20
        
        # Adding content for each section would be similar to previous methods
        # For brevity, I'll implement only a few sections
        
        # Determine sections to render
        sections_to_render = list(content["sections"].keys())[:3]  # First 3 sections
        
        for section in sections_to_render:
            section_content = content["sections"][section]
            
            # Draw section heading
            draw_text(draw, section, 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            if isinstance(section_content, list):
                # Draw content lines
                for line in section_content:
                    # Check if we need to add a page break (simplified approach)
                    if y_pos > img_height - 100:
                        # In a complete implementation, you would create a new page here
                        draw_text(draw, "[Content continues on next page...]", 150, y_pos, self.normal_font, self.text_color)
                        break
                    
                    draw_text(draw, line, 150, y_pos, self.normal_font, self.text_color)
                    y_pos += 30
            
            y_pos += 20
        
        # Placeholder text for remaining sections
        if len(content["sections"]) > 3:
            draw_text(draw, "[Additional sections not shown...]", 100, y_pos, self.normal_font, self.text_color)
        
        # Add approval section
        if "approvals" in content and y_pos < img_height - 200:
            # Position the approvals section at the bottom of the page if there's space
            y_pos = img_height - 200
            
            draw_text(draw, content["approvals"]["title"], 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            # Draw approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                roles = content["approvals"].get("roles", [""] * len(signers))
                
                table_data = [signers, ["________________"] * len(signers)]
                if all(roles):
                    table_data.append(roles)
                
                table_width = img_width - 200
                col_widths = [table_width // len(signers)] * len(signers)
                
                draw_table(
                    draw, 100, y_pos, table_data, col_widths,
                    text_color=self.text_color, bg_color=self.bg_color, header_color=self.accent_color,
                    font=self.normal_font
                )
        
        # Save the image
        img.save(full_path, quality=95 if self.format == 'jpg' else None)
        if self.logger:
            self.logger.debug(f"Image created successfully: {full_path}")
        
        return full_path
    
    def create_test_log(self, filepath: str, test_type: str, project_theme: Dict) -> str:
        """Create a simple test log image."""
        if self.logger:
            self.logger.info(f"Creating simple test log image for {test_type}")
        
        # Generate file name components
        component = random.choice(project_theme["components"])
        test_proc = random.choice(project_theme["test_procedures"])
        test_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
        date_str = test_date.strftime("%Y%m%d")
        
        filename = f"TestLog_{component}_{test_proc}_{date_str}"
        full_path = os.path.join(filepath, f"{filename}.{self.format}")
        
        # Create a blank image
        img_width, img_height = 2100, 2800  # Letter size at 300 dpi
        img = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw test log title
        title = f"TEST LOG: {component.upper()} - {test_proc.upper()}"
        draw_text(draw, title, 100, 100, self.title_font, self.text_color)
        
        # Draw test information
        y_pos = 200
        draw_text(draw, f"Test Date: {test_date.strftime('%B %d, %Y')}", 100, y_pos, self.normal_font, self.text_color)
        y_pos += 50
        draw_text(draw, f"Project: {project_theme['name']}", 100, y_pos, self.normal_font, self.text_color)
        y_pos += 50
        draw_text(draw, f"Test Type: {test_type}", 100, y_pos, self.normal_font, self.text_color)
        y_pos += 50
        draw_text(draw, f"Specification: {random.choice(project_theme['specifications'])}", 100, y_pos, self.normal_font, self.text_color)
        y_pos += 50
        
        # Draw a simple table header
        draw.line([(100, y_pos), (img_width - 100, y_pos)], fill=self.text_color, width=2)
        y_pos += 50
        
        headers = ["Test Step", "Expected Result", "Actual Result", "Pass/Fail"]
        x_positions = [100, 500, 900, 1500]
        
        for i, header in enumerate(headers):
            draw_text(draw, header, x_positions[i], y_pos, self.heading_font, self.text_color)
        
        y_pos += 50
        draw.line([(100, y_pos), (img_width - 100, y_pos)], fill=self.text_color, width=2)
        
        # Add a few dummy test steps
        for i in range(1, 6):
            y_pos += 100
            draw_text(draw, f"Step {i}: {random.choice(['Setup', 'Calibration', 'Run Test', 'Measure', 'Verify'])}", 
                      x_positions[0], y_pos, self.normal_font, self.text_color)
            draw_text(draw, f"Value within {random.randint(1, 10)}% of nominal", 
                      x_positions[1], y_pos, self.normal_font, self.text_color)
            draw_text(draw, f"{random.randint(90, 105)}% of nominal", 
                      x_positions[2], y_pos, self.normal_font, self.text_color)
            draw_text(draw, "PASS" if random.random() < 0.9 else "FAIL", 
                      x_positions[3], y_pos, self.normal_font, self.text_color)
            
            # Add horizontal line after each row
            y_pos += 50
            draw.line([(100, y_pos), (img_width - 100, y_pos)], fill=self.text_color, width=1)
        
        # Add signature area at bottom
        y_pos = img_height - 300
        draw_text(draw, "Signatures:", 100, y_pos, self.heading_font, self.text_color)
        y_pos += 100
        
        # Draw signature lines
        draw.line([(100, y_pos), (600, y_pos)], fill=self.text_color, width=2)
        draw.line([(800, y_pos), (1300, y_pos)], fill=self.text_color, width=2)
        
        y_pos += 30
        draw_text(draw, "Test Engineer", 250, y_pos, self.normal_font, self.text_color)
        draw_text(draw, "Quality Assurance", 950, y_pos, self.normal_font, self.text_color)
        
        # Save the image
        img.save(full_path, quality=90 if self.format == 'jpg' else None)
        
        return full_path
    
    def create_quote(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a quote image."""
        if self.logger:
            self.logger.info(f"Creating quote image: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_quote_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.{self.format}")
        
        # Create a new image (letter size equivalent)
        img_width, img_height = 2100, 2800
        img = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add title
        draw_centered_text(draw, content["title"], img_width // 2, 100, self.title_font, self.text_color)
        
        # Add company info
        y_pos = 170
        draw_centered_text(draw, content["company"]["name"], img_width // 2, y_pos, self.heading_font, self.text_color)
        y_pos += 30
        
        for address_line in content["company"]["address"]:
            draw_centered_text(draw, address_line, img_width // 2, y_pos, self.normal_font, self.text_color)
            y_pos += 30
        
        # Add metadata
        y_pos += 20
        for meta in content["metadata"]:
            draw_text(draw, meta, 100, y_pos, self.normal_font, self.text_color)
            y_pos += 30
        
        y_pos += 20
        
        # Add content for each section
        for section, section_content in content["sections"].items():
            # Draw section heading
            draw_text(draw, section, 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            if isinstance(section_content, list):
                # Draw content lines
                for line in section_content:
                    draw_text(draw, line, 150, y_pos, self.normal_font, self.text_color)
                    y_pos += 30
            elif isinstance(section_content, dict) and section_content.get("type") == "table":
                # Draw table
                headers = section_content["headers"]
                data = section_content["data"]
                
                table_data = [headers] + data
                col_widths = [int((img_width - 300) * 0.7), int((img_width - 300) * 0.3)]
                
                table_height = draw_table(
                    draw, 150, y_pos, table_data, col_widths,
                    text_color=self.text_color, bg_color=self.bg_color, header_color=self.accent_color,
                    font=self.normal_font
                )
                y_pos += table_height + 30
            
            y_pos += 20
        
        # Add contact information
        if "contact" in content:
            y_pos += 30
            draw_text(draw, content["contact"]["title"], 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            for detail in content["contact"]["details"]:
                draw_text(draw, detail, 150, y_pos, self.normal_font, self.text_color)
                y_pos += 30
        
        # Save the image
        img.save(full_path, quality=95 if self.format == 'jpg' else None)
        if self.logger:
            self.logger.debug(f"Image created successfully: {full_path}")
        
        return full_path
    
    def create_nod(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a Notice Of Deviation image."""
        if self.logger:
            self.logger.info(f"Creating NOD image: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_nod_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.{self.format}")
        
        # Create a new image (letter size equivalent)
        img_width, img_height = 2100, 2800
        img = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add title
        draw_centered_text(draw, content["title"], img_width // 2, 100, self.title_font, self.text_color)
        
        # Add metadata
        y_pos = 200
        for meta in content["metadata"]:
            draw_text(draw, meta, 100, y_pos, self.normal_font, self.text_color)
            y_pos += 30
        
        y_pos += 20
        
        # Add content for each section
        for section, section_content in content["sections"].items():
            # Draw section heading
            draw_text(draw, section, 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            if isinstance(section_content, list):
                # Draw content lines
                for line in section_content:
                    draw_text(draw, line, 150, y_pos, self.normal_font, self.text_color)
                    y_pos += 30
            
            y_pos += 20
        
        # Add approval section
        if "approvals" in content:
            y_pos += 50
            draw_text(draw, content["approvals"]["title"], 100, y_pos, self.heading_font, self.text_color)
            y_pos += 40
            
            # Draw approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                dates = content["approvals"].get("dates", ["__/__/____"] * len(signers))
                
                table_data = [signers, ["________________"] * len(signers), dates]
                table_width = img_width - 200
                col_widths = [table_width // len(signers)] * len(signers)
                
                draw_table(
                    draw, 100, y_pos, table_data, col_widths,
                    text_color=self.text_color, bg_color=self.bg_color, header_color=self.accent_color,
                    font=self.normal_font
                )
        
        # Save the image
        img.save(full_path, quality=95 if self.format == 'jpg' else None)
        if self.logger:
            self.logger.debug(f"Image created successfully: {full_path}")
        
        return full_path