#!/usr/bin/env python3
"""
Setup script to extract sample firmware data from zip file
"""

import zipfile
import os
from pathlib import Path

def setup_sample_data():
    """Extract sample firmware data if not already present"""
    
    current_dir = Path(__file__).parent
    zip_file = current_dir / "sample_firmware_mini.zip"
    extract_dir = current_dir / "sample_firmware"
    
    if extract_dir.exists():
        print(f"✅ Sample firmware already extracted at: {extract_dir}")
        return extract_dir
    
    if not zip_file.exists():
        print(f"❌ Sample firmware zip not found: {zip_file}")
        print(f"   Please ensure sample_firmware_mini.zip is present")
        return None
    
    print(f"📦 Extracting sample firmware from: {zip_file}")
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(current_dir)
        
        # The zip might contain various path structures, find the actual data directory
        possible_paths = [
            current_dir / "sample_firmware_mini",
            current_dir / "SimModeler" / "sample_firmware_mini", 
            current_dir / ".." / "SimModeler" / "sample_firmware_mini"
        ]
        
        extracted_mini = None
        for path in possible_paths:
            if path.exists():
                extracted_mini = path
                break
        
        if extracted_mini:
            try:
                if extracted_mini != extract_dir:
                    if extract_dir.exists():
                        # Remove existing directory
                        import shutil
                        shutil.rmtree(extract_dir)
                    extracted_mini.rename(extract_dir)
                    print(f"✅ Renamed {extracted_mini} to {extract_dir}")
                else:
                    print(f"✅ Data already in correct location: {extract_dir}")
            except OSError as e:
                print(f"⚠️  Warning: Could not rename directory: {e}")
                print(f"   Using existing directory: {extracted_mini}")
                extract_dir = extracted_mini
        else:
            print(f"⚠️  Warning: Could not find extracted sample_firmware_mini directory")
        
        print(f"✅ Sample firmware extracted to: {extract_dir}")
        
        # Show directory structure
        if extract_dir.exists():
            print(f"\n📁 Directory structure:")
            for project in extract_dir.iterdir():
                if project.is_dir():
                    print(f"  📂 {project.name}")
                    for version in project.iterdir():
                        if version.is_dir():
                            print(f"    📂 {version.name}")
                            firmware_dir = version / "firmware"
                            if firmware_dir.exists():
                                asm_files = list(firmware_dir.glob("*.asm"))
                                if asm_files:
                                    print(f"      📄 {asm_files[0].name}")
        else:
            print(f"❌ Directory not found: {extract_dir}")
        
        return extract_dir
        
    except Exception as e:
        print(f"❌ Error extracting sample firmware: {e}")
        return None

if __name__ == "__main__":
    setup_sample_data()