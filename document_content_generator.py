"""
Document Content Generator Module

This module handles the generation of document content independently of the output format.
"""

import random
import datetime
from typing import Dict, List, Tuple, Any

# Import configuration
from config import (
    TEST_THEMES,
    PO_SECTIONS, 
    QUOTE_SECTIONS, 
    SPEC_SECTIONS, 
    NOD_SECTIONS,
    BUSINESS_TERMS
)

class DocumentContentGenerator:
    """Class for generating document content independently of output format."""
    
    def __init__(self, logger=None):
        """Initialize the content generator."""
        self.logger = logger
    
    def generate_purchase_order_content(self, filename: str, project_theme: Dict) -> Dict[str, Any]:
        """
        Generate purchase order content.
        
        Args:
            filename: The base filename
            project_theme: The project theme dictionary
            
        Returns:
            Dict containing document content
        """
        current_date = datetime.datetime.now()
        content = {
            "title": f"PURCHASE ORDER: {filename}",
            "metadata": [
                f"Date: {current_date.strftime('%B %d, %Y')}",
                f"Project: {project_theme['name']}",
                f"Specification Reference: {random.choice(project_theme['specifications'])}"
            ],
            "sections": {}
        }
        
        # Generate different content for each section
        for section in PO_SECTIONS:
            if section == "Purchase Order Information":
                content["sections"][section] = [
                    f"Order Number: {filename}",
                    f"Date Required: {(current_date + datetime.timedelta(days=random.randint(30, 180))).strftime('%B %d, %Y')}",
                    f"Priority: {random.choice(['Standard', 'High', 'Critical'])}",
                    "Procurement Category: Aerospace Components"
                ]
            
            elif section == "Vendor Information":
                content["sections"][section] = [
                    f"Vendor: {random.choice(['Precision Aerospace Supply', 'Advanced Materials Co.', 'SpaceTech Industries', 'Orbital Components Inc.'])}",
                    f"Contact: {random.choice(['John Smith', 'Sarah Johnson', 'Robert Chen', 'Maria Rodriguez'])}",
                    f"Phone: (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    f"Email: contact@vendor-{random.randint(100, 999)}.com"
                ]
            
            elif section == "Technical Requirements":
                components = ", ".join(random.sample(project_theme['components'], min(3, len(project_theme['components']))))
                materials = ", ".join(random.sample(project_theme['materials'], min(3, len(project_theme['materials']))))
                
                content["sections"][section] = [
                    f"Components: {components}",
                    f"Materials: {materials}",
                    f"Quantity: {random.randint(1, 10)} units",
                    f"Drawing Reference: DWG-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C', 'D'])}"
                ]
            
            elif section == "Quality Assurance Requirements":
                content["sections"][section] = [
                    f"Quality Standard: {random.choice(BUSINESS_TERMS['quality_standards'])}",
                    f"Inspection Level: {random.choice(['Level I', 'Level II', 'Level III'])}",
                    "Documentation Required: Material Certificates, Test Reports, Certificate of Conformance",
                    f"Special Requirements: {random.choice(['None', 'First Article Inspection', 'Source Inspection', 'Lot Traceability'])}"
                ]
            
            elif section == "Shipping Instructions":
                content["sections"][section] = [
                    f"Delivery Terms: {random.choice(BUSINESS_TERMS['delivery_terms'])}",
                    f"Carrier: {random.choice(['FedEx', 'UPS', 'DHL', 'Specialized Freight'])}",
                    f"Packaging: {random.choice(['Standard', 'Custom Protective', 'Clean Room', 'Anti-Static'])}",
                    f"Shipping Address: 1234 Aerospace Way, Engineering Building {random.randint(1, 20)}, Room {random.randint(100, 999)}"
                ]
            
            elif section == "Terms and Conditions":
                content["sections"][section] = [
                    f"Payment Terms: {random.choice(BUSINESS_TERMS['payment_terms'])}",
                    f"Warranty: {random.choice(BUSINESS_TERMS['warranty_periods'])}",
                    f"Acceptance Criteria: {random.choice(BUSINESS_TERMS['acceptance_criteria'])}",
                    "Confidentiality: All technical information related to this purchase order is confidential and proprietary."
                ]
        
        # Add approval section
        content["approvals"] = {
            "title": "APPROVALS",
            "signers": ["Procurement Officer", "Technical Authority", "Quality Assurance"]
        }
        
        return content
    
    def generate_quote_content(self, filename: str, project_theme: Dict) -> Dict[str, Any]:
        """
        Generate quote content.
        
        Args:
            filename: The base filename
            project_theme: The project theme dictionary
            
        Returns:
            Dict containing document content
        """
        current_date = datetime.datetime.now()
        valid_until = current_date + datetime.timedelta(days=random.randint(30, 90))
        company_name = f"{random.choice(['Precision', 'Advanced', 'Stellar', 'Orbital'])} {random.choice(['Aerospace', 'Technologies', 'Engineering', 'Systems'])}"
        
        content = {
            "title": f"QUOTATION: {filename}",
            "company": {
                "name": company_name,
                "address": [
                    f"123 Technology Lane, Suite {random.randint(100, 999)}",
                    f"Aerospace Park, CA {random.randint(90000, 96000)}"
                ]
            },
            "metadata": [
                f"Date: {current_date.strftime('%B %d, %Y')}",
                f"Valid Until: {valid_until.strftime('%B %d, %Y')}",
                f"Project: {project_theme['name']}",
                f"Customer Reference: CR-{random.randint(10000, 99999)}"
            ],
            "sections": {}
        }
        
        # Generate different content for each section
        for section in QUOTE_SECTIONS:
            if section == "Executive Summary":
                summary = (
                    f"{company_name} is pleased to present this quotation for the {project_theme['name']} project. "
                    f"This quote covers the {random.choice(['design', 'manufacturing', 'testing', 'certification'])} "
                    f"of {random.choice(project_theme['components'])} components that meet or exceed the requirements "
                    f"specified in {random.choice(project_theme['specifications'])}. "
                    f"Our team has extensive experience with similar aerospace applications and is committed to "
                    f"delivering high-quality products that meet your schedule and performance requirements."
                )
                content["sections"][section] = [summary]
            
            elif section == "Scope of Work":
                components = ", ".join(random.sample(project_theme['components'], min(3, len(project_theme['components']))))
                test_procedures = ", ".join(random.sample(project_theme['test_procedures'], min(3, len(project_theme['test_procedures']))))
                
                content["sections"][section] = [
                    "This quotation includes the following scope:",
                    f"- Engineering analysis and design optimization for {components}",
                    "- Material procurement and quality verification",
                    f"- Manufacturing and assembly of {random.randint(1, 5)} units",
                    f"- Testing per {test_procedures}",
                    "- Documentation package including test reports and material certifications",
                    f"- {random.choice(['2', '3', '4'])} technical review meetings with customer representatives"
                ]
            
            elif section == "Technical Approach":
                content["sections"][section] = [
                    "Our approach for this project includes:",
                    "",
                    f"- Using {random.choice(project_theme['materials'])} material qualified to {random.choice(project_theme['specifications'])}",
                    f"- Implementing {random.choice(['advanced manufacturing techniques', 'proprietary process controls', 'specialized tooling'])} to ensure consistent quality",
                    f"- Conducting {random.choice(project_theme['test_procedures'])} according to industry standards",
                    f"- Performing all work in our {random.choice(['ISO 9001', 'AS9100D'])} certified facility",
                    "- Providing traceability for all materials and processes"
                ]
            
            elif section == "Schedule":
                start_date = current_date + datetime.timedelta(days=random.randint(7, 21))
                design_duration = random.randint(2, 6)
                manufacturing_duration = random.randint(4, 12)
                testing_duration = random.randint(2, 6)
                delivery_date = start_date + datetime.timedelta(weeks=(design_duration + manufacturing_duration + testing_duration))
                
                content["sections"][section] = [
                    "Preliminary Schedule:",
                    f"- Project Start: {start_date.strftime('%B %d, %Y')}",
                    f"- Design Phase: {design_duration} weeks",
                    f"- Manufacturing: {manufacturing_duration} weeks",
                    f"- Testing: {testing_duration} weeks",
                    f"- Final Delivery: {delivery_date.strftime('%B %d, %Y')}",
                    "",
                    "This schedule assumes timely customer reviews and approvals at key milestones."
                ]
            
            elif section == "Cost Breakdown":
                engineering = random.randint(20, 80) * 1000
                materials = random.randint(15, 60) * 1000
                manufacturing = random.randint(30, 100) * 1000
                testing = random.randint(10, 40) * 1000
                documentation = random.randint(5, 15) * 1000
                total = engineering + materials + manufacturing + testing + documentation
                
                content["sections"][section] = {
                    "type": "table",
                    "headers": ["Item", "Cost (USD)"],
                    "data": [
                        ["Engineering", f"${engineering:,}"],
                        ["Materials", f"${materials:,}"],
                        ["Manufacturing", f"${manufacturing:,}"],
                        ["Testing", f"${testing:,}"],
                        ["Documentation", f"${documentation:,}"],
                        ["Total", f"${total:,}"]
                    ]
                }
            
            elif section == "Terms and Conditions":
                content["sections"][section] = [
                    f"Payment Terms: {random.choice(BUSINESS_TERMS['payment_terms'])}",
                    f"Delivery: {random.choice(BUSINESS_TERMS['delivery_terms'])}",
                    f"Warranty: {random.choice(BUSINESS_TERMS['warranty_periods'])} from date of delivery",
                    f"Validity: This quote is valid for {random.randint(30, 90)} days from the date of issue",
                    "",
                    "This quotation is subject to our standard terms and conditions, which are available upon request.",
                    "All technical information provided in this quote is considered proprietary and confidential."
                ]
        
        # Add contact information
        contact_name = random.choice(['John Smith', 'Sarah Johnson', 'Robert Chen', 'Maria Rodriguez'])
        title = random.choice(['Sales Engineer', 'Project Manager', 'Business Development Manager', 'Technical Director'])
        
        content["contact"] = {
            "title": "CONTACT INFORMATION",
            "details": [
                f"Primary Contact: {contact_name}",
                f"Title: {title}",
                f"Phone: (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                f"Email: contact@{company_name.lower().replace(' ', '')}.com"
            ]
        }
        
        return content
    
    def generate_nod_content(self, filename: str, project_theme: Dict) -> Dict[str, Any]:
        """
        Generate Notice Of Deviation content.
        
        Args:
            filename: The base filename (should contain date in format NOD_mm.dd.yyyy)
            project_theme: The project theme dictionary
            
        Returns:
            Dict containing document content
        """
        # Extract date from filename
        nod_date = datetime.datetime.strptime(filename.split('_')[1], '%m.%d.%Y')
        
        content = {
            "title": "NOTICE OF DEVIATION",
            "metadata": [
                f"NOD Number: NOD-{random.randint(1000, 9999)}",
                f"Date: {nod_date.strftime('%B %d, %Y')}",
                f"Project: {project_theme['name']}",
                f"Component: {random.choice(project_theme['components'])}",
                f"Test Reference: {random.choice(project_theme['test_procedures'])}"
            ],
            "sections": {}
        }
        
        # Generate different content for each section
        for section in NOD_SECTIONS:
            if section == "Notice Of Deviation":
                content["sections"][section] = [
                    f"This Notice of Deviation documents a deviation from the approved {random.choice(['test procedure', 'specification', 'drawing', 'process requirement'])} "
                    f"identified during {random.choice(['testing', 'inspection', 'analysis', 'manufacturing'])} of the {project_theme['name']} {random.choice(project_theme['components'])}."
                ]
            
            elif section == "Affected Requirements":
                spec = random.choice(project_theme['specifications'])
                content["sections"][section] = [
                    "The following requirements are affected by this deviation:",
                    "",
                    f"Document: {spec}",
                    f"Section: {random.randint(1, 9)}.{random.randint(1, 9)}.{random.randint(1, 9)}",
                    f"Requirement: {random.choice(['Dimensional tolerance', 'Material property', 'Performance parameter', 'Test condition', 'Surface finish'])}",
                    "",
                    "Additional Reference Documents:",
                    f"- Drawing DWG-{random.randint(10000, 99999)}",
                    f"- Test Procedure TP-{random.randint(1000, 9999)}"
                ]
            
            elif section == "Description of Deviation":
                content["sections"][section] = [
                    f"{random.choice(['During testing', 'During inspection', 'During manufacturing', 'During assembly'])} of the {random.choice(project_theme['components'])}, "
                    f"the following deviation was observed:",
                    "",
                    f"The {random.choice(project_theme['data_descriptions'])} value was {random.randint(5, 25)}% outside the specified tolerance."
                    "",
                    f"Deviation was first observed on {(nod_date - datetime.timedelta(days=random.randint(1, 5))).strftime('%B %d, %Y')} "
                    f"by {random.choice(['Quality Inspector', 'Test Engineer', 'Manufacturing Engineer', 'Design Engineer'])}."
                ]
            
            elif section == "Technical Justification":
                content["sections"][section] = [
                    f"Analysis shows that the deviation is within acceptable margins for safe operation of the {project_theme['name']}.",
                    "",
                    "Supporting data:",
                    f"- {random.choice(['FEA', 'CFD', 'Thermal', 'Structural'])} analysis report AR-{random.randint(1000, 9999)}",
                    f"- Additional test data from Test Run TR-{random.randint(1000, 9999)}",
                    "- Historical data from similar conditions on previous projects"
                ]
            
            elif section == "Impact Assessment":
                content["sections"][section] = [
                    f"Impact on Form: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}",
                    f"Impact on Fit: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}",
                    f"Impact on Function: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}",
                    f"Impact on Reliability: {random.choice(['None', 'Minor', 'Moderate', 'Significant'])}",
                    f"Impact on Schedule: {random.choice(['None', 'Delay of 1-3 days', 'Delay of 4-7 days', 'Delay of 8-14 days'])}",
                    f"Impact on Cost: {random.choice(['None', 'Minor increase < 5%', 'Moderate increase 5-10%', 'Significant increase > 10%'])}",
                    "",
                    f"Overall Risk Assessment: {random.choice(['Low', 'Medium', 'High'])}"
                ]
            
            elif section == "Disposition and Approval":
                disposition = random.choice(['Use As Is', 'Rework', 'Repair', 'Scrap and Replace', 'Conditional Acceptance'])
                content["sections"][section] = [
                    f"Recommended Disposition: {disposition}",
                    "",
                    "Justification for Disposition:",
                    'Conditional acceptance with additional monitoring during operation.'
                    "",                   
                    f'Additional verification test required: {random.choice(project_theme["test_procedures"])}',
                ]
        
        # Add approval section
        content["approvals"] = {
            "title": "APPROVAL SIGNATURES",
            "signers": ["Originator", "Technical Authority", "Quality Assurance", "Customer (if required)"],
            "dates": [nod_date.strftime('%m/%d/%Y'), "__/__/____", "__/__/____", "__/__/____"]
        }
        
        return content
    
    def generate_specification_content(self, filename: str, project_theme: Dict) -> Dict[str, Any]:
        """
        Generate specification content.
        
        Args:
            filename: The base filename
            project_theme: The project theme dictionary
            
        Returns:
            Dict containing document content
        """
        current_date = datetime.datetime.now()
        spec_id = random.choice(project_theme['specifications'])
        
        content = {
            "title": f"TECHNICAL SPECIFICATION: {filename}",
            "metadata": [
                f"Document Number: {spec_id}",
                f"Revision: {random.choice(['A', 'B', 'C', 'D', 'E'])}",
                f"Release Date: {current_date.strftime('%B %d, %Y')}",
                f"Project: {project_theme['name']}"
            ],
            "sections": {}
        }
        
        # Generate different content for each section
        for section in SPEC_SECTIONS:
            if section == "Scope":
                content["sections"][section] = [
                    f"This specification establishes the requirements for the design, materials, manufacturing, testing, "
                    f"and quality assurance for the {project_theme['name']} system and its components. It applies to all "
                    f"{project_theme['name']} hardware used in aerospace applications classified as {random.choice(['Flight Critical', 'Mission Critical', 'Safety Critical'])}.",
                    "",
                    "The requirements herein apply to the following components:",
                    f"- {random.choice(project_theme['components'])}",
                    f"- {random.choice(project_theme['components'])}",
                    f"- {random.choice(project_theme['components'])}"
                ]
            
            elif section == "Applicable Documents":
                content["sections"][section] = [
                    "The following documents form a part of this specification to the extent specified herein:",
                    "",
                    "Industry Standards:",
                    f"- {random.choice(project_theme['specifications'])}",
                    f"- ASTM {random.choice(['E8', 'E9', 'E21', 'E238', 'E466'])}",
                    f"- MIL-STD-{random.randint(100, 999)}",
                    f"- RTCA DO-{random.randint(100, 400)}",
                    "",
                    "Company Documents:",
                    f"- Quality Manual QM-{random.randint(1000, 9999)}",
                    f"- Process Specification PS-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C'])}",
                    f"- Test Procedure TP-{random.randint(1000, 9999)}"
                ]
            
            elif section == "Requirements":
                materials = ", ".join(random.sample(project_theme['materials'], min(3, len(project_theme['materials']))))
                performance_metric = random.choice(project_theme['data_descriptions'])
                
                content["sections"][section] = [
                    "3.1 Physical Requirements",
                    f"   3.1.1 Dimensions: Per Drawing DWG-{random.randint(10000, 99999)}",
                    f"   3.1.2 Weight: Maximum {random.randint(5, 500)} {random.choice(['grams', 'kg', 'lbs'])}",
                    f"   3.1.3 Finish: {random.choice(['Anodized', 'Passivated', 'Painted', 'Plated', 'As Machined'])}",
                    "",
                    "3.2 Material Requirements",
                    f"   3.2.1 Approved Materials: {materials}",
                    "   3.2.2 Material Certification: Required for all raw materials",
                    "   3.2.3 Prohibited Materials: Cadmium, mercury, zinc, pure tin",
                    "",
                    "3.3 Performance Requirements",
                    f"   3.3.1 Operating Temperature: {random.choice(['-65 to +160', '-54 to +125', '-45 to +85'])} °C",
                    f"   3.3.2 {performance_metric}: Minimum {random.randint(80, 99)}% of nominal",
                    f"   3.3.3 Service Life: Minimum {random.randint(5, 15)} years or {random.randint(1000, 10000)} cycles",
                    "",
                    "3.4 Environmental Requirements",
                    f"   3.4.1 Shall withstand {random.choice(['vibration', 'shock', 'thermal cycling', 'vacuum', 'radiation'])} per Section 4",
                    f"   3.4.2 Humidity Resistance: Up to {random.randint(85, 100)}% RH"
                ]
            
            elif section == "Verification":
                test_procedures = ", ".join(random.sample(project_theme['test_procedures'], min(3, len(project_theme['test_procedures']))))
                
                content["sections"][section] = [
                    "Verification methods shall include:",
                    "",
                    "4.1 Analysis",
                    f"   Engineering analysis shall be performed to verify compliance with requirements {random.randint(3, 5)}.1, {random.randint(3, 5)}.2, and {random.randint(3, 5)}.3.",
                    "",
                    "4.2 Demonstration",
                    f"   Functional demonstration shall be performed to verify requirements {random.randint(3, 5)}.4 and {random.randint(3, 5)}.5.",
                    "",
                    "4.3 Test",
                    "   The following tests shall be performed:",
                    f"   - {test_procedures}",
                    "   - Environmental screening per MIL-STD-810",
                    f"   - {random.choice(['Proof pressure test', 'Leak test', 'Functional test', 'EMI/EMC test'])}",
                    "",
                    "4.4 Inspection",
                    "   Visual and dimensional inspection shall verify compliance with requirements 3.1.1, 3.1.3, and 3.2."
                ]
            
            elif section == "Materials and Processes":
                content["sections"][section] = [
                    "5.1 Material Selection",
                    f"   Materials shall be selected based on {random.choice(['strength-to-weight ratio', 'corrosion resistance', 'thermal properties', 'electrical conductivity'])}.",
                    "",
                    "5.2 Special Processes",
                    "   The following special processes require qualification and approval:",
                    f"   - {random.choice(['Heat Treatment', 'Welding', 'Brazing', 'NDT', 'Surface Treatment'])}",
                    f"   - {random.choice(['Composite Layup', 'Adhesive Bonding', 'Precision Cleaning', 'Soldering', 'Coating'])}",
                    "",
                    "5.3 Process Controls",
                    "   All processes shall be performed in accordance with approved procedures.",
                    "   Process parameters shall be recorded and maintained as quality records."
                ]
            
            elif section == "Quality Assurance":
                content["sections"][section] = [
                    "6.1 Quality System",
                    f"   All work shall be performed under a quality system compliant with {random.choice(['ISO 9001', 'AS9100', 'NASA-STD-8739', 'ESA ECSS-Q-ST-20'])}.",
                    "",
                    "6.2 Nonconformance",
                    "   Nonconforming materials shall be identified, segregated, and dispositioned per approved procedures.",
                    "   Repair dispositions require customer approval.",
                    "",
                    "6.3 Traceability",
                    "   Full material and process traceability shall be maintained through all manufacturing operations.",
                    "   Each unit shall be marked with a unique serial number.",
                    "",
                    "6.4 Records",
                    f"   Quality records shall be maintained for a minimum of {random.randint(5, 10)} years."
                ]
            
            elif section == "Testing and Acceptance":
                content["sections"][section] = [
                    "7.1 Acceptance Testing",
                    "   Each unit shall undergo the following minimum acceptance tests:",
                    f"   - {random.choice(project_theme['test_procedures'])}",
                    "   - Dimensional inspection to critical characteristics",
                    f"   - {random.choice(['Functional verification', 'Leak check', 'Proof pressure', 'Electrical test'])}",
                    "",
                    "7.2 Qualification Testing",
                    f"   Qualification testing shall be performed on {random.choice(['first article units', 'dedicated qualification units', 'selected production units'])}.",
                    "   Tests shall demonstrate compliance with all performance and environmental requirements.",
                    "",
                    "7.3 Test Reports",
                    "   Test reports shall include:",
                    "   - Test configuration and setup",
                    "   - Test data and results",
                    "   - Pass/fail criteria",
                    "   - Non-conformances and observations",
                    "   - Authorization signatures"
                ]
        
        # Add approval section
        content["approvals"] = {
            "title": "APPROVALS",
            "signers": ["Prepared By", "Reviewed By", "Approved By"],
            "roles": [
                f"{random.choice(['Engineering', 'Systems', 'Design Engineer'])}", 
                f"{random.choice(['Quality Assurance', 'Technical Lead', 'Chief Engineer'])}",
                f"{random.choice(['Program Manager', 'Project Director', 'Engineering Manager'])}"
            ]
        }
        
        return content
        
    def generate_test_log_content(self, component: str, test_proc: str, test_date: datetime.datetime, project_theme: Dict, test_type: str) -> Dict[str, Any]:
        """
        Generate test log content.
        
        Args:
            component: Component name
            test_proc: Test procedure name
            test_date: Test date
            project_theme: Project theme dictionary
            test_type: Type of test (from TEST_TYPES)
            
        Returns:
            Dict containing document content
        """
        # This would implement test log content generation
        # For now it's a placeholder that your test_log_generator would use
        pass