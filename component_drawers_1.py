"""
Drawing functions for aerospace hardware components - Part 1.

This module contains functions for drawing rocket engines, solar panels,
landing gear, avionics, and fuel tanks.
"""

import random
from math import sin, cos, pi
from drawer_utils import get_random_color, draw_electronic_components, create_variation

def draw_rocket_engine(draw, width, height, color_scheme):
    """Draw a rocket engine component."""
    metals = color_scheme["metals"]
    highlights = color_scheme["highlights"]
    
    # Nozzle
    nozzle_color = get_random_color(metals)
    draw.polygon(
        [(width//2 - 150, height//4), 
         (width//2 + 150, height//4), 
         (width//2 + 250, height*3//4), 
         (width//2 - 250, height*3//4)],
        fill=nozzle_color, outline=(0, 0, 0)
    )
    
    # Nozzle interior
    interior_color = get_random_color(highlights)
    draw.polygon(
        [(width//2 - 120, height//4 + 20), 
         (width//2 + 120, height//4 + 20), 
         (width//2 + 220, height*3//4 - 20), 
         (width//2 - 220, height*3//4 - 20)],
        fill=interior_color, outline=(0, 0, 0)
    )
    
    # Combustion chamber
    chamber_color = get_random_color(metals)
    draw.rectangle(
        [(width//2 - 100, height//8), 
         (width//2 + 100, height//4)],
        fill=chamber_color, outline=(0, 0, 0)
    )
    
    # Fuel lines
    line_color = get_random_color(metals)
    # Left fuel line
    draw.rectangle(
        [(width//2 - 80, height//16), 
         (width//2 - 60, height//8)],
        fill=line_color, outline=(0, 0, 0)
    )
    # Right fuel line
    draw.rectangle(
        [(width//2 + 60, height//16), 
         (width//2 + 80, height//8)],
        fill=line_color, outline=(0, 0, 0)
    )
    
    # Turbopump (simplified)
    pump_color = get_random_color(metals)
    draw.ellipse(
        [(width//2 - 40, height//32), 
         (width//2 + 40, height//8)],
        fill=pump_color, outline=(0, 0, 0)
    )
    
    # Add cooling channels (lines on nozzle)
    for i in range(-200, 201, 40):
        draw.line(
            [(width//2 + i, height//4), 
             (width//2 + i*1.6, height*3//4)],
            fill=(0, 0, 0), width=2
        )

def draw_solar_panel(draw, width, height, color_scheme):
    """Draw a satellite solar panel component."""
    metals = color_scheme["metals"]
    composites = color_scheme["composites"]
    highlights = color_scheme["highlights"]
    
    # Panel backing structure
    panel_color = get_random_color(composites)
    draw.rectangle(
        [(width//10, height//10), 
         (width*9//10, height*9//10)],
        fill=panel_color, outline=(0, 0, 0)
    )
    
    # Solar cells grid
    cell_width = (width*8//10) // 8
    cell_height = (height*8//10) // 10
    cell_color = (20, 30, 80)  # Dark blue for solar cells
    
    for row in range(10):
        for col in range(8):
            cell_x = width//10 + col * cell_width
            cell_y = height//10 + row * cell_height
            draw.rectangle(
                [(cell_x, cell_y), 
                 (cell_x + cell_width - 2, cell_y + cell_height - 2)],
                fill=cell_color, outline=(0, 0, 0)
            )
    
    # Hinge mechanism
    hinge_color = get_random_color(metals)
    draw.rectangle(
        [(width//20, height*4//10), 
         (width//10, height*6//10)],
        fill=hinge_color, outline=(0, 0, 0)
    )
    
    # Power connector
    connector_color = get_random_color(highlights)
    draw.rectangle(
        [(width//20, height*4.5//10), 
         (width//40, height*5.5//10)],
        fill=connector_color, outline=(0, 0, 0)
    )
    
    # Add electrical traces
    for row in range(11):
        y_pos = height//10 + row * cell_height
        draw.line(
            [(width//10, y_pos), 
             (width*9//10, y_pos)],
            fill=(120, 120, 120), width=1
        )

def draw_landing_gear(draw, width, height, color_scheme):
    """Draw a landing gear component."""
    metals = color_scheme["metals"]
    highlights = color_scheme["highlights"]
    
    # Main strut
    strut_color = get_random_color(metals)
    draw.rectangle(
        [(width*4//10, height//10), 
         (width*6//10, height*8//10)],
        fill=strut_color, outline=(0, 0, 0)
    )
    
    # Wheel housing
    housing_color = get_random_color(metals)
    draw.rectangle(
        [(width*3//10, height*7//10), 
         (width*7//10, height*9//10)],
        fill=housing_color, outline=(0, 0, 0)
    )
    
    # Wheel
    wheel_color = (30, 30, 30)  # Black tire
    draw.ellipse(
        [(width*3.5//10, height*7.5//10), 
         (width*6.5//10, height*9.5//10)],
        fill=wheel_color, outline=(0, 0, 0)
    )
    
    # Wheel rim
    rim_color = get_random_color(metals)
    draw.ellipse(
        [(width*4.25//10, height*8.25//10), 
         (width*5.75//10, height*8.75//10)],
        fill=rim_color, outline=(0, 0, 0)
    )
    
    # Hydraulic cylinder
    cylinder_color = get_random_color(metals)
    draw.rectangle(
        [(width*2.5//10, height*3//10), 
         (width*3.5//10, height*6//10)],
        fill=cylinder_color, outline=(0, 0, 0)
    )
    
    # Hydraulic piston
    piston_color = get_random_color(highlights)
    draw.rectangle(
        [(width*2.75//10, height*2//10), 
         (width*3.25//10, height*3//10)],
        fill=piston_color, outline=(0, 0, 0)
    )
    
    # Linkage arms
    linkage_color = get_random_color(metals)
    # Upper linkage
    draw.line(
        [(width*3.5//10, height*4//10), 
         (width*4//10, height*3//10)],
        fill=linkage_color, width=5
    )
    # Lower linkage
    draw.line(
        [(width*3.5//10, height*5//10), 
         (width*4//10, height*6//10)],
        fill=linkage_color, width=5
    )

def draw_avionics(draw, width, height, color_scheme):
    """Draw an avionics component."""
    metals = color_scheme["metals"]
    composites = color_scheme["composites"]
    highlights = color_scheme["highlights"]
    
    # Main housing
    housing_color = get_random_color(metals)
    draw.rectangle(
        [(width//10, height//10), 
         (width*9//10, height*9//10)],
        fill=housing_color, outline=(0, 0, 0)
    )
    
    # Front panel
    panel_color = get_random_color(metals)
    draw.rectangle(
        [(width//10, height//10), 
         (width*9//10, height*2//10)],
        fill=panel_color, outline=(0, 0, 0)
    )
    
    # Circuit board
    pcb_color = get_random_color(composites)
    draw.rectangle(
        [(width*2//10, height*3//10), 
         (width*8//10, height*8//10)],
        fill=pcb_color, outline=(0, 0, 0)
    )
    
    # Electronic components
    draw_electronic_components(
        draw, 
        width*2//10, height*3//10, 
        width*8//10, height*8//10, 
        count=20, 
        colors=highlights
    )
    
    # Connectors
    connector_colors = highlights
    # Left side connectors
    for i in range(3):
        y_pos = height*(3 + i)//10
        draw.rectangle(
            [(width//10 - 10, y_pos), 
             (width//10, y_pos + height//20)],
            fill=get_random_color(connector_colors), outline=(0, 0, 0)
        )
    
    # Right side connectors
    for i in range(3):
        y_pos = height*(3 + i)//10
        draw.rectangle(
            [(width*9//10, y_pos), 
             (width*9//10 + 10, y_pos + height//20)],
            fill=get_random_color(connector_colors), outline=(0, 0, 0)
        )
    
    # Indicator LEDs on front panel
    for i in range(4):
        x_pos = width*(2 + 2*i)//10
        draw.ellipse(
            [(x_pos, height*1.25//10), 
             (x_pos + width//40, height*1.75//10)],
            fill=get_random_color(highlights), outline=(0, 0, 0)
        )

def draw_fuel_tank(draw, width, height, color_scheme):
    """Draw a fuel tank component."""
    metals = color_scheme["metals"]
    highlights = color_scheme["highlights"]
    
    # Main tank body
    tank_color = get_random_color(metals)
    draw.ellipse(
        [(width//4, height//10), 
         (width*3//4, height*9//10)],
        fill=tank_color, outline=(0, 0, 0)
    )
    
    # Pressure vessel ridges
    ridge_color = (
        max(0, tank_color[0]-20), 
        max(0, tank_color[1]-20), 
        max(0, tank_color[2]-20)
    )
    for i in range(1, 10):
        y_pos = height * i // 10
        draw.line(
            [(width//4, y_pos), 
             (width*3//4, y_pos)],
            fill=ridge_color, width=2
        )
    
    # Top valve/port
    valve_color = get_random_color(metals)
    draw.rectangle(
        [(width*2//5, height//20), 
         (width*3//5, height//10)],
        fill=valve_color, outline=(0, 0, 0)
    )
    
    # Bottom drain valve
    draw.rectangle(
        [(width*2//5, height*9//10), 
         (width*3//5, height*19//20)],
        fill=valve_color, outline=(0, 0, 0)
    )
    
    # Side port
    side_port_color = get_random_color(highlights)
    draw.ellipse(
        [(width*3//4 - 10, height*4//10), 
         (width*3//4 + 10, height*5//10)],
        fill=side_port_color, outline=(0, 0, 0)
    )
    
    # Level indicator
    indicator_color = get_random_color(highlights)
    draw.rectangle(
        [(width*3//4 - 5, height*2//10), 
         (width*3//4 + 5, height*8//10)],
        fill=(220, 220, 220), outline=(0, 0, 0)
    )
    
    # Fill indicator to random level
    fill_level = random.randint(3, 7)
    draw.rectangle(
        [(width*3//4 - 4, height*fill_level//10), 
         (width*3//4 + 4, height*8//10)],
        fill=indicator_color, outline=None
    )
