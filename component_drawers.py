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

def draw_heat_shield(draw, width, height, color_scheme):
    """Draw a heat shield component."""
    metals = color_scheme["metals"]
    composites = color_scheme["composites"]
    highlights = color_scheme["highlights"]
    
    # Main heat shield curved shape
    shield_color = get_random_color(composites)
    draw.arc(
        [(width//10, height//10), 
         (width*9//10, height*19//10)],
        180, 0, fill=shield_color, width=height//8
    )
    
    # Shield texture (ablative material)
    for i in range(20):
        x_pos = random.randint(width//5, width*4//5)
        y_pos = height - int(((x_pos - width//2)**2) / 1000) - random.randint(10, 30)
        texture_size = random.randint(5, 15)
        texture_color = create_variation(shield_color, 20)
        draw.ellipse(
            [(x_pos, y_pos), 
             (x_pos + texture_size, y_pos + texture_size)],
            fill=texture_color, outline=None
        )
    
    # Attachment points
    attachment_color = get_random_color(metals)
    for i in range(3):
        x_pos = width * (i+1) // 4
        y_pos = height // 5
        draw.rectangle(
            [(x_pos - 10, y_pos - 10), 
             (x_pos + 10, y_pos + 10)],
            fill=attachment_color, outline=(0, 0, 0)
        )
    
    # Temperature sensors
    sensor_color = get_random_color(highlights)
    for i in range(4):
        angle = pi * (0.3 + 0.15*i)
        radius = width * 0.4
        center_x = width // 2
        center_y = height * 1.7
        x_pos = int(center_x + radius * cos(angle))
        y_pos = int(center_y - radius * sin(angle))
        
        draw.ellipse(
            [(x_pos - 5, y_pos - 5), 
             (x_pos + 5, y_pos + 5)],
            fill=sensor_color, outline=(0, 0, 0)
        )
        # Wire to sensor
        draw.line(
            [(x_pos, y_pos), 
             (x_pos + random.randint(-30, 30), height // 5)],
            fill=(50, 50, 50), width=2
        )
    
    # Edge seal (around the perimeter)
    for angle in range(180, 361, 5):
        rad_angle = angle * pi / 180
        radius = width * 0.4
        center_x = width // 2
        center_y = height * 1.7
        x_pos = int(center_x + radius * cos(rad_angle))
        y_pos = int(center_y - radius * sin(rad_angle))
        
        draw.ellipse(
            [(x_pos - 2, y_pos - 2), 
             (x_pos + 2, y_pos + 2)],
            fill=(30, 30, 30), outline=None
        )

def draw_control_surface(draw, width, height, color_scheme):
    """Draw an aircraft control surface component."""
    metals = color_scheme["metals"]
    composites = color_scheme["composites"]
    
    # Main airfoil shape
    airfoil_color = get_random_color(composites)
    # Upper curve
    points = []
    for x in range(width//10, width*9//10, 10):
        # Airfoil curve approximation
        curve_height = int(height//3 * (1 - (2*(x/width - 0.5))**2))
        points.append((x, height//2 - curve_height))
    
    # Lower curve (reversed)
    for x in range(width*9//10, width//10, -10):
        curve_height = int(height//6 * (1 - (2*(x/width - 0.5))**2))
        points.append((x, height//2 + curve_height))
    
    draw.polygon(points, fill=airfoil_color, outline=(0, 0, 0))
    
    # Hinge line
    hinge_color = get_random_color(metals)
    draw.line(
        [(width*7//10, height//3), 
         (width*7//10, height*2//3)],
        fill=hinge_color, width=3
    )
    
    # Control surface (aileron/elevator/rudder)
    control_color = get_random_color(composites)
    control_points = []
    
    # Upper curve
    for x in range(width*7//10, width*9//10, 10):
        curve_height = int(height//3 * (1 - (2*(x/width - 0.5))**2))
        control_points.append((x, height//2 - curve_height))
    
    # Lower curve (reversed)
    for x in range(width*9//10, width*7//10, -10):
        curve_height = int(height//6 * (1 - (2*(x/width - 0.5))**2))
        control_points.append((x, height//2 + curve_height))
    
    draw.polygon(control_points, fill=control_color, outline=(0, 0, 0))
    
    # Actuator
    actuator_color = get_random_color(metals)
    draw.rectangle(
        [(width*6//10, height*5//12), 
         (width*7//10, height*7//12)],
        fill=actuator_color, outline=(0, 0, 0)
    )
    
    # Actuator arm
    arm_x = width * 8 // 10
    draw.line(
        [(width*7//10, height//2), 
         (arm_x, height//2)],
        fill=actuator_color, width=3
    )
    
    # Ribs
    rib_color = get_random_color(metals)
    for i in range(1, 6):
        x_pos = width * i // 6
        if x_pos < width*7//10:  # Only for main wing section
            upper_y = int(height//2 - height//3 * (1 - (2*(x_pos/width - 0.5))**2))
            lower_y = int(height//2 + height//6 * (1 - (2*(x_pos/width - 0.5))**2))
            draw.line(
                [(x_pos, upper_y), 
                 (x_pos, lower_y)],
                fill=rib_color, width=2
            )

def draw_propellant_valve(draw, width, height, color_scheme):
    """Draw a propellant valve component."""
    metals = color_scheme["metals"]
    highlights = color_scheme["highlights"]
    
    # Valve body
    body_color = get_random_color(metals)
    draw.rectangle(
        [(width//4, height//3), 
         (width*3//4, height*2//3)],
        fill=body_color, outline=(0, 0, 0)
    )
    
    # Inlet port (left)
    inlet_color = get_random_color(metals)
    draw.rectangle(
        [(width//8, height*2//5), 
         (width//4, height*3//5)],
        fill=inlet_color, outline=(0, 0, 0)
    )
    
    # Outlet port (right)
    outlet_color = get_random_color(metals)
    draw.rectangle(
        [(width*3//4, height*2//5), 
         (width*7//8, height*3//5)],
        fill=outlet_color, outline=(0, 0, 0)
    )
    
    # Actuator (top)
    actuator_color = get_random_color(metals)
    draw.rectangle(
        [(width*2//5, height//6), 
         (width*3//5, height//3)],
        fill=actuator_color, outline=(0, 0, 0)
    )
    
    # Solenoid coil
    solenoid_color = get_random_color(highlights)
    draw.ellipse(
        [(width*3//8, height//5), 
         (width*5//8, height*7//20)],
        fill=solenoid_color, outline=(0, 0, 0)
    )
    
    # Valve internals (simplified)
    valve_color = get_random_color(highlights)
    # Flow path
    draw.rectangle(
        [(width//4, height*9//20), 
         (width*3//4, height*11//20)],
        fill=(220, 220, 220), outline=None
    )
    
    # Valve position - randomly open or closed
    if random.random() < 0.5:  # Open
        draw.rectangle(
            [(width*7//16, height//3), 
             (width*9//16, height*3//5)],
            fill=valve_color, outline=(0, 0, 0)
        )
    else:  # Closed
        draw.rectangle(
            [(width*7//16, height//3), 
             (width*9//16, height*1//2)],
            fill=valve_color, outline=(0, 0, 0)
        )
        # Closed valve blocks flow
        draw.rectangle(
            [(width*3//8, height*9//20), 
             (width*5//8, height*11//20)],
            fill=valve_color, outline=None
        )
    
    # Pressure gauge
    gauge_color = (220, 220, 220)
    draw.ellipse(
        [(width*5//8, height*2//3), 
         (width*3//4, height*5//6)],
        fill=gauge_color, outline=(0, 0, 0)
    )
    
    # Gauge needle
    needle_angle = random.random() * pi * 0.8 + pi * 0.1  # Between 0.1π and 0.9π
    center_x = width * 11 // 16
    center_y = height * 3 // 4
    end_x = center_x + int(width//16 * cos(needle_angle))
    end_y = center_y - int(width//16 * sin(needle_angle))
    draw.line(
        [(center_x, center_y), 
         (end_x, end_y)],
        fill=(255, 0, 0), width=2
    )

def draw_payload_fairing(draw, width, height, color_scheme):
    """Draw a payload fairing component."""
    metals = color_scheme["metals"]
    composites = color_scheme["composites"]
    
    # Fairing half (simplified)
    fairing_color = get_random_color(composites)
    
    # Draw a half-ellipse for the fairing
    points = []
    center_x = width // 2
    
    # Top arc
    for x in range(width//10, width*9//10, 10):
        # Calculate y based on an ellipse formula
        rel_x = (x - center_x) / (width*4//10)
        if abs(rel_x) <= 1:
            y = int(height*8//10 * (1 - rel_x**2)**0.5)
            points.append((x, height//10 + y))
    
    # Bottom line
    points.append((width*9//10, height*9//10))
    points.append((width//10, height*9//10))
    
    draw.polygon(points, fill=fairing_color, outline=(0, 0, 0))
    
    # Separation line
    sep_color = get_random_color(metals)
    draw.line(
        [(center_x, height//10), 
         (center_x, height*9//10)],
        fill=sep_color, width=3
    )
    
    # Separation system (pyrotechnic cord)
    pyro_color = random.choice([(255, 80, 0), (240, 240, 0)])
    for i in range(1, 9):
        y_pos = height * i // 10
        draw.ellipse(
            [(center_x - 5, y_pos - 5), 
             (center_x + 5, y_pos + 5)],
            fill=pyro_color, outline=(0, 0, 0)
        )
    
    # Acoustic blanket pattern
    blanket_color = (
        min(255, fairing_color[0]+30),
        min(255, fairing_color[1]+30),
        min(255, fairing_color[2]+30)
    )
    for i in range(20):
        x_pos = random.randint(width//8, width*7//8)
        if abs(x_pos - center_x) < 20:  # Don't draw too close to separation line
            continue
        y_pos = random.randint(height//8, height*7//8)
        size = random.randint(10, 30)
        draw.rectangle(
            [(x_pos, y_pos), 
             (x_pos + size, y_pos + size)],
            fill=blanket_color, outline=None
        )
    
    # Access port
    port_color = get_random_color(metals)
    if random.random() < 0.5:  # Left side
        port_x = width//4
    else:  # Right side
        port_x = width*3//4
            
    port_y = height//2
    draw.ellipse(
        [(port_x - 20, port_y - 20), 
         (port_x + 20, port_y + 20)],
        fill=port_color, outline=(0, 0, 0)
    )
    
    # Vent holes
    vent_color = (50, 50, 50)
    for i in range(3):
        if random.random() < 0.5:  # Left side
            vent_x = width//4 + random.randint(-30, 30)
        else:  # Right side
            vent_x = width*3//4 + random.randint(-30, 30)
                
        vent_y = height * (i+1) // 4
        vent_size = random.randint(5, 10)
        draw.ellipse(
            [(vent_x - vent_size, vent_y - vent_size), 
             (vent_x + vent_size, vent_y + vent_size)],
            fill=vent_color, outline=(0, 0, 0)
        )

def draw_docking_mechanism(draw, width, height, color_scheme):
    """Draw a docking mechanism component."""
    metals = color_scheme["metals"]
    highlights = color_scheme["highlights"]
    
    # Main docking ring
    ring_color = get_random_color(metals)
    draw.ellipse(
        [(width//4, height//4), 
         (width*3//4, height*3//4)],
        fill=None, outline=ring_color, width=10
    )
    
    # Inner mechanism
    inner_color = get_random_color(metals)
    draw.ellipse(
        [(width*3//8, height*3//8), 
         (width*5//8, height*5//8)],
        fill=inner_color, outline=(0, 0, 0)
    )
    
    # Alignment guides
    guide_color = get_random_color(highlights)
    for i in range(4):
        angle = i * pi / 2
        guide_x = width//2 + int(width*3//10 * cos(angle))
        guide_y = height//2 + int(height*3//10 * sin(angle))
        
        draw.ellipse(
            [(guide_x - 10, guide_y - 10), 
             (guide_x + 10, guide_y + 10)],
            fill=guide_color, outline=(0, 0, 0)
        )
    
    # Latches
    latch_color = get_random_color(metals)
    for i in range(8):
        angle = i * pi / 4
        latch_x = width//2 + int(width*2//8 * cos(angle))
        latch_y = height//2 + int(height*2//8 * sin(angle))
        
        # Latch base
        draw.rectangle(
            [(latch_x - 8, latch_y - 8), 
             (latch_x + 8, latch_y + 8)],
            fill=latch_color, outline=(0, 0, 0)
        )
        
        # Latch arm
        arm_end_x = latch_x + int(15 * cos(angle))
        arm_end_y = latch_y + int(15 * sin(angle))
        draw.line(
            [(latch_x, latch_y), 
             (arm_end_x, arm_end_y)],
            fill=latch_color, width=4
        )
    
    # Electrical connectors
    connector_color = get_random_color(highlights)
    connector_positions = [
        (width//2, height*3//4 - 10),
        (width//2, height//4 + 10),
        (width*3//4 - 10, height//2),
        (width//4 + 10, height//2)
    ]
    
    for pos in connector_positions:
        draw.rectangle(
            [(pos[0] - 7, pos[1] - 7), 
             (pos[0] + 7, pos[1] + 7)],
            fill=connector_color, outline=(0, 0, 0)
        )
    
    # Seal
    seal_color = (50, 50, 50)  # Dark gray
    draw.ellipse(
        [(width*5//16, height*5//16), 
         (width*11//16, height*11//16)],
        fill=None, outline=seal_color, width=3
    )
    
    # Shock attenuators (springs)
    spring_color = get_random_color(metals)
    for i in range(4):
        angle = i * pi / 2 + pi/4
        spring_x = width//2 + int(width*5//16 * cos(angle))
        spring_y = height//2 + int(height*5//16 * sin(angle))
        
        # Draw spring (simplified)
        center_x = spring_x
        center_y = spring_y
        for j in range(3):
            radius = 5 + j*3
            draw.ellipse(
                [(center_x - radius, center_y - radius), 
                 (center_x + radius, center_y + radius)],
                fill=None, outline=spring_color, width=2
            )
