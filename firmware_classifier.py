#!/usr/bin/env python3
"""
Simple Firmware Classifier

A standalone tool for extracting project-based unique features and classifying firmware
based on 3D offset pattern similarity.

Usage:
    python firmware_classifier.py extract /path/to/firmware/root
    python firmware_classifier.py classify /path/to/unknown.asm
"""

import os
import re
import csv
import json
import hashlib
import argparse
import zipfile
import tempfile
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AssemblyParser:
    """Parse ARM assembly files and extract 3D offset features"""
    
    def __init__(self):
        # ARM branch operations
        self.branch_ops = {
            'b', 'bl', 'bx', 'blx', 'bne', 'beq', 'bcs', 'bcc', 'bmi', 'bpl',
            'bvs', 'bvc', 'bhi', 'bls', 'bge', 'blt', 'bgt', 'ble', 'bal'
        }
        
    def parse_assembly_file(self, file_path: Path) -> Dict[str, List[List[int]]]:
        """
        Parse assembly file and extract 3D offset features
        
        Returns:
            Dict mapping opcode -> List of [opcode_offset, codeblock_offset, branch_offset]
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return {}
            
        features = defaultdict(list)
        lines = content.strip().split('\n')
        
        # Regex patterns based on working assembly parser
        section_pattern = re.compile(r'Disassembly of section ([\w\.\-]+):')
        label_pattern = re.compile(r'([0-9A-Fa-f]+)\s+<([^>]+)>:')
        instruction_pattern = re.compile(
            r'\s*(?P<address>[0-9a-f]+):\s+(?P<opcode>[0-9a-f ]+)\s+(?P<assembly>\S+)(?:\s+(?P<operands>.*))?'
        )
        
        current_section = None
        code_blocks = []
        current_block = []
        current_block_start = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                current_section = section_match.group(1)
                i += 1
                continue
            
            # Skip if not in .text section
            if current_section != '.text':
                i += 1
                continue
            
            # Check for code block label
            label_match = label_pattern.match(line)
            if label_match:
                # Save previous block
                if current_block:
                    code_blocks.append({
                        'start_address': current_block_start,
                        'instructions': current_block
                    })
                
                # Start new block
                current_block_start = int(label_match.group(1), 16)
                current_block = []
                i += 1
                continue
            
            # Parse instruction
            instruction_match = instruction_pattern.match(line)
            if instruction_match:
                address = int(instruction_match.group('address'), 16)
                assembly = instruction_match.group('assembly')
                
                # Extract base opcode
                opcode = assembly.split('.')[0]  # Handle opcodes like "bl.w" -> "bl"
                
                # Calculate branch offset
                branch_offset = 0
                if opcode in self.branch_ops:
                    branch_offset = address - current_block_start if current_block_start else 0
                
                current_block.append({
                    'address': address,
                    'opcode': opcode,
                    'op_offset': address - current_block_start if current_block_start else 0,
                    'branch_offset': branch_offset
                })
            
            i += 1
        
        # Add final block
        if current_block:
            code_blocks.append({
                'start_address': current_block_start,
                'instructions': current_block
            })
            
        # Extract 3D features from code blocks
        for block_idx, block in enumerate(code_blocks):
            for instruction in block['instructions']:
                opcode = instruction['opcode']
                
                # Create 3D feature vector: [opcode_offset, codeblock_offset, branch_offset]
                feature_vector = [
                    instruction['op_offset'],  # Offset within code block
                    block_idx,                 # Code block index
                    instruction['branch_offset']  # Branch target offset
                ]
                
                features[opcode].append(feature_vector)
        
        # Sort each opcode's feature vectors for consistent ordering
        for opcode in features:
            features[opcode].sort()
                
        return dict(features)

class FirmwareDatabase:
    """Simple database for storing and retrieving firmware features"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.projects = defaultdict(lambda: defaultdict(dict))  # project -> version -> features
        self.load_database()
        
    def load_database(self):
        """Load existing database"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.projects = defaultdict(lambda: defaultdict(dict), data)
                logger.info(f"Loaded database with {len(self.projects)} projects")
            except Exception as e:
                logger.warning(f"Could not load database: {e}")
                
    def save_database(self):
        """Save database to file"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(dict(self.projects), f, indent=2)
            logger.info(f"Saved database to {self.db_path}")
        except Exception as e:
            logger.error(f"Could not save database: {e}")
            
    def add_firmware(self, project: str, version: str, features: Dict[str, List[List[int]]]):
        """Add firmware features to database"""
        # Convert features to hashed signatures
        feature_hashes = {}
        for opcode, vectors in features.items():
            # Sort vectors for consistent hashing
            sorted_vectors = sorted(vectors)
            vector_str = json.dumps(sorted_vectors, sort_keys=True)
            hash_value = hashlib.sha256(vector_str.encode()).hexdigest()
            feature_hashes[opcode] = hash_value
            
        self.projects[project][version] = feature_hashes
        logger.info(f"Added {project} v{version} with {len(feature_hashes)} opcodes")
        
    def get_project_features(self, project: str) -> Dict[str, Set[str]]:
        """Get all unique features for a project across versions"""
        project_features = defaultdict(set)
        
        if project in self.projects:
            for version_features in self.projects[project].values():
                for opcode, hash_value in version_features.items():
                    project_features[opcode].add(hash_value)
                    
        return {opcode: hashes for opcode, hashes in project_features.items()}

