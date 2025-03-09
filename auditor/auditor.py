#!/usr/bin/env python3
"""
Project Directory Audit Script

This script audits hardware test data directories for potential issues.
It flags errors in red and warnings in yellow, providing a summary to the console
and generating a detailed log file.
"""

import os
import sys
import datetime
import argparse
from pathlib import Path
import mimetypes


# ANSI color codes for terminal output
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'


class DirectoryAuditor:
    def __init__(self, base_path="../docgen2"):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.log_entries = []
        self.project_dirs = []
        
    def audit_project(self, project_id):
        """Audit a specific project directory using the project ID."""
        # Find the matching project directory
        project_path = None
        for item in self.base_path.glob(f"testbed/PD{project_id}*"):
            if item.is_dir() and item.name.startswith(f"PD{project_id}"):
                project_path = item
                break
        
        if not project_path:
            self.errors.append(f"Project directory PD{project_id}* does not exist")
            return False
        
        self.project_dirs.append(project_path)
        self.log_entries.append(f"Auditing project: {project_path.name}")
        
        # Perform the audit checks
        self._check_empty_folders(project_path)
        self._check_subdirectory_files(project_path)
        self._check_specific_files(project_path)
        
        return True
        
    def _check_empty_folders(self, project_path):
        """Check for empty critical folders (ERROR condition)."""
        critical_paths = [
            "receiving",
            "admin/PO",
            "admin/quotes",
            "admin/specification",
        ]
        
        # Add dynamic paths for testing folders
        for test_type in ["Dynamics", "EMIEMC", "Environmental"]:
            test_path = f"testing/{test_type}"
            if (project_path / test_path).exists():
                for phb_dir in (project_path / test_path).glob("PHB*"):
                    critical_paths.append(f"{test_path}/{phb_dir.name}/photographs")
                    critical_paths.append(f"{test_path}/{phb_dir.name}/worksheets")
        
        for rel_path in critical_paths:
            path = project_path / rel_path
            if path.exists() and not any(path.iterdir()):
                self.errors.append(f"Empty folder: {path.relative_to(self.base_path)}")
                self._log_directory_info(path)
    
    def _check_subdirectory_files(self, project_path):
        """Check for no files in any subdirectories (ERROR condition)."""
        # Check main project directory
        if not any(f.is_file() for f in project_path.glob("**/*")):
            self.errors.append(f"No files in any subdirectories: {project_path.relative_to(self.base_path)}")
        
        # Check PHB directories
        for test_type in ["Dynamics", "EMIEMC", "Environmental"]:
            test_path = project_path / "testing" / test_type
            if test_path.exists():
                for phb_dir in test_path.glob("PHB*"):
                    if not any(f.is_file() for f in phb_dir.glob("**/*")):
                        self.errors.append(f"No files in any subdirectories: {phb_dir.relative_to(self.base_path)}")
                    self._log_directory_info(phb_dir)
    
    def _check_specific_files(self, project_path):
        """Check for specific file requirements (WARNING conditions)."""
        # Check for PDF files in admin folders
        admin_folders = {
            "admin/PO": ".pdf",
            "admin/quotes": ".pdf",
            "admin/specification": ".pdf"
        }
        
        for folder, ext in admin_folders.items():
            path = project_path / folder
            if path.exists():
                pdf_files = list(path.glob(f"*{ext}"))
                if not pdf_files:
                    self.warnings.append(f"No {ext} file in {path.relative_to(self.base_path)}")
                elif len(pdf_files) > 1:
                    self.warnings.append(f"Multiple files in {path.relative_to(self.base_path)}")
                self._log_directory_info(path)
        
        # Check for JPEG files in receiving
        receiving_path = project_path / "receiving"
        if receiving_path.exists():
            jpeg_files = list(receiving_path.glob("*.jpeg")) + list(receiving_path.glob("*.jpg"))
            if not jpeg_files:
                self.warnings.append(f"No jpeg file in {receiving_path.relative_to(self.base_path)}")
            self._log_directory_info(receiving_path)
        
        # Check worksheets and data folders in testing directories
        for test_type in ["Dynamics", "EMIEMC", "Environmental"]:
            test_path = project_path / "testing" / test_type
            if test_path.exists():
                for phb_dir in test_path.glob("PHB*"):
                    # Check worksheets for PDF files
                    worksheets_path = phb_dir / "worksheets"
                    if worksheets_path.exists():
                        pdf_files = list(worksheets_path.glob("*.pdf"))
                        if not pdf_files:
                            self.warnings.append(f"No pdf file in {worksheets_path.relative_to(self.base_path)}")
                        self._log_directory_info(worksheets_path)
                    
                    # Check data folder
                    data_path = phb_dir / "data"
                    if data_path.exists() and not any(data_path.iterdir()):
                        self.warnings.append(f"No files in {data_path.relative_to(self.base_path)}")
                    self._log_directory_info(data_path)
                    
                    # Log other directories
                    nods_path = phb_dir / "NODs"
                    if nods_path.exists():
                        self._log_directory_info(nods_path)
                    
                    photos_path = phb_dir / "photographs"
                    if photos_path.exists():
                        self._log_directory_info(photos_path)
    
    def _log_directory_info(self, directory):
        """Log information about a directory and its contents."""
        if not directory.exists():
            self.log_entries.append(f"  Directory does not exist: {directory.relative_to(self.base_path)}")
            return
        
        self.log_entries.append(f"  Directory: {directory.relative_to(self.base_path)}")
        
        # Log files in the directory
        files = list(directory.glob("*"))
        if not files:
            self.log_entries.append("    No files found")
            return
        
        for file_path in files:
            if file_path.is_file():
                # Get file information
                size = file_path.stat().st_size
                mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                file_type = mimetypes.guess_type(file_path)[0] or "unknown"
                
                self.log_entries.append(
                    f"    {file_path.name}: {size} bytes, "
                    f"Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"Type: {file_type}"
                )
            elif file_path.is_dir():
                self.log_entries.append(f"    Subdirectory: {file_path.name}/")
    
    def generate_report(self):
        """Generate a summary report and log file."""
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Console output
        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}No issues found!{Colors.RESET}")
        else:
            print(f"{Colors.RED}Errors: {len(self.errors)}{Colors.RESET}")
            for error in self.errors:
                print(f"{Colors.RED}ERROR: {error}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}Warnings: {len(self.warnings)}{Colors.RESET}")
            for warning in self.warnings:
                print(f"{Colors.YELLOW}WARNING: {warning}{Colors.RESET}")
        
        # Overall status
        status = "PASS" if not self.errors else "FAIL"
        print(f"\nOverall status: {Colors.GREEN if status == 'PASS' else Colors.RED}{status}{Colors.RESET}")
        print(f"Projects audited: {', '.join([p.name for p in self.project_dirs])}")
        
        # Write detailed log file
        log_filename = f"audit_log_{now}.txt"
        with open(log_filename, "w") as log_file:
            log_file.write(f"Project Directory Audit Log - {now}\n")
            log_file.write(f"Status: {status}\n")
            log_file.write(f"Projects audited: {', '.join([p.name for p in self.project_dirs])}\n\n")
            
            log_file.write("ERRORS:\n")
            if self.errors:
                for error in self.errors:
                    log_file.write(f"  {error}\n")
            else:
                log_file.write("  None\n")
            
            log_file.write("\nWARNINGS:\n")
            if self.warnings:
                for warning in self.warnings:
                    log_file.write(f"  {warning}\n")
            else:
                log_file.write("  None\n")
            
            log_file.write("\nDETAILED LOG:\n")
            for entry in self.log_entries:
                log_file.write(f"{entry}\n")
        
        print(f"\nDetailed log saved to: {log_filename}")


def main():
    """Main function to parse arguments and run the audit."""
    parser = argparse.ArgumentParser(description="Audit project directories for issues.")
    parser.add_argument("project_ids", nargs="*", help="Project ID numbers (without PD prefix)")
    args = parser.parse_args()
    
    auditor = DirectoryAuditor()
    
    # If no project IDs provided, ask the user
    project_ids = args.project_ids
    if not project_ids:
        project_id = input("Enter a project directory number (without PD prefix): ")
        project_ids = [project_id]
    
    # Audit each project
    for project_id in project_ids:
        auditor.audit_project(project_id)
    
    # Generate the report
    auditor.generate_report()


if __name__ == "__main__":
    main()
