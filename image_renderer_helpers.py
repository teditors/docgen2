"""
Image Renderer Helper Module

This module provides helper functions for the image renderer.
"""

from typing import Tuple, List
from PIL import ImageDraw, ImageFont

def draw_text(draw, text, x, y, font, fill=(0, 0, 0)):
    """
    Helper method to draw text at a specific position.
    
    Args:
        draw: PIL ImageDraw object
        text: Text to draw
        x, y: Position coordinates
        font: Font to use
        fill: Color tuple
    """
    draw.text((x, y), text, font=font, fill=fill)

def draw_centered_text(draw, text, x, y, font, fill=(0, 0, 0)):
    """
    Helper method to draw centered text.
    
    Args:
        draw: PIL ImageDraw object
        text: Text to draw
        x, y: Position coordinates (x is center position)
        font: Font to use
        fill: Color tuple
    """
    text_width = get_text_width(text, font, draw)
    draw.text((x - text_width // 2, y), text, font=font, fill=fill)

def get_text_width(text, font, draw=None):
    """
    Get the width of text with the given font.
    
    Args:
        text: Text to measure
        font: Font to use
        draw: Optional ImageDraw object (used in older Pillow versions)
        
    Returns:
        int: Width in pixels
    """
    if hasattr(font, 'getlength'):
        return font.getlength(text)
    elif hasattr(font, 'getsize'):
        # For compatibility with older Pillow versions
        return font.getsize(text)[0]
    elif draw:
        # Even older Pillow versions
        return draw.textlength(text, font=font)
    else:
        # Fallback estimate
        return len(text) * 8  # rough estimate for monospace

def wrap_text(text, font, max_width, draw=None):
    """
    Wrap text to fit within a specified width.
    
    Args:
        text: Text to wrap
        font: Font to use for measuring
        max_width: Maximum width in pixels
        draw: Optional ImageDraw object (used in older Pillow versions)
        
    Returns:
        list: List of wrapped text lines
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Add the word to the current line
        test_line = ' '.join(current_line + [word])
        # Measure the width of the line with the new word
        width = get_text_width(test_line, font, draw)
        
        if width <= max_width:
            # Word fits, add it to the current line
            current_line.append(word)
        else:
            # Word doesn't fit, start a new line
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # If the word is too long for a line, just add it anyway
                lines.append(word)
                current_line = []
    
    # Add the last line if it's not empty
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def draw_table(draw, x, y, data, col_widths, 
               row_height=40, 
               text_color=(0, 0, 0), 
               bg_color=(255, 255, 255), 
               header_color=(200, 200, 200),
               font=None):
    """
    Draw a table.
    
    Args:
        draw: ImageDraw object
        x, y: Starting position (top-left corner)
        data: 2D list of strings representing table data
        col_widths: List of column widths in pixels
        row_height: Height of each row in pixels
        text_color: Color for text
        bg_color: Background color
        header_color: Color for header row
        font: Font to use for text
        
    Returns:
        int: Total height of the table
    """
    if font is None:
        # If no font provided, use default
        font = ImageFont.load_default()
    
    table_width = sum(col_widths)
    
    # Calculate total height
    table_height = len(data) * row_height
    
    # Draw table background
    draw.rectangle([(x, y), (x + table_width, y + table_height)], 
                   fill=bg_color, outline=text_color)
    
    # Draw horizontal lines
    for i in range(len(data) + 1):
        draw.line([(x, y + i * row_height), (x + table_width, y + i * row_height)], 
                 fill=text_color, width=1)
    
    # Draw vertical lines
    current_x = x
    for width in col_widths:
        draw.line([(current_x, y), (current_x, y + table_height)], 
                 fill=text_color, width=1)
        current_x += width
    draw.line([(x + table_width, y), (x + table_width, y + table_height)], 
             fill=text_color, width=1)
    
    # Draw table content
    current_y = y
    for row_idx, row in enumerate(data):
        current_x = x
        for i, cell in enumerate(row):
            # If it's a header row, use a different background
            if row_idx == 0:
                draw.rectangle([(current_x, current_y), 
                              (current_x + col_widths[i], current_y + row_height)], 
                             fill=header_color)
            
            # Center text in cell
            text_width = get_text_width(cell, font, draw)
            text_x = current_x + (col_widths[i] - text_width) // 2
            
            # Determine font height - this is tricky with different Pillow versions
            if hasattr(font, 'getsize'):
                font_height = font.getsize('Tg')[1]  # Height of typical text
            else:
                # Rough estimate based on font "size" if available
                font_height = getattr(font, 'size', 12)
            
            text_y = current_y + (row_height - font_height) // 2
            draw.text((text_x, text_y), cell, font=font, fill=text_color)
            
            current_x += col_widths[i]
        current_y += row_height
    
    return table_height
