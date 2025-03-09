"""
Configuration settings for the hardware image generator.
"""

# Color schemes for different component types
COLOR_SCHEMES = {
    "aerospace": {
        "metals": [(192, 192, 192), (160, 160, 160), (120, 120, 120), (100, 100, 100)],  # Silver/aluminum
        "composites": [(50, 50, 50), (30, 30, 30), (20, 20, 20)],  # Carbon fiber black
        "highlights": [(0, 102, 204), (0, 51, 153), (255, 102, 0), (204, 0, 0)],  # Blue/orange/red
        "labels": [(255, 255, 0), (255, 102, 0), (0, 204, 0)]  # Yellow/orange/green
    },
    "engine": {
        "metals": [(100, 100, 100), (80, 80, 80), (60, 60, 60)],  # Darker metals
        "composites": [(50, 30, 10), (40, 25, 5), (30, 20, 5)],  # Brown/tan
        "highlights": [(255, 60, 0), (200, 40, 0), (150, 30, 0)],  # Fire/heat colors
        "labels": [(255, 240, 0), (240, 240, 240)]  # Yellow/white
    },
    "electronic": {
        "metals": [(220, 220, 220), (180, 180, 180)],  # Light metals
        "composites": [(0, 50, 0), (0, 30, 0), (0, 20, 0)],  # Green PCB
        "highlights": [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)],  # LED colors
        "labels": [(255, 255, 255), (0, 0, 0)]  # White/black
    }
}

# Component type mapping - maps keywords to drawer functions and color schemes
COMPONENT_TYPE_MAPPING = {
    "engine": {
        "keywords": ["engine", "nozzle", "combustion", "turbopump", "propulsion", "thruster"],
        "drawer": "rocket_engine",
        "color_scheme": "engine"
    },
    "solar_panel": {
        "keywords": ["solar", "panel", "array", "pv", "photovoltaic"],
        "drawer": "solar_panel",
        "color_scheme": "aerospace"
    },
    "landing_gear": {
        "keywords": ["landing", "gear", "wheel", "strut", "shock", "absorber"],
        "drawer": "landing_gear",
        "color_scheme": "aerospace"
    },
    "avionics": {
        "keywords": ["avionics", "computer", "electronic", "controller", "circuit", "board"],
        "drawer": "avionics",
        "color_scheme": "electronic"
    },
    "fuel_tank": {
        "keywords": ["tank", "fuel", "propellant", "storage", "container"],
        "drawer": "fuel_tank",
        "color_scheme": "aerospace"
    },
    "heat_shield": {
        "keywords": ["heat", "shield", "thermal", "ablative", "protection"],
        "drawer": "heat_shield",
        "color_scheme": "aerospace"
    },
    "control_surface": {
        "keywords": ["control", "surface", "aileron", "rudder", "elevator", "flap"],
        "drawer": "control_surface",
        "color_scheme": "aerospace"
    },
    "valve": {
        "keywords": ["valve", "regulator", "flow", "control", "relief", "check"],
        "drawer": "propellant_valve",
        "color_scheme": "aerospace"
    },
    "fairing": {
        "keywords": ["fairing", "payload", "shroud", "nose", "cone", "cowling"],
        "drawer": "payload_fairing",
        "color_scheme": "aerospace"
    },
    "docking": {
        "keywords": ["dock", "latch", "mechanism", "capture", "port", "berthing"],
        "drawer": "docking_mechanism",
        "color_scheme": "aerospace"
    }
}

# Default image sizes
IMAGE_SIZES = {
    "landscape": (800, 600),
    "portrait": (600, 800)
}

# Default background color
DEFAULT_BACKGROUND = (240, 240, 240)  # Light gray

# Default border settings
BORDER_SETTINGS = {
    "color": (0, 0, 0),  # Black
    "width": 2
}

# Font settings
FONT_SETTINGS = {
    "size": 20,
    "color": (0, 0, 0),  # Black
    "default_font": "arial.ttf",
    "y_position": 30  # Distance from bottom
}
