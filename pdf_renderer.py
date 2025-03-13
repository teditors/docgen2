"""
PDF Document Renderer Module

This module provides PDF implementation of the document renderer.
"""

import os
import random
import datetime
import logging
from typing import Dict, List, Any

# Import for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch

# Import our modules
from base_document_renderer import DocumentRenderer
from document_content_generator import DocumentContentGenerator

class PDFRenderer(DocumentRenderer):
    """
    PDF implementation of the document renderer.
    Renders documents as PDF files using ReportLab.
    """
    
    def __init__(self, logger=None):
        """Initialize the PDF renderer."""
        super().__init__(logger)
        self.content_generator = DocumentContentGenerator(logger)
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()
    
    def _init_custom_styles(self):
        """Initialize custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='DocumentTitle',
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
    
    def create_purchase_order(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a purchase order PDF."""
        if self.logger:
            self.logger.info(f"Creating purchase order PDF: {filename}")
            
        # Get content from the content generator
        content = self.content_generator.generate_purchase_order_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title
        elements.append(Paragraph(content["title"], self.styles['DocumentTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add metadata
        for meta in content["metadata"]:
            elements.append(Paragraph(meta, self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section
        for section, section_content in content["sections"].items():
            elements.append(Paragraph(section, self.styles['Section']))
            
            if isinstance(section_content, list):
                # Regular text content
                section_text = "\n".join(section_content)
                elements.append(Paragraph(section_text, self.styles['DocumentNormal']))
            elif isinstance(section_content, dict) and section_content.get("type") == "table":
                # Table content
                data = [section_content["headers"]] + section_content["data"]
                table = Table(data)
                table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ]))
                elements.append(table)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section if present
        if "approvals" in content:
            elements.append(Spacer(1, 0.5 * inch))
            elements.append(Paragraph(content["approvals"]["title"], self.styles['Section']))
            
            # Create approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                dates = content["approvals"].get("dates", ["__/__/____"] * len(signers))
                roles = content["approvals"].get("roles", [""] * len(signers))
                
                # Create table data
                data = [signers, ["________________"] * len(signers)]
                if dates:
                    date_row = [f"Date: {date}" for date in dates]
                    data.append(date_row)
                if roles and all(roles):
                    data.append(roles)
                
                # Create and style the table
                t = Table(data, colWidths=[2.5*inch] * len(signers))
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ]))
                
                elements.append(t)
        
        # Add contact information if present
        if "contact" in content:
            elements.append(Spacer(1, 0.25 * inch))
            elements.append(Paragraph(content["contact"]["title"], self.styles['Section']))
            
            for detail in content["contact"]["details"]:
                elements.append(Paragraph(detail, self.styles['DocumentNormal']))
        
        # Build the PDF
        doc.build(elements)
        if self.logger:
            self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
    
    def create_quote(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a quote PDF."""
        if self.logger:
            self.logger.info(f"Creating quote PDF: {filename}")
            
        # Get content from the content generator
        content = self.content_generator.generate_quote_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title
        elements.append(Paragraph(content["title"], self.styles['DocumentTitle']))
        
        # Add company information
        company_name = content["company"]["name"]
        elements.append(Paragraph(company_name, self.styles['DocumentNormal']))
        for address_line in content["company"]["address"]:
            elements.append(Paragraph(address_line, self.styles['DocumentNormal']))
        
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add metadata
        for meta in content["metadata"]:
            elements.append(Paragraph(meta, self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section (similar to purchase order implementation)
        for section, section_content in content["sections"].items():
            elements.append(Paragraph(section, self.styles['Section']))
            
            if isinstance(section_content, list):
                # Regular text content
                section_text = "\n".join(section_content)
                elements.append(Paragraph(section_text, self.styles['DocumentNormal']))
            elif isinstance(section_content, dict) and section_content.get("type") == "table":
                # Table content
                data = [section_content["headers"]] + section_content["data"]
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
            
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add contact information
        if "contact" in content:
            elements.append(Spacer(1, 0.25 * inch))
            elements.append(Paragraph(content["contact"]["title"], self.styles['Section']))
            
            for detail in content["contact"]["details"]:
                elements.append(Paragraph(detail, self.styles['DocumentNormal']))
        
        # Build the PDF
        doc.build(elements)
        if self.logger:
            self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
    
    def create_nod(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a Notice Of Deviation PDF."""
        if self.logger:
            self.logger.info(f"Creating NOD PDF: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_nod_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title
        elements.append(Paragraph(content["title"], self.styles['DocumentTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add metadata
        for meta in content["metadata"]:
            elements.append(Paragraph(meta, self.styles['DocumentNormal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section (similar to previous implementations)
        for section, section_content in content["sections"].items():
            elements.append(Paragraph(section, self.styles['Section']))
            
            if isinstance(section_content, list):
                # Regular text content
                section_text = "\n".join(section_content)
                elements.append(Paragraph(section_text, self.styles['DocumentNormal']))
            
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section
        if "approvals" in content:
            elements.append(Spacer(1, 0.5 * inch))
            elements.append(Paragraph(content["approvals"]["title"], self.styles['Section']))
            
            # Create approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                dates = content["approvals"].get("dates", ["__/__/____"] * len(signers))
                
                # Create table data
                data = [signers, ["________________"] * len(signers)]
                if dates:
                    date_row = [f"Date: {date}" for date in dates]
                    data.append(date_row)
                
                # Create and style the table
                t = Table(data, colWidths=[1.5*inch] * len(signers))
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ]))
                
                elements.append(t)
        
        # Build the PDF
        doc.build(elements)
        if self.logger:
            self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
    
    def create_specification(self, filepath: str, filename: str, project_theme: Dict) -> str:
        """Create a specification PDF."""
        if self.logger:
            self.logger.info(f"Creating specification PDF: {filename}")
        
        # Get content from the content generator
        content = self.content_generator.generate_specification_content(filename, project_theme)
        
        # Get the complete file path
        full_path = os.path.join(filepath, f"{filename}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        elements = []
        
        # Add title
        elements.append(Paragraph(content["title"], self.styles['Title']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add metadata
        for meta in content["metadata"]:
            elements.append(Paragraph(meta, self.styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add content for each section (similar to previous implementations)
        for section, section_content in content["sections"].items():
            elements.append(Paragraph(section, self.styles['Heading1']))
            
            if isinstance(section_content, list):
                # Regular text content
                section_text = "\n".join(section_content)
                elements.append(Paragraph(section_text, self.styles['Normal']))
            
            elements.append(Spacer(1, 0.2 * inch))
        
        # Add approval section
        if "approvals" in content:
            elements.append(Spacer(1, 0.5 * inch))
            elements.append(Paragraph(content["approvals"]["title"], self.styles['Heading1']))
            
            # Create approval table
            if "signers" in content["approvals"]:
                signers = content["approvals"]["signers"]
                roles = content["approvals"].get("roles", [""] * len(signers))
                
                # Create table data
                data = [signers, ["________________"] * len(signers)]
                if roles:
                    data.append(roles)
                
                # Create and style the table
                t = Table(data, colWidths=[2.5*inch] * len(signers))
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ]))
                
                elements.append(t)
        
        # Build the PDF
        doc.build(elements)
        if self.logger:
            self.logger.debug(f"PDF created successfully: {full_path}")
        
        return full_path
    
    def create_test_log(self, filepath: str, test_type: str, project_theme: Dict) -> str:
        """
        Create a test log PDF.
        
        """
        if self.logger:
            self.logger.info(f"Creating test log PDF for {test_type}")

        component = random.choice(project_theme["components"])
        test_proc = random.choice(project_theme["test_procedures"])
        test_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 365))
        filename = f"TestLog_{component}_{test_proc}_{test_date.strftime('%Y%m%d')}.pdf"

        full_path = os.path.join(filepath, filename)

        try:
            # Create the PDF document
            doc = SimpleDocTemplate(full_path, pagesize=letter)
            elements = []
            
            # Add title
            elements.append(Paragraph(f"TEST LOG: {test_proc}", self.styles['Title']))
            elements.append(Spacer(1, 0.25 * inch))
            
            # Add general information
            elements.append(Paragraph("TEST INFORMATION", self.styles['Heading1']))
            
            data = [
                ["Test ID:", f"TL-{random.randint(10000, 99999)}"],
                ["Test Date:", test_date.strftime("%B %d, %Y")],
                ["Component:", component],
                ["Project:", project_theme['name']],
                ["Test Type:", test_type],
                ["Test Procedure:", test_proc],
                ["Test Engineer:", random.choice(['J. Smith', 'A. Johnson', 'R. Chen', 'M. Rodriguez', 'L. Williams'])],
                ["Location:", f"Test Bay {random.randint(1, 12)}"]
            ]
            
            t = Table(data, colWidths=[2*inch, 4*inch])
            t.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('ALIGNMENT', (0, 0), (0, -1), 'RIGHT'),
            ]))
            
            elements.append(t)
            elements.append(Spacer(1, 0.25 * inch))
            
            # Add test setup
            elements.append(Paragraph("TEST SETUP", self.styles['Heading1']))
            
            # Generate random test equipment
            test_equipment = []
            equipment_options = [
                f"Oscilloscope (S/N: OSC-{random.randint(10000, 99999)})",
                f"Function Generator (S/N: FG-{random.randint(10000, 99999)})",
                f"Data Acquisition System (S/N: DAQ-{random.randint(10000, 99999)})",
                f"Thermocouple Reader (S/N: TC-{random.randint(10000, 99999)})",
                f"Load Cell (S/N: LC-{random.randint(10000, 99999)})",
                f"Pressure Transducer (S/N: PT-{random.randint(10000, 99999)})",
                f"Accelerometer (S/N: ACC-{random.randint(10000, 99999)})",
                f"Environmental Chamber (S/N: EC-{random.randint(10000, 99999)})",
                f"Vibration Table (S/N: VT-{random.randint(10000, 99999)})",
                f"Spectrum Analyzer (S/N: SA-{random.randint(10000, 99999)})"
            ]
            
            # Select 2-5 random equipment items
            for _ in range(random.randint(2, 5)):
                if equipment_options:
                    equipment = random.choice(equipment_options)
                    test_equipment.append(equipment)
                    equipment_options.remove(equipment)  # No duplicates
            
            # Add equipment to document
            equipment_text = "The following equipment was used in this test:"
            elements.append(Paragraph(equipment_text, self.styles['Normal']))
            
            for item in test_equipment:
                elements.append(Paragraph(f"• {item}", self.styles['Normal']))
            
            elements.append(Spacer(1, 0.25 * inch))
            
            # Add test procedure summary
            elements.append(Paragraph("TEST PROCEDURE SUMMARY", self.styles['Heading1']))
            
            procedure_text = f"""
            This test was conducted in accordance with {test_proc} to verify the {component}'s
            performance under {test_type} conditions. The test sequence consisted of the following steps:
            """
            elements.append(Paragraph(procedure_text, self.styles['Normal']))
            
            # Generate random test steps
            test_steps = []
            if "Thermal" in test_type or "Temperature" in test_type:
                test_steps = [
                    "Install test article in environmental chamber",
                    f"Attach {random.randint(3, 8)} thermocouples to critical locations",
                    "Connect data acquisition system and verify sensor readings",
                    f"Establish ambient baseline at {random.randint(20, 25)}°C for 30 minutes",
                    f"Perform thermal cycling from {random.randint(-65, -40)}°C to +{random.randint(70, 125)}°C",
                    "Record temperature data at 1-minute intervals",
                    "Return to ambient conditions and perform functional test"
                ]
            elif "Vibration" in test_type or "Shock" in test_type:
                test_steps = [
                    "Mount test article to vibration fixture",
                    f"Attach {random.randint(3, 8)} accelerometers to critical locations",
                    "Perform pre-test functional check",
                    "Conduct low-level sine sweep for resonance search",
                    f"Apply random vibration profile at {random.randint(5, 15)} g RMS for {random.randint(1, 3)} minutes per axis",
                    "Conduct post-test functional check",
                    "Repeat for remaining axes"
                ]
            elif "Pressure" in test_type or "Leak" in test_type:
                test_steps = [
                    "Install test article in pressure test fixture",
                    "Connect pressure source and instrumentation",
                    "Perform initial leak check at low pressure",
                    f"Increase pressure to {random.randint(100, 500)} psi in {random.randint(3, 10)} increments",
                    "Hold at maximum pressure for 30 minutes",
                    "Monitor for pressure decay",
                    "Depressurize and perform post-test inspection"
                ]
            else:
                # Generic steps
                test_steps = [
                    "Install test article in test fixture",
                    "Connect test instrumentation and verify readings",
                    "Perform pre-test functional check",
                    f"Apply test conditions per {test_proc}",
                    "Record data at specified intervals",
                    "Return to ambient conditions",
                    "Perform post-test functional check"
                ]
            
            # Add steps to document
            for i, step in enumerate(test_steps, 1):
                elements.append(Paragraph(f"{i}. {step}", self.styles['Normal']))
            
            elements.append(Spacer(1, 0.25 * inch))
            
            # Add test results
            elements.append(Paragraph("TEST RESULTS", self.styles['Heading1']))
            
            # Generate test results based on test type
            if random.random() < 0.8:  # 80% pass rate
                result_text = f"""
                The {component} successfully completed all test requirements specified in {test_proc}.
                All measured parameters remained within acceptable limits throughout the test.
                """
                if "Thermal" in test_type or "Temperature" in test_type:
                    result_text += f" Maximum temperature deviation was {random.randint(1, 5)}°C from nominal."
                elif "Vibration" in test_type or "Shock" in test_type:
                    result_text += f" No resonances were detected within the {random.randint(10, 50)} to {random.randint(1000, 2000)} Hz range of interest."
                elif "Pressure" in test_type or "Leak" in test_type:
                    result_text += f" Pressure decay rate was {random.random()*0.5:.3f} psi/minute, below the {random.random()*0.8+0.5:.2f} psi/minute requirement."
            else:
                # Generate a test anomaly
                anomalies = [
                    f"Temperature exceeded upper limit by {random.randint(5, 15)}°C during cycle {random.randint(3, 8)}",
                    f"Resonance detected at {random.randint(50, 500)} Hz with amplification factor of {random.randint(5, 20)}",
                    f"Pressure decay rate of {random.random()*0.5+0.8:.2f} psi/minute exceeded the maximum allowable value",
                    f"Visual inspection revealed minor {random.choice(['discoloration', 'deformation', 'surface irregularities'])}",
                    f"Measured {random.choice(project_theme['data_descriptions'])} deviated by {random.randint(5, 25)}% from expected value"
                ]
                
                anomaly = random.choice(anomalies)
                result_text = f"""
                The {component} exhibited an anomaly during testing. {anomaly}.
                A Notice of Deviation (NOD) has been generated to document this condition.
                Engineering assessment is required to determine impact on component qualification.
                """
            
            elements.append(Paragraph(result_text, self.styles['Normal']))
            
            # Add data table
            elements.append(Paragraph("KEY MEASUREMENTS", self.styles['Heading1']))
            
            header = ["Parameter", "Requirement", "Measured", "Status"]
            
            rows = []
            for _ in range(random.randint(3, 6)):
                param = random.choice(project_theme['data_descriptions'])
                if "Temperature" in param:
                    req = f"{random.randint(-65, 150)}°C ± {random.randint(2, 10)}°C"
                    measured = f"{random.randint(-60, 145)}°C"
                elif "Pressure" in param:
                    req = f"{random.randint(10, 1000)} psi ± {random.randint(5, 50)} psi"
                    measured = f"{random.randint(15, 990)} psi"
                elif "Time" in param or "Rate" in param:
                    req = f"< {random.randint(10, 60)} seconds"
                    measured = f"{random.randint(5, 70)} seconds"
                else:
                    req = f"{random.randint(80, 120)} ± {random.randint(5, 20)}%"
                    measured = f"{random.randint(75, 125)}%"
                
                # Determine pass/fail status
                if random.random() < 0.9:  # 90% pass rate for individual measurements
                    status = "PASS"
                else:
                    status = "FAIL"
                
                rows.append([param, req, measured, status])
            
            # Create the table
            table_data = [header] + rows
            col_widths = [2*inch, 1.5*inch, 1.5*inch, 1*inch]
            t = Table(table_data, colWidths=col_widths)
            
            # Style the table
            table_style = [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGNMENT', (1, 1), (2, -1), 'CENTER'),
                ('ALIGNMENT', (3, 1), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]
            
            # Add color coding for pass/fail
            for i, row in enumerate(rows, 1):
                if row[3] == "PASS":
                    table_style.append(('TEXTCOLOR', (3, i), (3, i), colors.green))
                    table_style.append(('FONTNAME', (3, i), (3, i), 'Helvetica-Bold'))
                else:
                    table_style.append(('TEXTCOLOR', (3, i), (3, i), colors.red))
                    table_style.append(('FONTNAME', (3, i), (3, i), 'Helvetica-Bold'))
            
            t.setStyle(TableStyle(table_style))
            elements.append(t)
            
            elements.append(Spacer(1, 0.5 * inch))
            
            # Add conclusion and signatures
            elements.append(Paragraph("CONCLUSION", self.styles['Heading1']))
            
            if "FAIL" in [row[3] for row in rows] or "anomaly" in result_text:
                conclusion = f"""
                Based on the test results, the {component} does not fully meet all requirements
                specified in {test_proc}. Additional engineering analysis is required to determine
                the root cause and necessary corrective actions.
                """
            else:
                conclusion = f"""
                Based on the test results, the {component} meets all requirements specified in
                {test_proc} and is acceptable for the intended application.
                """
            
            elements.append(Paragraph(conclusion, self.styles['Normal']))
            elements.append(Spacer(1, 0.5 * inch))
            
            # Add signature table
            elements.append(Paragraph("APPROVALS", self.styles['Heading2']))
            
            sig_data = [
                ["Test Engineer", "Quality Assurance", "Engineering Manager"],
                ["________________", "________________", "________________"],
                [f"Date: {test_date.strftime('%m/%d/%Y')}", "Date: __/__/____", "Date: __/__/____"]
            ]
            
            t = Table(sig_data, colWidths=[2*inch, 2*inch, 2*inch])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            elements.append(t)
            
            # Build the PDF
            doc.build(elements)
            self.logger.debug(f"PDF created successfully: {full_path}")
            
            return full_path
            
        except Exception as e:
            self.logger.error(f"Error creating test log PDF {filename}: {e}")
            return None        
