#!/usr/bin/env python3
"""
Example script showing how to use the firmware classifier programmatically
"""

from pathlib import Path
from firmware_classifier import AssemblyParser, FirmwareDatabase, UniqueFeatureExtractor, FirmwareClassifier

def example_extract_and_classify():
    """Example of extracting features and classifying firmware"""
    
    # Setup paths
    firmware_root = Path("./example_firmware")  # Your firmware directory
    output_dir = Path("./results")
    database_file = output_dir / "firmware_database.json"
    unique_features_file = output_dir / "unique_features.csv"
    unknown_firmware = Path("./unknown_sample.asm")  # Your unknown firmware
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("🔍 Step 1: Extracting features from firmware collection...")
    
    # Initialize components
    database = FirmwareDatabase(database_file)
    parser = AssemblyParser()
    
    # Example: Add some firmware manually
    if firmware_root.exists():
        for project_dir in firmware_root.iterdir():
            if not project_dir.is_dir():
                continue
                
            project_name = project_dir.name
            print(f"  Processing project: {project_name}")
            
            # Find assembly files
            asm_files = list(project_dir.rglob("*.asm")) + list(project_dir.rglob("*.elf.asm"))
            
            for asm_file in asm_files:
                # Determine version from path
                relative_path = asm_file.relative_to(project_dir)
                version = str(relative_path.parent) if relative_path.parent != Path('.') else "default"
                
                print(f"    Processing {asm_file.name} (version: {version})")
                
                # Extract features
                features = parser.parse_assembly_file(asm_file)
                if features:
                    database.add_firmware(project_name, version, features)
                    print(f"      Extracted {len(features)} unique opcodes")
    
    # Save database
    database.save_database()
    
    print(f"\n📊 Step 2: Extracting unique features...")
    
    # Extract unique features
    extractor = UniqueFeatureExtractor(database)
    extractor.extract_unique_features(unique_features_file)
    
    print(f"\n🎯 Step 3: Classifying unknown firmware...")
    
    # Classify unknown firmware (if it exists)
    if unknown_firmware.exists():
        classifier = FirmwareClassifier(unique_features_file)
        results = classifier.classify_firmware(unknown_firmware)
        
        if results:
            print(f"\nClassification Results for {unknown_firmware.name}:")
            print("-" * 60)
            for i, (project, similarity, matched, total) in enumerate(results[:5], 1):
                confidence = "high" if similarity > 0.7 else "medium" if similarity > 0.3 else "low"
                print(f"{i}. {project:<15} Similarity: {similarity:.3f} ({matched}/{total}) - {confidence}")
                
            best_project, best_similarity, best_matched, best_total = results[0]
            print(f"\n🏆 Best Match: {best_project} with {best_similarity:.1%} similarity")
        else:
            print("❌ Classification failed")
    else:
        print(f"⚠️  Unknown firmware file not found: {unknown_firmware}")
        print("   Create a sample .asm file to test classification")
    
    print(f"\n✅ Process completed!")
    print(f"   Database: {database_file}")
    print(f"   Unique features: {unique_features_file}")

def example_programmatic_analysis():
    """Example of programmatic analysis without files"""
    
    print("🔬 Programmatic Analysis Example")
    print("=" * 50)
    
    # Create sample firmware features (normally parsed from .asm files)
    sample_features = {
        "ArduCopter_v4.0": {
            "mov": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "ldr": [[0, 0, 0], [2, 0, 0]],
            "bl": [[1, 0, 1], [3, 1, 2]]
        },
        "ArduCopter_v4.1": {
            "mov": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],  # Same as v4.0
            "ldr": [[0, 0, 0], [2, 0, 0], [1, 1, 0]],  # Added feature
            "str": [[0, 1, 0]]  # New opcode
        },
        "ArduPlane_v4.0": {
            "mov": [[0, 0, 0], [2, 1, 0]],  # Different pattern
            "ldr": [[1, 0, 0]],
            "bne": [[0, 0, 1]]  # Different opcodes
        }
    }
    
    # Initialize in-memory database
    database = FirmwareDatabase(Path("memory_db.json"))
    
    # Add sample firmware
    for firmware_name, features in sample_features.items():
        project, version = firmware_name.split("_")
        database.add_firmware(project, version, features)
        print(f"Added {firmware_name}: {len(features)} opcodes")
    
    # Analyze unique features
    print(f"\n📊 Unique Features Analysis:")
    
    for project in ["ArduCopter", "ArduPlane"]:
        project_features = database.get_project_features(project)
        print(f"\n{project}:")
        for opcode, hashes in project_features.items():
            print(f"  {opcode}: {len(hashes)} unique variants")
    
    # Simulate classification
    unknown_features = {
        "mov": [[0, 0, 0], [1, 0, 0]],  # Matches ArduCopter pattern
        "ldr": [[0, 0, 0]],
        "bl": [[1, 0, 1]]  # Matches ArduCopter
    }
    
    print(f"\n🎯 Simulated Classification:")
    print(f"Unknown firmware has opcodes: {list(unknown_features.keys())}")
    print(f"This would likely classify as ArduCopter based on 'mov' and 'bl' patterns")

if __name__ == "__main__":
    print("🚀 Firmware Classifier Examples")
    print("=" * 40)
    
    # Run programmatic example (always works)
    example_programmatic_analysis()
    
    print("\n" + "=" * 40)
    
    # Run file-based example (requires firmware files)
    print("\n📁 File-based Example:")
    print("To run the full file-based example:")
    print("1. Create ./example_firmware/ directory")
    print("2. Add firmware projects with .asm files")
    print("3. Uncomment the line below and run again")
    
    # Uncomment to run file-based example:
    # example_extract_and_classify()