class UniqueFeatureExtractor:
    """Extract unique features per project"""
    
    def __init__(self, database: FirmwareDatabase):
        self.database = database
        
    def extract_unique_features(self, output_file: Path):
        """Extract unique features for each project and save to CSV"""
        all_projects = list(self.database.projects.keys())
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Project', 'Opcode', 'Hash'])
            
            for project in all_projects:
                logger.info(f"Processing project: {project}")
                
                # Get this project's features
                project_features = self.database.get_project_features(project)
                
                # Get all other projects' features
                other_features = defaultdict(set)
                for other_project in all_projects:
                    if other_project != project:
                        other_project_features = self.database.get_project_features(other_project)
                        for opcode, hashes in other_project_features.items():
                            other_features[opcode].update(hashes)
                
                # Find unique features (in this project but not in others)
                unique_count = 0
                for opcode, project_hashes in project_features.items():
                    other_hashes = other_features.get(opcode, set())
                    unique_hashes = project_hashes - other_hashes
                    
                    for unique_hash in unique_hashes:
                        writer.writerow([project, opcode, unique_hash])
                        unique_count += 1
                        
                logger.info(f"Found {unique_count} unique features for {project}")
                
        logger.info(f"Unique features saved to {output_file}")

class FirmwareClassifier:
    """Classify unknown firmware based on unique feature similarity"""
    
    def __init__(self, unique_features_file: Path):
        self.unique_features = defaultdict(lambda: defaultdict(set))  # project -> opcode -> hashes
        self.load_unique_features(unique_features_file)
        
    def load_unique_features(self, csv_file: Path):
        """Load unique features from CSV"""
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    project = row['Project']
                    opcode = row['Opcode']
                    hash_value = row['Hash']
                    self.unique_features[project][opcode].add(hash_value)
                    
            logger.info(f"Loaded unique features for {len(self.unique_features)} projects")
        except Exception as e:
            logger.error(f"Could not load unique features: {e}")
            
    def classify_firmware(self, firmware_file: Path) -> List[Tuple[str, float, int, int]]:
        """
        Classify firmware and return similarity scores
        
        Returns:
            List of (project, similarity, matched_features, total_features) tuples
        """
        # Parse the unknown firmware
        parser = AssemblyParser()
        firmware_features = parser.parse_assembly_file(firmware_file)
        
        if not firmware_features:
            logger.error("No features extracted from firmware")
            return []
            
        # Convert to hashes
        firmware_hashes = {}
        for opcode, vectors in firmware_features.items():
            sorted_vectors = sorted(vectors)
            vector_str = json.dumps(sorted_vectors, sort_keys=True)
            hash_value = hashlib.sha256(vector_str.encode()).hexdigest()
            firmware_hashes[opcode] = hash_value
            
        logger.info(f"Extracted {len(firmware_hashes)} unique opcodes from firmware")
        
        # Calculate similarity with each project
        results = []
        for project, project_opcodes in self.unique_features.items():
            matched_features = 0
            total_project_features = 0
            
            for opcode, unique_hashes in project_opcodes.items():
                total_project_features += len(unique_hashes)
                
                if opcode in firmware_hashes:
                    firmware_hash = firmware_hashes[opcode]
                    if firmware_hash in unique_hashes:
                        matched_features += 1
                        
            # Calculate similarity
            similarity = matched_features / total_project_features if total_project_features > 0 else 0
            results.append((project, similarity, matched_features, total_project_features))
            
        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results

