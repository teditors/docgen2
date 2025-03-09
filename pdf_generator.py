"""
PDF Document Generator Module

This module handles the generation of fake PDF documents with realistic content.
"""

import os
import random
import datetime
import logging
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch

# Import configuration
from config import (
    TEST_THEMES,
    PO_SECTIONS, 
    QUOTE_SECTIONS, 
    SPEC_SECTIONS, 
    NOD_SECTIONS,
    BUSINESS_TERMS
)

class PDFGenerator:
    """Class for generating realistic PDF documents."""
    
    def __init__(self, logger):
        """Initialize the PDF generator."""
        self.logger = logger
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()
    
    def _init_custom_styles(self):
        """Initialize custom paragraph styles."""
        # Instead of trying to add a style named 'Title', which already exists,
        # we'll create a custom style with a different name
        self.styles.add(ParagraphStyle(
            name='DocumentTitle',  # Changed from 'Title' to 'DocumentTitle'
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=1,  # Center alignment
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='Section',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='DocumentNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
    
    def create_purchase_order(self, filepath, filename, project_theme):
        """Create a realistic purchase order PDF."""
        self.logger.info(f"Creating purchase order PDF: {filename}")
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title (using our custom DocumentTitle style instead of Title)
        elements.append(Paragraph(f"PURCHASE ORDER: {filename}", self.styles['DocumentTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add date and PO information
        current_date = datetime.datetime.now()
        elements.append(Paragraph(f"Date: {current_date.strftime('%B %d, %Y')}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Project: {project_theme['name']}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Specification Reference: {random.choice(project_theme['specifications'])}", self.styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section
        for section in PO_SECTIONS:
            elements.append(Paragraph(section, self.styles['Section']))
            
            # Generate different content for each section
            if section == "Purchase Order Information":
                content = f"""
                Order Number: {filename}
                Date Required: {(current_date + datetime.timedelta(days=random.randint(30, 180))).strftime('%B %d, %Y')}
                Priority: {random.choice(['Standard', 'High', 'Critical'])}
                Procurement Category: Aerospace Components
                """
            
            elif section == "Vendor Information":
                content = f"""
                Vendor: {random.choice(['Precision Aerospace Supply', 'Advanced Materials Co.', 'SpaceTech Industries', 'Orbital Components Inc.'])}
                Contact: {random.choice(['John Smith', 'Sarah Johnson', 'Robert Chen', 'Maria Rodriguez'])}
                Phone: (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}
                Email: contact@vendor-{random.randint(100, 999)}.com
                """
            
            elif section == "Technical Requirements":
                components = ", ".join(random.sample(project_theme['components'], min(3, len(project_theme['components']))))
                materials = ", ".join(random.sample(project_theme['materials'], min(3, len(project_theme['materials']))))
                
                content = f"""
                Components: {components}
                Materials: {materials}
                Quantity: {random.randint(1, 10)} units
                Drawing Reference: DWG-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C', 'D'])}
                """
            
            elif section == "Quality Assurance Requirements":
                content = f"""
                Quality Standard: {random.choice(BUSINESS_TERMS['quality_standards'])}
                Inspection Level: {random.choice(['Level I', 'Level II', 'Level III'])}
                Documentation Required: Material Certificates, Test Reports, Certificate of Conformance
                Special Requirements: {random.choice(['None', 'First Article Inspection', 'Source Inspection', 'Lot Traceability'])}
                """
            
            elif section == "Shipping Instructions":
                content = f"""
                Delivery Terms: {random.choice(BUSINESS_TERMS['delivery_terms'])}
                Carrier: {random.choice(['FedEx', 'UPS', 'DHL', 'Specialized Freight'])}
                Packaging: {random.choice(['Standard', 'Custom Protective', 'Clean Room', 'Anti-Static'])}
                Shipping Address: 1234 Aerospace Way, Engineering Building {random.randint(1, 20)}, Room {random.randint(100, 999)}
                """
            
            elif section == "Terms and Conditions":
                content = f"""
                Payment Terms: {random.choice(BUSINESS_TERMS['payment_terms'])}
                Warranty: {random.choice(BUSINESS_TERMS['warranty_periods'])}
                Acceptance Criteria: {random.choice(BUSINESS_TERMS['acceptance_criteria'])}
                Confidentiality: All technical information related to this purchase order is confidential and proprietary.
                """
            
            elements.append(Paragraph(content, self.styles['DocumentNormal']))
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("APPROVALS", self.styles['Section']))
        
        data = [
            ["Procurement Officer", "Technical Authority", "Quality Assurance"],
            ["________________", "________________", "________________"],
            [f"Date: __/__/____", f"Date: __/__/____", f"Date: __/__/____"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        elements.append(t)
        
        # Build the PDF
        doc.build(elements)
        self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
    
    def create_quote(self, filepath, filename, project_theme):
        """Create a realistic quote PDF."""
        self.logger.info(f"Creating quote PDF: {filename}")
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title and company info (using DocumentTitle instead of Title)
        elements.append(Paragraph(f"QUOTATION: {filename}", self.styles['DocumentTitle']))
        company_name = f"{random.choice(['Precision', 'Advanced', 'Stellar', 'Orbital'])} {random.choice(['Aerospace', 'Technologies', 'Engineering', 'Systems'])}"
        elements.append(Paragraph(company_name, self.styles['DocumentNormal']))
        elements.append(Paragraph(f"123 Technology Lane, Suite {random.randint(100, 999)}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Aerospace Park, CA {random.randint(90000, 96000)}", self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add date and quote information
        current_date = datetime.datetime.now()
        valid_until = current_date + datetime.timedelta(days=random.randint(30, 90))
        elements.append(Paragraph(f"Date: {current_date.strftime('%B %d, %Y')}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Valid Until: {valid_until.strftime('%B %d, %Y')}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Project: {project_theme['name']}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Customer Reference: CR-{random.randint(10000, 99999)}", self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section
        for section in QUOTE_SECTIONS:
            elements.append(Paragraph(section, self.styles['Section']))
            
            # Generate different content for each section
            if section == "Executive Summary":
                content = f"""
                {company_name} is pleased to present this quotation for the {project_theme['name']} project. 
                This quote covers the {random.choice(['design', 'manufacturing', 'testing', 'certification'])} 
                of {random.choice(project_theme['components'])} components that meet or exceed the requirements 
                specified in {random.choice(project_theme['specifications'])}.
                Our team has extensive experience with similar aerospace applications and is committed to 
                delivering high-quality products that meet your schedule and performance requirements.
                """
            
            elif section == "Scope of Work":
                components = ", ".join(random.sample(project_theme['components'], min(4, len(project_theme['components']))))
                test_procedures = ", ".join(random.sample(project_theme['test_procedures'], min(3, len(project_theme['test_procedures']))))
                
                content = f"""
                This quotation includes the following scope:
                - Engineering analysis and design optimization for {components}
                - Material procurement and quality verification
                - Manufacturing and assembly of {random.randint(1, 5)} units
                - Testing per {test_procedures}
                - Documentation package including test reports and material certifications
                - {random.choice(['2', '3', '4'])} technical review meetings with customer representatives
                """
            
            elif section == "Technical Approach":
                content = f"""
                Our approach for this project includes:
                
                - Using {random.choice(project_theme['materials'])} material qualified to {random.choice(project_theme['specifications'])}
                - Implementing {random.choice(['advanced manufacturing techniques', 'proprietary process controls', 'specialized tooling'])} to ensure consistent quality
                - Conducting {random.choice(project_theme['test_procedures'])} according to industry standards
                - Performing all work in our {random.choice(['ISO 9001', 'AS9100D'])} certified facility
                - Providing traceability for all materials and processes
                """
            
            elif section == "Schedule":
                start_date = current_date + datetime.timedelta(days=random.randint(7, 21))
                design_duration = random.randint(2, 6)
                manufacturing_duration = random.randint(4, 12)
                testing_duration = random.randint(2, 6)
                delivery_date = start_date + datetime.timedelta(weeks=(design_duration + manufacturing_duration + testing_duration))
                
                content = f"""
                Preliminary Schedule:
                - Project Start: {start_date.strftime('%B %d, %Y')}
                - Design Phase: {design_duration} weeks
                - Manufacturing: {manufacturing_duration} weeks
                - Testing: {testing_duration} weeks
                - Final Delivery: {delivery_date.strftime('%B %d, %Y')}
                
                This schedule assumes timely customer reviews and approvals at key milestones.
                """
            
            elif section == "Cost Breakdown":
                engineering = random.randint(20, 80) * 1000
                materials = random.randint(15, 60) * 1000
                manufacturing = random.randint(30, 100) * 1000
                testing = random.randint(10, 40) * 1000
                documentation = random.randint(5, 15) * 1000
                total = engineering + materials + manufacturing + testing + documentation
                
                data = [
                    ["Item", "Cost (USD)"],
                    ["Engineering", f"${engineering:,}"],
                    ["Materials", f"${materials:,}"],
                    ["Manufacturing", f"${manufacturing:,}"],
                    ["Testing", f"${testing:,}"],
                    ["Documentation", f"${documentation:,}"],
                    ["Total", f"${total:,}"]
                ]
                
                t = Table(data, colWidths=[4*inch, 2*inch])
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ]))
                
                elements.append(t)
                content = ""  # Skip adding paragraph since we're using a table
            
            elif section == "Terms and Conditions":
                content = f"""
                Payment Terms: {random.choice(BUSINESS_TERMS['payment_terms'])}
                Delivery: {random.choice(BUSINESS_TERMS['delivery_terms'])}
                Warranty: {random.choice(BUSINESS_TERMS['warranty_periods'])} from date of delivery
                Validity: This quote is valid for {random.randint(30, 90)} days from the date of issue
                
                This quotation is subject to our standard terms and conditions, which are available upon request.
                All technical information provided in this quote is considered proprietary and confidential.
                """
            
            # Only add the paragraph if there's content (skip if we used a table)
            if content:
                elements.append(Paragraph(content, self.styles['DocumentNormal']))
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add contact information
        elements.append(Spacer(1, 0.25 * inch))
        elements.append(Paragraph("CONTACT INFORMATION", self.styles['Section']))
        elements.append(Paragraph(f"Primary Contact: {random.choice(['John Smith', 'Sarah Johnson', 'Robert Chen', 'Maria Rodriguez'])}", self.styles['Normal']))
        elements.append(Paragraph(f"Title: {random.choice(['Sales Engineer', 'Project Manager', 'Business Development Manager', 'Technical Director'])}", self.styles['Normal']))
        elements.append(Paragraph(f"Phone: (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Email: contact@{company_name.lower().replace(' ', '')}.com", self.styles['DocumentNormal']))
        
        # Build the PDF
        doc.build(elements)
        self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path

    def create_nod(self, filepath, filename, project_theme):
        """Create a realistic Notice Of Deviation (NOD) PDF."""
        self.logger.info(f"Creating NOD PDF: {filename}")
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title and document info (using DocumentTitle instead of Title)
        elements.append(Paragraph("NOTICE OF DEVIATION", self.styles['DocumentTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add NOD information
        nod_date = datetime.datetime.strptime(filename.split('_')[1], '%m.%d.%Y')
        elements.append(Paragraph(f"NOD Number: NOD-{random.randint(1000, 9999)}", self.styles['Normal']))
        elements.append(Paragraph(f"Date: {nod_date.strftime('%B %d, %Y')}", self.styles['Normal']))
        elements.append(Paragraph(f"Project: {project_theme['name']}", self.styles['Normal']))
        elements.append(Paragraph(f"Component: {random.choice(project_theme['components'])}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Test Reference: {random.choice(project_theme['test_procedures'])}", self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section
        for section in NOD_SECTIONS:
            elements.append(Paragraph(section, self.styles['Section']))
            
            # Generate different content for each section
            if section == "Notice Of Deviation":
                content = f"""
                This Notice of Deviation documents a deviation from the approved {random.choice(['test procedure', 'specification', 'drawing', 'process requirement'])} 
                identified during {random.choice(['testing', 'inspection', 'analysis', 'manufacturing'])} of the {project_theme['name']} {random.choice(project_theme['components'])}.
                """
            
            elif section == "Affected Requirements":
                spec = random.choice(project_theme['specifications'])
                content = f"""
                The following requirements are affected by this deviation:
                
                Document: {spec}
                Section: {random.randint(1, 9)}.{random.randint(1, 9)}.{random.randint(1, 9)}
                Requirement: {random.choice(['Dimensional tolerance', 'Material property', 'Performance parameter', 'Test condition', 'Surface finish'])}
                
                Additional Reference Documents:
                - Drawing DWG-{random.randint(10000, 99999)}
                - Test Procedure TP-{random.randint(1000, 9999)}
                """
            
            elif section == "Description of Deviation":
                content = f"""
                {random.choice(['During testing', 'During inspection', 'During manufacturing', 'During assembly'])} of the {random.choice(project_theme['components'])}, 
                the following deviation was observed:
                
                {random.choice([
                    f"The {random.choice(project_theme['data_descriptions'])} value was {random.randint(5, 25)}% outside the specified tolerance.",
                    f"The {random.choice(project_theme['materials'])} material exhibited unexpected {random.choice(['discoloration', 'deformation', 'surface irregularities'])}.",
                    f"The {random.choice(project_theme['components'])} failed to meet the minimum {random.choice(project_theme['data_descriptions'])} requirement.",
                    f"Manufacturing process parameters deviated from approved values during {random.choice(['machining', 'heat treatment', 'assembly', 'coating'])}."
                ])}
                
                Deviation was first observed on {(nod_date - datetime.timedelta(days=random.randint(1, 5))).strftime('%B %d, %Y')} 
                by {random.choice(['Quality Inspector', 'Test Engineer', 'Manufacturing Engineer', 'Design Engineer'])}.
                """
            
            elif section == "Technical Justification":
                content = f"""
                {random.choice([
                    f"Analysis shows that the deviation is within acceptable margins for safe operation of the {project_theme['name']}.",
                    f"Additional testing demonstrates that the deviation does not affect critical performance parameters.",
                    f"Review of design margins confirms that the deviation is within the safety factor of the system.",
                    f"Material analysis confirms that the properties remain within acceptable limits despite the deviation."
                ])}
                
                Supporting data:
                - {random.choice(['FEA', 'CFD', 'Thermal', 'Structural'])} analysis report AR-{random.randint(1000, 9999)}
                - Additional test data from Test Run TR-{random.randint(1000, 9999)}
                - Historical data from similar conditions on previous projects
                """
            
            elif section == "Impact Assessment":
                content = f"""
                Impact on Form: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}
                Impact on Fit: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}
                Impact on Function: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}
                Impact on Reliability: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}
                Impact on Schedule: {random.choice(['None', 'Delay of 1-3 days', 'Delay of 4-7 days', 'Delay of 8-14 days'])}
                Impact on Cost: {random.choice(['None', 'Minor increase < 5%', 'Moderate increase 5-10%', 'Significant increase > 10%'])}
                
                Overall Risk Assessment: {random.choice(['Low', 'Medium', 'High'])}
                """
            
            elif section == "Disposition and Approval":
                disposition = random.choice(['Use As Is', 'Rework', 'Repair', 'Scrap and Replace', 'Conditional Acceptance'])
                content = f"""
                Recommended Disposition: {disposition}
                
                Justification for Disposition:
                {random.choice([
                    f"The deviation is within acceptable limits for the intended application.",
                    f"Rework can bring the component within specification requirements.",
                    f"Repair procedure has been validated to restore full functionality.",
                    f"Deviation exceeds critical limits and cannot be accepted.",
                    f"Conditional acceptance with additional monitoring during operation."
                ])}
                
                {random.choice([
                    "No additional verification testing required.",
                    f"Additional verification test required: {random.choice(project_theme['test_procedures'])}",
                    "Re-inspection required after rework/repair.",
                    "Material analysis required before implementation of disposition."
                ])}
                """
            
            elements.append(Paragraph(content, self.styles['DocumentNormal']))
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("APPROVAL SIGNATURES", self.styles['Section']))
        
        data = [
            ["Originator", "Technical Authority", "Quality Assurance", "Customer (if required)"],
            ["________________", "________________", "________________", "________________"],
            [f"Date: {nod_date.strftime('%m/%d/%Y')}", "Date: __/__/____", "Date: __/__/____", "Date: __/__/____"]
        ]
        
        t = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        elements.append(t)
        
        # Build the PDF
        doc.build(elements)
        self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
        
    def create_specification(self, filepath, filename, project_theme):
        """Create a realistic specification PDF."""
        self.logger.info(f"Creating specification PDF: {filename}")
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title and document info (using DocumentTitle instead of Title)
        elements.append(Paragraph(f"TECHNICAL SPECIFICATION: {filename}", self.styles['DocumentTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add specification information
        current_date = datetime.datetime.now()
        spec_id = random.choice(project_theme['specifications'])
        elements.append(Paragraph(f"Document Number: {spec_id}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Revision: {random.choice(['A', 'B', 'C', 'D', 'E'])}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Release Date: {current_date.strftime('%B %d, %Y')}", self.styles['DocumentNormal']))
        elements.append(Paragraph(f"Project: {project_theme['name']}", self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section
        for section in SPEC_SECTIONS:
            elements.append(Paragraph(section, self.styles['Section']))
            
            # Generate different content for each section
            if section == "Scope":
                content = f"""
                This specification establishes the requirements for the design, materials, manufacturing, testing, 
                and quality assurance for the {project_theme['name']} system and its components. It applies to all 
                {project_theme['name']} hardware used in aerospace applications classified as {random.choice(['Flight Critical', 'Mission Critical', 'Safety Critical'])}.
                
                The requirements herein apply to the following components:
                - {random.choice(project_theme['components'])}
                - {random.choice(project_theme['components'])}
                - {random.choice(project_theme['components'])}
                """
            
            elif section == "Applicable Documents":
                content = f"""
                The following documents form a part of this specification to the extent specified herein:
                
                Industry Standards:
                - {random.choice(project_theme['specifications'])}
                - ASTM {random.choice(['E8', 'E9', 'E21', 'E238', 'E466'])}
                - MIL-STD-{random.randint(100, 999)}
                - RTCA DO-{random.randint(100, 400)}
                
                Company Documents:
                - Quality Manual QM-{random.randint(1000, 9999)}
                - Process Specification PS-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C'])}
                - Test Procedure TP-{random.randint(1000, 9999)}
                """
            
            elif section == "Requirements":
                materials = ", ".join(random.sample(project_theme['materials'], min(3, len(project_theme['materials']))))
                performance_metric = random.choice(project_theme['data_descriptions'])
                
                content = f"""
                3.1 Physical Requirements
                   3.1.1 Dimensions: Per Drawing DWG-{random.randint(10000, 99999)}
                   3.1.2 Weight: Maximum {random.randint(5, 500)} {random.choice(['grams', 'kg', 'lbs'])}
                   3.1.3 Finish: {random.choice(['Anodized', 'Passivated', 'Painted', 'Plated', 'As Machined'])}
                
                3.2 Material Requirements
                   3.2.1 Approved Materials: {materials}
                   3.2.2 Material Certification: Required for all raw materials
                   3.2.3 Prohibited Materials: Cadmium, mercury, zinc, pure tin
                
                3.3 Performance Requirements
                   3.3.1 Operating Temperature: {random.choice(['-65 to +160', '-54 to +125', '-45 to +85'])} °C
                   3.3.2 {performance_metric}: Minimum {random.randint(80, 99)}% of nominal
                   3.3.3 Service Life: Minimum {random.randint(5, 15)} years or {random.randint(1000, 10000)} cycles
                
                3.4 Environmental Requirements
                   3.4.1 Shall withstand {random.choice(['vibration', 'shock', 'thermal cycling', 'vacuum', 'radiation'])} per Section 4
                   3.4.2 Humidity Resistance: Up to {random.randint(85, 100)}% RH
                """
            
            elif section == "Verification":
                test_procedures = ", ".join(random.sample(project_theme['test_procedures'], min(3, len(project_theme['test_procedures']))))
                
                content = f"""
                Verification methods shall include:
                
                4.1 Analysis
                   Engineering analysis shall be performed to verify compliance with requirements {random.randint(3, 5)}.1, {random.randint(3, 5)}.2, and {random.randint(3, 5)}.3.
                
                4.2 Demonstration
                   Functional demonstration shall be performed to verify requirements {random.randint(3, 5)}.4 and {random.randint(3, 5)}.5.
                
                4.3 Test
                   The following tests shall be performed:
                   - {test_procedures}
                   - Environmental screening per MIL-STD-810
                   - {random.choice(['Proof pressure test', 'Leak test', 'Functional test', 'EMI/EMC test'])}
                
                4.4 Inspection
                   Visual and dimensional inspection shall verify compliance with requirements 3.1.1, 3.1.3, and 3.2.
                """
            
            elif section == "Materials and Processes":
                content = f"""
                5.1 Material Selection
                   Materials shall be selected based on {random.choice(['strength-to-weight ratio', 'corrosion resistance', 'thermal properties', 'electrical conductivity'])}.
                
                5.2 Special Processes
                   The following special processes require qualification and approval:
                   - {random.choice(['Heat Treatment', 'Welding', 'Brazing', 'NDT', 'Surface Treatment'])}
                   - {random.choice(['Composite Layup', 'Adhesive Bonding', 'Precision Cleaning', 'Soldering', 'Coating'])}
                
                5.3 Process Controls
                   All processes shall be performed in accordance with approved procedures.
                   Process parameters shall be recorded and maintained as quality records.
                """
            
            elif section == "Quality Assurance":
                content = f"""
                6.1 Quality System
                   All work shall be performed under a quality system compliant with {random.choice(['ISO 9001', 'AS9100', 'NASA-STD-8739', 'ESA ECSS-Q-ST-20'])}.
                
                6.2 Nonconformance
                   Nonconforming materials shall be identified, segregated, and dispositioned per approved procedures.
                   Repair dispositions require customer approval.
                
                6.3 Traceability
                   Full material and process traceability shall be maintained through all manufacturing operations.
                   Each unit shall be marked with a unique serial number.
                
                6.4 Records
                   Quality records shall be maintained for a minimum of {random.randint(5, 10)} years.
                """
            
            elif section == "Testing and Acceptance":
                content = f"""
                7.1 Acceptance Testing
                   Each unit shall undergo the following minimum acceptance tests:
                   - {random.choice(project_theme['test_procedures'])}
                   - Dimensional inspection to critical characteristics
                   - {random.choice(['Functional verification', 'Leak check', 'Proof pressure', 'Electrical test'])}
                
                7.2 Qualification Testing
                   Qualification testing shall be performed on {random.choice(['first article units', 'dedicated qualification units', 'selected production units'])}.
                   Tests shall demonstrate compliance with all performance and environmental requirements.
                
                7.3 Test Reports
                   Test reports shall include:
                   - Test configuration and setup
                   - Test data and results
                   - Pass/fail criteria
                   - Non-conformances and observations
                   - Authorization signatures
                """
            
            elements.append(Paragraph(content, self.styles['DocumentNormal']))
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("APPROVALS", self.styles['Section']))
        
        data = [
            ["Prepared By", "Reviewed By", "Approved By"],
            ["________________", "________________", "________________"],
            [f"{random.choice(['Engineering', 'Systems', 'Design Engineer'])}", 
             f"{random.choice(['Quality Assurance', 'Technical Lead', 'Chief Engineer'])}",
             f"{random.choice(['Program Manager', 'Project Director', 'Engineering Manager'])}"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        elements.append(t)
        
        # Build the PDF
        doc.build(elements)
        self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path