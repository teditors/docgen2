"""
Configuration module for the Aerospace Test Directory Generator.

This module contains all configuration settings and constants used throughout the application.
"""

import os
from pathlib import Path

# Base directory configuration
DEFAULT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(DEFAULT_BASE_DIR, "testbed")

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_FILE = os.path.join(DEFAULT_BASE_DIR, "generator.log")

# Company name components for generating realistic company names
COMPANY_NAME_PREFIXES = [
    "Advanced", "Precision", "Dynamic", "Orbital", "Stellar", "Quantum", "Integrated", 
    "Alpha", "Global", "NextGen", "Innovative", "Strategic", "Universal", "Apex",
    "Aero", "Cosmic", "Frontier", "Pioneer", "Elite", "Astro", "Skyward", "Prime"
]

COMPANY_NAME_MIDS = [
    "Aerospace", "Propulsion", "Systems", "Engineering", "Technologies", "Dynamics",
    "Materials", "Structures", "Aviation", "Defense", "Space", "Rocket", "Composite",
    "Flight", "Orbital", "Satellite", "Avionics", "Launch", "Payload", "Propellant"
]

COMPANY_NAME_SUFFIXES = [
    "Solutions", "Industries", "Corporation", "Systems", "Services", "Technologies",
    "Group", "Associates", "International", "Enterprises", "Labs", "Works", "Innovations",
    "Dynamics", "Research", "Designs", "Partners", "Alliance", "Aerospace", "Engineering"
]