def extract_zip_if_needed(firmware_path: Path) -> Path:
    """Extract zip file if needed and return path to firmware directory"""
    if firmware_path.suffix.lower() == '.zip':
        logger.info(f"Extracting ZIP file: {firmware_path}")
        
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp())
        
        # Extract zip file
        with zipfile.ZipFile(firmware_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the firmware directory inside extracted content
        extracted_items = list(temp_dir.iterdir())
        if len(extracted_items) == 1 and extracted_items[0].is_dir():
            # If there's only one directory, use it
            return extracted_items[0]
        else:
            # Multiple items or files, use temp directory
            return temp_dir
    else:
        # Not a zip file, return as-is
        return firmware_path

def extract_features_from_directory(firmware_root: Path, output_dir: Path):
    """Extract features from firmware directory structure or zip file"""
    database_file = output_dir / "firmware_database.json"
    unique_features_file = output_dir / "unique_features.csv"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle zip file extraction if needed
    actual_firmware_root = extract_zip_if_needed(firmware_root)
    
    # Initialize database
    database = FirmwareDatabase(database_file)
    parser = AssemblyParser()
    
    # Scan firmware directory
    logger.info(f"Scanning firmware directory: {actual_firmware_root}")
    
    try:
        for project_dir in actual_firmware_root.iterdir():
            if not project_dir.is_dir():
                continue
                
            project_name = project_dir.name
            logger.info(f"Processing project: {project_name}")
            
            # Find assembly files in project directory
            asm_files = list(project_dir.rglob("*.asm")) + list(project_dir.rglob("*.elf.asm"))
            
            for asm_file in asm_files:
                # Use file path structure to determine version
                relative_path = asm_file.relative_to(project_dir)
                version = str(relative_path.parent) if relative_path.parent != Path('.') else "default"
                
                logger.info(f"  Processing {project_name} v{version}: {asm_file.name}")
                
                # Extract features
                features = parser.parse_assembly_file(asm_file)
                if features:
                    database.add_firmware(project_name, version, features)
                    
        # Save database
        database.save_database()
        
        # Extract unique features
        logger.info("Extracting unique features...")
        extractor = UniqueFeatureExtractor(database)
        extractor.extract_unique_features(unique_features_file)
        
        logger.info(f"Feature extraction completed!")
        logger.info(f"Database: {database_file}")
        logger.info(f"Unique features: {unique_features_file}")
        
    finally:
        # Clean up temporary directory if zip was extracted
        if firmware_root.suffix.lower() == '.zip' and actual_firmware_root != firmware_root:
            import shutil
            shutil.rmtree(actual_firmware_root, ignore_errors=True)
            logger.info("Cleaned up temporary extraction directory")

def classify_firmware_file(firmware_file: Path, unique_features_file: Path):
    """Classify a single firmware file"""
    if not unique_features_file.exists():
        logger.error(f"Unique features file not found: {unique_features_file}")
        return
        
    logger.info(f"Classifying firmware: {firmware_file}")
    
    # Initialize classifier
    classifier = FirmwareClassifier(unique_features_file)
    
    # Classify firmware
    results = classifier.classify_firmware(firmware_file)
    
    if not results:
        logger.error("Classification failed")
        return
        
    # Display results
    print(f"\n🎯 Classification Results for {firmware_file.name}")
    print("=" * 80)
    print(f"{'Rank':<5} {'Project':<20} {'Similarity':<12} {'Matched':<10} {'Total':<10} {'Confidence'}")
    print("=" * 80)
    
    for i, (project, similarity, matched, total) in enumerate(results[:10], 1):
        confidence = "high" if similarity > 0.7 else "medium" if similarity > 0.3 else "low"
        print(f"{i:<5} {project:<20} {similarity:<12.3f} {matched:<10} {total:<10} {confidence}")
        
    # Best match details
    if results:
        best_project, best_similarity, best_matched, best_total = results[0]
        print(f"\n🏆 Best Match:")
        print(f"  Project: {best_project}")
        print(f"  Similarity: {best_similarity:.3f} ({best_similarity*100:.1f}%)")
        print(f"  Matched Features: {best_matched}/{best_total}")
        print(f"  Confidence: {'high' if best_similarity > 0.7 else 'medium' if best_similarity > 0.3 else 'low'}")

def main():
    parser = argparse.ArgumentParser(description="Simple Firmware Classifier")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract unique features from firmware directory')
    extract_parser.add_argument('firmware_root', type=Path, help='Root directory containing firmware projects')
    extract_parser.add_argument('--output', '-o', type=Path, default=Path('.'), help='Output directory (default: current directory)')
    
    # Classify command
    classify_parser = subparsers.add_parser('classify', help='Classify unknown firmware')
    classify_parser.add_argument('firmware_file', type=Path, help='Assembly file to classify')
    classify_parser.add_argument('--features', '-f', type=Path, default=Path('./unique_features.csv'), help='Unique features CSV file')
    
    args = parser.parse_args()
    
    if args.command == 'extract':
        extract_features_from_directory(args.firmware_root, args.output)
    elif args.command == 'classify':
        classify_firmware_file(args.firmware_file, args.features)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()