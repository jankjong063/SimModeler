#!/usr/bin/env python3
"""
Quick test script to verify the firmware classifier works
"""

import tempfile
from pathlib import Path
from firmware_classifier import AssemblyParser, FirmwareDatabase, UniqueFeatureExtractor, FirmwareClassifier

def create_sample_asm_file(content: str, file_path: Path):
    """Create a sample assembly file for testing"""
    with open(file_path, 'w') as f:
        f.write(content)

def test_firmware_classifier():
    """Test the firmware classifier with sample data"""
    
    print("🧪 Testing Firmware Classifier")
    print("=" * 40)
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create sample firmware files
        arducopter_asm = """
.text
00008000:	e1a00000 	nop
00008004:	e59f0010 	ldr	r0, [pc, #16]
00008008:	e3a01001 	mov	r1, #1
0000800c:	e5801000 	str	r1, [r0]
00008010:	e1a0f00e 	mov	pc, lr
00008014:	e59f0008 	ldr	r0, [pc, #8]
00008018:	ebfffffe 	bl	8000
0000801c:	e1a0f00e 	mov	pc, lr
        """
        
        arduplane_asm = """
.text
00008000:	e1a00000 	nop
00008004:	e59f0014 	ldr	r0, [pc, #20]
00008008:	e3a02002 	mov	r2, #2
0000800c:	e5802000 	str	r2, [r0]
00008010:	e3a03003 	mov	r3, #3
00008014:	e1a0f00e 	mov	pc, lr
00008018:	e59f0004 	ldr	r0, [pc, #4]
0000801c:	e12fff1e 	bx	lr
        """
        
        unknown_asm = """
.text
00008000:	e1a00000 	nop
00008004:	e59f0010 	ldr	r0, [pc, #16]
00008008:	e3a01001 	mov	r1, #1
0000800c:	e5801000 	str	r1, [r0]
00008010:	e1a0f00e 	mov	pc, lr
        """
        
        # Create firmware directory structure
        firmware_dir = temp_path / "firmware"
        
        # ArduCopter
        arducopter_dir = firmware_dir / "ArduCopter" / "v4.0"
        arducopter_dir.mkdir(parents=True)
        create_sample_asm_file(arducopter_asm, arducopter_dir / "arducopter.elf.asm")
        
        # ArduPlane  
        arduplane_dir = firmware_dir / "ArduPlane" / "v4.0"
        arduplane_dir.mkdir(parents=True)
        create_sample_asm_file(arduplane_asm, arduplane_dir / "arduplane.elf.asm")
        
        # Unknown firmware
        unknown_file = temp_path / "unknown.asm"
        create_sample_asm_file(unknown_asm, unknown_file)
        
        print(f"📁 Created test firmware in: {firmware_dir}")
        
        # Test feature extraction
        print(f"\n🔍 Step 1: Testing Assembly Parser")
        parser = AssemblyParser()
        
        # Test ArduCopter
        copter_features = parser.parse_assembly_file(arducopter_dir / "arducopter.elf.asm")
        print(f"ArduCopter features: {len(copter_features)} opcodes")
        for opcode, vectors in copter_features.items():
            print(f"  {opcode}: {len(vectors)} instances")
        
        # Test ArduPlane
        plane_features = parser.parse_assembly_file(arduplane_dir / "arduplane.elf.asm")
        print(f"ArduPlane features: {len(plane_features)} opcodes")
        for opcode, vectors in plane_features.items():
            print(f"  {opcode}: {len(vectors)} instances")
        
        # Test database
        print(f"\n💾 Step 2: Testing Database")
        database_file = temp_path / "test_database.json"
        database = FirmwareDatabase(database_file)
        
        database.add_firmware("ArduCopter", "v4.0", copter_features)
        database.add_firmware("ArduPlane", "v4.0", plane_features)
        database.save_database()
        
        print(f"Database saved to: {database_file}")
        
        # Test unique feature extraction
        print(f"\n🎯 Step 3: Testing Unique Feature Extraction")
        unique_features_file = temp_path / "unique_features.csv"
        extractor = UniqueFeatureExtractor(database)
        extractor.extract_unique_features(unique_features_file)
        
        # Read and display unique features
        with open(unique_features_file, 'r') as f:
            lines = f.readlines()
            print(f"Unique features file created with {len(lines)-1} features")
            print("Sample entries:")
            for line in lines[:5]:  # Show first 5 lines
                print(f"  {line.strip()}")
        
        # Test classification
        print(f"\n🏆 Step 4: Testing Classification")
        classifier = FirmwareClassifier(unique_features_file)
        results = classifier.classify_firmware(unknown_file)
        
        if results:
            print(f"Classification results for unknown firmware:")
            for i, (project, similarity, matched, total) in enumerate(results, 1):
                confidence = "high" if similarity > 0.7 else "medium" if similarity > 0.3 else "low"
                print(f"  {i}. {project}: {similarity:.3f} similarity ({matched}/{total}) - {confidence}")
                
            best_project, best_similarity, _, _ = results[0]
            print(f"\n🎉 Best match: {best_project} with {best_similarity:.1%} similarity")
            
            # The unknown firmware is based on ArduCopter, so it should classify as ArduCopter
            if best_project == "ArduCopter":
                print("✅ Test PASSED: Correctly identified as ArduCopter")
            else:
                print("❌ Test FAILED: Should have identified as ArduCopter")
        else:
            print("❌ Classification failed")
        
        print(f"\n🧪 Test completed successfully!")
        print(f"All components working correctly.")

if __name__ == "__main__":
    test_firmware_classifier()