# Test project themes for consistency across a project
TEST_THEMES = [
    {
        "name": "Rocket Engine",
        "components": ["Nozzle", "Combustion Chamber", "Turbopump", "Igniter", "Fuel Injector", "Gas Generator", "Thrust Vector Control"],
        "data_descriptions": ["Thrust", "Temperature", "Pressure", "Vibration", "Flow Rate", "Ignition Sequence", "Combustion Stability"],
        "specifications": ["SN-RE-001", "MIL-STD-1540C", "NASA-STD-5012", "AIAA-S-120"],
        "materials": ["Inconel 718", "RP-1", "Liquid Oxygen", "GRCop-84", "Haynes 230"],
        "test_procedures": ["Hot Fire Test", "Cold Flow Test", "Ignition Test", "Throttle Response Test", "Endurance Test"],
        "project_stakeholders": ["Propulsion Division", "Flight Dynamics Team", "Mission Assurance", "Safety Committee", "Launch Operations"]
    },
    {
        "name": "Satellite Solar Panel",
        "components": ["PV Array", "Deployment Mechanism", "Power Regulator", "Thermal Control", "Junction Box", "Hinges", "Drive Motor"],
        "data_descriptions": ["Power Output", "Deployment Angle", "Temperature Cycling", "Radiation Exposure", "Efficiency", "Current-Voltage Curve"],
        "specifications": ["SN-SP-102", "AIAA-S-111", "ECSS-E-ST-20-08C", "MIL-STD-810G"],
        "materials": ["Gallium Arsenide", "Aluminum Honeycomb", "Kapton Film", "Silver Interconnects", "Composite Substrate"],
        "test_procedures": ["Solar Simulation Test", "Deployment Test", "Thermal Vacuum Cycling", "Vibration Survey", "Power Output Verification"],
        "project_stakeholders": ["Power Systems Group", "Structural Team", "Mission Planning", "Thermal Engineering", "Electrical Systems"]
    },
    {
        "name": "Landing Gear",
        "components": ["Strut", "Actuator", "Wheel Assembly", "Brake System", "Shock Absorber", "Toggle Links", "Lock Mechanism"],
        "data_descriptions": ["Load Test", "Deployment Time", "Shock Response", "Fatigue Test", "Brake Performance", "Retraction Force"],
        "specifications": ["SN-LG-045", "AMS 4911", "MIL-STD-1553B", "SAE AS8084", "FAR Part 25"],
        "materials": ["7075-T6 Aluminum", "300M Steel", "Titanium 6Al-4V", "Carbon Fiber Composite", "Hydraulic Fluid MIL-PRF-83282"],
        "test_procedures": ["Drop Test", "Cycle Life Test", "Ultimate Load Test", "Brake Dynamometer Test", "Low Temperature Operation Test"],
        "project_stakeholders": ["Landing Systems", "Structures Division", "Flight Test Group", "Certification Team", "Weight Engineering"]
    },
    {
        "name": "Avionics System",
        "components": ["Flight Computer", "Navigation Unit", "Communication System", "Power Distribution", "Sensor Array", "Data Bus", "Control Interface"],
        "data_descriptions": ["Signal Integrity", "Processor Load", "Power Consumption", "Heat Dissipation", "Data Throughput", "Latency", "Bit Error Rate"],
        "specifications": ["SN-AV-213", "DO-178C", "DO-254", "MIL-STD-1553B", "ARINC 429"],
        "materials": ["FR-4 PCB", "Gold-Plated Connectors", "Radiation-Hardened ICs", "Conformal Coating", "EMI Shielding Materials"],
        "test_procedures": ["Software Validation", "EMI/EMC Test", "Hardware-in-Loop Simulation", "Power Quality Test", "Thermal Survey"],
        "project_stakeholders": ["Software Team", "Hardware Design", "Systems Integration", "Flight Control", "Operations Team"]
    },
    {
        "name": "Fuel Tank",
        "components": ["Tank Shell", "Baffles", "Fuel Pickup", "Pressure Relief Valve", "Feed Line", "Level Sensor", "Fill/Drain Valve"],
        "data_descriptions": ["Pressure Test", "Slosh Dynamics", "Temperature Gradient", "Fill/Drain Rate", "Leak Detection", "Expulsion Efficiency"],
        "specifications": ["SN-FT-078", "ASME BPVC", "NASA-STD-5009", "MIL-DTL-5624U", "SAE AS1225"],
        "materials": ["2219 Aluminum", "Titanium 6Al-4V", "Inconel 718", "PTFE Seals", "Stainless Steel 321"],
        "test_procedures": ["Hydrostatic Test", "Slosh Test", "Proof Pressure Test", "Leak Test", "Expulsion Test", "Thermal Cycling"],
        "project_stakeholders": ["Propulsion Division", "Structural Design", "Materials Group", "Fluid Dynamics Team", "Safety Committee"]
    },
    {
        "name": "Heat Shield",
        "components": ["Ablative Layer", "Structural Support", "Temperature Sensor", "Attachment Points", "Edge Seals", "Thermal Insulation", "Gap Fillers"],
        "data_descriptions": ["Thermal Protection", "Ablation Rate", "Structural Integrity", "Temperature Profile", "Weight Loss", "Heat Flux"],
        "specifications": ["SN-HS-056", "NASA-STD-6016", "ASTM E285", "MIL-STD-810G", "ECSS-E-ST-31-02C"],
        "materials": ["PICA", "SLA-561V", "Carbon Phenolic", "RTV Silicone", "Ceramic Matrix Composite", "Nomex Felt"],
        "test_procedures": ["Arc Jet Test", "Thermal Vacuum Test", "Mechanical Loading Test", "Acoustic Test", "Thermal Response Test"],
        "project_stakeholders": ["Thermal Protection Systems", "Entry Systems", "Materials Research", "Structural Analysis", "Mission Planning"]
    },
    {
        "name": "Control Surface",
        "components": ["Aileron", "Actuator", "Hinge Mechanism", "Control Linkage", "Deflection Limiter", "Balance Weight", "Servo Controller"],
        "data_descriptions": ["Deflection Angle", "Response Time", "Flutter Test", "Load Distribution", "Position Accuracy", "Hinge Moment"],
        "specifications": ["SN-CS-189", "MIL-DTL-5687", "RTCA DO-160G", "SAE ARP1070", "FAR 25.629"],
        "materials": ["2024-T3 Aluminum", "Composite Skin", "Titanium Hinges", "Stainless Steel Fasteners", "Aerodynamic Fairings"],
        "test_procedures": ["Flutter Test", "Endurance Cycling", "Stiffness Test", "Deflection Test", "Failure Mode Test", "Environmental Exposure"],
        "project_stakeholders": ["Aerodynamics Team", "Flight Controls", "Structural Test", "Manufacturing Engineering", "Certification Group"]
    },
    {
        "name": "Propellant Valve",
        "components": ["Valve Body", "Actuator", "Seals", "Pressure Sensor", "Flow Restrictor", "Solenoid", "Thermal Conditioner"],
        "data_descriptions": ["Flow Rate", "Opening Time", "Leakage Test", "Pressure Drop", "Cycle Life", "Response Curve", "Power Requirement"],
        "specifications": ["SN-PV-042", "MIL-V-24520", "AIAA S-080-1998", "SAE AS4842", "NASA-STD-5001"],
        "materials": ["Inconel 718", "Viton Seals", "Kel-F Seats", "Cobalt Alloy", "304L Stainless Steel"],
        "test_procedures": ["Proof Pressure Test", "Flow Calibration", "Life Cycle Test", "Cryogenic Compatibility", "Response Time Measurement"],
        "project_stakeholders": ["Propulsion Systems", "Component Engineering", "Test Operations", "Quality Assurance", "Supplier Management"]
    },
    {
        "name": "Payload Fairing",
        "components": ["Composite Shell", "Separation System", "Acoustic Blanket", "Vents", "Access Ports", "RF Transparent Window", "Jettison Controller"],
        "data_descriptions": ["Separation Test", "Acoustic Transmission", "Thermal Profile", "Venting Performance", "Structural Load", "Shock Levels"],
        "specifications": ["SN-PF-117", "MIL-STD-1540D", "NASA-STD-5002", "ECSS-E-ST-32-01C", "AIAA S-110"],
        "materials": ["Carbon Fiber Composite", "Honeycomb Core", "Acoustic Damping Material", "Pyrotechnic Devices", "Thermal Insulation"],
        "test_procedures": ["Static Load Test", "Acoustic Test", "Separation Test", "Thermal Balance Test", "Modal Survey"],
        "project_stakeholders": ["Structures Division", "Acoustic Analysis", "Payload Integration", "Launch Operations", "Systems Engineering"]
    },
    {
        "name": "Docking Mechanism",
        "components": ["Capture System", "Alignment Guides", "Latches", "Seals", "Electrical Connectors", "Shock Attenuators", "Control Electronics"],
        "data_descriptions": ["Capture Envelope", "Alignment Accuracy", "Latch Strength", "Seal Compression", "Connection Test", "Shock Absorption"],
        "specifications": ["SN-DM-095", "NASA-STD-3000", "GOST R 50804-95", "ISO 11227", "ECSS-E-ST-33-11C"],
        "materials": ["AISI 321 Stainless Steel", "Titanium Alloy", "Kapton Multilayer Insulation", "Elastomeric Seals", "Gold-Plated Contacts"],
        "test_procedures": ["Soft Capture Test", "Hard Dock Test", "Misalignment Test", "Leak Test", "Electrical Continuity Test", "Cycle Life Test"],
        "project_stakeholders": ["Docking Systems", "GNC Team", "Crew Systems", "International Partners", "Mission Operations"]
    }
]

