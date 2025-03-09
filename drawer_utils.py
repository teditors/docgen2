"""
Utility functions for drawing hardware components.
"""

import random
from math import sin, cos, pi

def get_component_type(component_name, component_mapping):
    """
    Determine component type based on name.
    
    Args:
        component_name (str): Name of the component
        component_mapping (dict): Dictionary mapping components to keywords
        
    Returns:
        str: Component type
    """
    component_lower = component_name.lower()
    
    for component_type, config in component_mapping.items():
        if any(keyword in component_lower for keyword in config["keywords"]):
            return component_type
    
    # Default to avionics if no match
    return "avionics"

def get_random_color(colors):
    """
    Get a random color from a list of colors.
    
    Args:
        colors (list): List of color tuples
        
    Returns:
        tuple: RGB color tuple
    """
    return random.choice(colors)

def create_variation(base_color, variation=20):
    """
    Create a variation of a base color.
    
    Args:
        base_color (tuple): Base RGB color
        variation (int): Maximum amount to vary by
        
    Returns:
        tuple: Varied RGB color
    """
    r = max(0, min(255, base_color[0] + random.randint(-variation, variation)))
    g = max(0, min(255, base_color[1] + random.randint(-variation, variation)))
    b = max(0, min(255, base_color[2] + random.randint(-variation, variation)))
    return (r, g, b)

def draw_grid(draw, x1, y1, x2, y2, rows, cols, color=(0, 0, 0), width=1):
    """
    Draw a grid pattern.
    
    Args:
        draw: PIL ImageDraw object
        x1, y1: Top-left coordinates
        x2, y2: Bottom-right coordinates
        rows, cols: Number of rows and columns
        color: Line color
        width: Line width
    """
    # Draw horizontal lines
    for i in range(rows + 1):
        y = y1 + i * (y2 - y1) // rows
        draw.line([(x1, y), (x2, y)], fill=color, width=width)
    
    # Draw vertical lines
    for i in range(cols + 1):
        x = x1 + i * (x2 - x1) // cols
        draw.line([(x, y1), (x, y2)], fill=color, width=width)

def draw_dashed_line(draw, start, end, color=(0, 0, 0), width=1, dash_length=5, gap_length=3):
    """
    Draw a dashed line.
    
    Args:
        draw: PIL ImageDraw object
        start: Starting coordinates (x, y)
        end: Ending coordinates (x, y)
        color: Line color
        width: Line width
        dash_length: Length of each dash
        gap_length: Length of each gap
    """
    # Calculate line length and angle
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = (dx**2 + dy**2)**0.5
    
    if length == 0:
        return
    
    # Calculate step per unit length
    x_step = dx / length
    y_step = dy / length
    
    # Draw dashes
    pos = 0
    x, y = start
    
    while pos < length:
        # Draw dash
        dash_end = min(pos + dash_length, length)
        x_end = start[0] + dash_end * x_step
        y_end = start[1] + dash_end * y_step
        
        draw.line([(x, y), (x_end, y_end)], fill=color, width=width)
        
        # Move to next position
        pos = dash_end + gap_length
        x = start[0] + pos * x_step
        y = start[1] + pos * y_step

def draw_electronic_components(draw, x1, y1, x2, y2, count=20, colors=None):
    """
    Draw random electronic components in a region.
    
    Args:
        draw: PIL ImageDraw object
        x1, y1: Top-left coordinates
        x2, y2: Bottom-right coordinates
        count: Number of components to draw
        colors: List of color tuples to use
    """
    if colors is None:
        colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
        
    for _ in range(count):
        comp_x = random.randint(x1, x2)
        comp_y = random.randint(y1, y2)
        comp_size = random.randint(10, 30)
        comp_color = random.choice(colors)
        
        if random.random() < 0.3:
            # Square component (chip)
            draw.rectangle(
                [(comp_x, comp_y), 
                 (comp_x + comp_size, comp_y + comp_size//2)],
                fill=comp_color, outline=(0, 0, 0)
            )
        else:
            # Round component (capacitor)
            draw.ellipse(
                [(comp_x, comp_y), 
                 (comp_x + comp_size//2, comp_y + comp_size//2)],
                fill=comp_color, outline=(0, 0, 0)
            )

def draw_metal_texture(draw, x1, y1, x2, y2, base_color, lines=10, variation=10):
    """
    Draw a metal texture with subtle variations.
    
    Args:
        draw: PIL ImageDraw object
        x1, y1: Top-left coordinates
        x2, y2: Bottom-right coordinates
        base_color: Base RGB color
        lines: Number of highlight lines
        variation: Color variation amount
    """
    # Fill base color
    draw.rectangle([(x1, y1), (x2, y2)], fill=base_color, outline=(0, 0, 0))
    
    # Add highlight lines
    for _ in range(lines):
        y = random.randint(y1, y2)
        line_color = create_variation(base_color, variation)
        draw.line([(x1, y), (x2, y)], fill=line_color, width=1)

def calculate_ellipse_points(center_x, center_y, a, b, start_angle, end_angle, steps=36):
    """
    Calculate points along an ellipse.
    
    Args:
        center_x, center_y: Center coordinates
        a, b: Major and minor axes
        start_angle, end_angle: Angle range in radians
        steps: Number of points to calculate
        
    Returns:
        list: List of point coordinates
    """
    points = []
    for i in range(steps):
        angle = start_angle + (end_angle - start_angle) * i / (steps - 1)
        x = center_x + a * cos(angle)
        y = center_y + b * sin(angle)
        points.append((int(x), int(y)))
    return points