# Test types and their common measurements
TEST_TYPES = {
    "Dynamics": [
        "Vibration", "Shock", "Modal Analysis", "Acoustic", "Random Vibration", 
        "Sine Sweep", "Structural Resonance", "Damping Factor", "Harmonic Response", "Impulse Response"
    ],
    "EMIEMC": [
        "Conducted Emissions", "Radiated Emissions", "Susceptibility", "ESD", "Lightning",
        "Signal Integrity", "Crosstalk", "Radiated Immunity", "Power Quality", "Transient Response"
    ],
    "Environmental": [
        "Thermal Cycling", "Vacuum", "Salt Fog", "Humidity", "Altitude",
        "Solar Radiation", "Sand and Dust", "Fungus Resistance", "Explosive Atmosphere", "Rain and Icing"
    ]
}

# PDF generation content
PO_SECTIONS = [
    "Purchase Order Information",
    "Vendor Information",
    "Technical Requirements",
    "Quality Assurance Requirements",
    "Shipping Instructions",
    "Terms and Conditions"
]

QUOTE_SECTIONS = [
    "Executive Summary",
    "Scope of Work",
    "Technical Approach",
    "Schedule",
    "Cost Breakdown",
    "Terms and Conditions"
]

SPEC_SECTIONS = [
    "Scope",
    "Applicable Documents",
    "Requirements",
    "Verification",
    "Materials and Processes",
    "Quality Assurance",
    "Testing and Acceptance"
]

NOD_SECTIONS = [
    "Notice Of Deviation",
    "Affected Requirements",
    "Description of Deviation",
    "Technical Justification",
    "Impact Assessment",
    "Disposition and Approval"
]

# Business terms for document generation
BUSINESS_TERMS = {
    "payment_terms": ["Net 30", "Net 45", "Net 60", "50% upfront, 50% on delivery"],
    "delivery_terms": ["FOB Origin", "FOB Destination", "Ex Works", "CIF"],
    "quality_standards": ["ISO 9001", "AS9100D", "NASA-STD-8739.6", "MIL-STD-45662A"],
    "acceptance_criteria": ["Visual Inspection", "Functional Test", "Dimensional Inspection", "Performance Test"],
    "warranty_periods": ["12 months", "18 months", "24 months", "36 months"]
}

def sanitize_themes():
    """
    Sanitize all component names, data descriptions, and other theme elements
    to ensure they don't contain characters that would create invalid file paths.
    
    This function should be called at the bottom of the config.py file.
    """
    for theme in TEST_THEMES:
        # Sanitize component names
        theme['components'] = [component.replace('/', '-').replace('\\', '-') 
                               for component in theme['components']]
        
        # Sanitize data descriptions
        theme['data_descriptions'] = [desc.replace('/', '-').replace('\\', '-') 
                                      for desc in theme['data_descriptions']]
        
        # Sanitize specifications
        theme['specifications'] = [spec.replace('/', '-').replace('\\', '-') 
                                  for spec in theme['specifications']]
        
        # Sanitize materials
        theme['materials'] = [material.replace('/', '-').replace('\\', '-') 
                             for material in theme['materials']]
        
        # Sanitize test procedures
        theme['test_procedures'] = [proc.replace('/', '-').replace('\\', '-') 
                                   for proc in theme['test_procedures']]
        
        # Sanitize project stakeholders
        theme['project_stakeholders'] = [stake.replace('/', '-').replace('\\', '-') 
                                        for stake in theme['project_stakeholders']]

# Run the sanitization function
sanitize_themes()

# Also sanitize test types
for test_type, measurements in TEST_TYPES.items():
    TEST_TYPES[test_type] = [measurement.replace('/', '-').replace('\\', '-') 
                            for measurement in measurements]