# Simple Firmware Classifier (SimModeler)

A standalone Python tool for project-based unique feature extraction and firmware classification using 3D offset patterns.

## 🎯 Purpose

This tool provides a simplified, standalone implementation of the firmware classification algorithm without dependencies on the main `fa` CLI. It's designed for:

- **Quick analysis** of firmware collections
- **Research experiments** with different datasets
- **Educational purposes** to understand the core algorithm
- **Integration** into other projects

## 🚀 Quick Start

### 0. Setup Sample Data (First Time Only)

```bash
# Extract sample firmware data from zip
python setup_sample_data.py
```

### 1. Extract Unique Features

```bash
# Extract features from firmware directory
python firmware_classifier.py extract ./sample_firmware

# Or extract from zip file directly
python firmware_classifier.py extract ./sample_firmware_mini.zip

# With custom output directory
python firmware_classifier.py extract ./sample_firmware --output ./results
```

**Expected directory structure:**
```
sample_firmware/
├── ProjectA/
│   ├── v1.0/
│   │   └── firmware/
│   │       └── firmware.elf.asm
│   ├── v1.1/
│   │   └── firmware/
│   │       └── firmware.elf.asm
│   └── v1.2/
│       └── firmware/
│           └── firmware.elf.asm
├── ProjectB/
│   ├── v1.0/
│   │   └── firmware/
│   │       └── firmware.elf.asm
│   └── v1.1/
│       └── firmware/
│           └── firmware.elf.asm
└── ProjectC/
    └── v1.0/
        └── firmware/
            └── firmware.elf.asm
```

### 2. Classify Unknown Firmware

```bash
# Classify using generated unique features
python firmware_classifier.py classify unknown_firmware.asm

# Using custom features file
python firmware_classifier.py classify unknown_firmware.asm --features ./results/unique_features.csv
```

## 📊 Output Files

### 1. Firmware Database (`firmware_database.json`)
```json
{
  "ArduCopter": {
    "v4.0.0": {
      "mov": "a1b2c3d4e5f6...",
      "ldr": "f6e5d4c3b2a1...",
      "bl": "1234567890ab..."
    }
  }
}
```

### 2. Unique Features (`unique_features.csv`)
```csv
Project,Opcode,Hash
ArduCopter,mov,a1b2c3d4e5f6789012345678901234567890123456789012345678901234
ArduCopter,ldr,f6e5d4c3b2a1098765432109876543210987654321098765432109876543
ArduPlane,bl,1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab
```

### 3. Classification Results
```
🎯 Classification Results for unknown_firmware.asm
================================================================================
Rank  Project              Similarity   Matched    Total      Confidence
================================================================================
1     ProjectA            0.847        1247       1472       high
2     ProjectB            0.623        916        1472       medium
3     ProjectC            0.234        345        1472       low

🏆 Best Match:
  Project: ProjectA
  Similarity: 0.847 (84.7%)
  Matched Features: 1247/1472
  Confidence: high
```

## 🔧 Algorithm Overview

### 3D Offset Feature Extraction

The tool extracts 3D offset features for each opcode:

```python
feature_vector = [
    instr_idx,      # opcode_offset (position in code block)
    block_idx,      # codeblock_offset (block index in section)
    branch_offset   # branch_offset (for branch instructions)
]
```

### Unique Feature Identification

1. **Extract features** from all firmware in each project
2. **Hash feature vectors** using SHA256 for consistent signatures
3. **Identify unique features** present in one project but not in others
4. **Save unique features** per project to CSV

### Classification Process

1. **Parse unknown firmware** and extract 3D offset features
2. **Compare feature hashes** against unique features database
3. **Calculate similarity** as (matched_features / total_project_features)
4. **Rank projects** by similarity score

## 💡 Usage Examples

### Example 1: Sample Firmware Analysis

```bash
# Extract features from sample firmware collection
python firmware_classifier.py extract ./sample_firmware

# Classify unknown firmware
python firmware_classifier.py classify unknown_firmware.asm
```

### Example 2: Custom Firmware Collection

```bash
# Extract with custom output
python firmware_classifier.py extract ./my_firmware_collection --output ./analysis_results

# Classify with custom features
python firmware_classifier.py classify unknown.asm --features ./analysis_results/unique_features.csv
```

### Example 3: Batch Classification

```bash
# Classify multiple files
for firmware in unknown_firmware/*.asm; do
    echo "Classifying: $firmware"
    python firmware_classifier.py classify "$firmware"
done
```

## 🎓 Educational Value

This tool demonstrates:

- **3D offset feature extraction** from assembly code
- **Unique feature identification** for project differentiation
- **Similarity-based classification** using structural patterns
- **Hash-based feature comparison** for efficiency

## 🔬 Research Applications

### Firmware Family Analysis
- Identify firmware families and variants
- Track firmware evolution across versions
- Detect unauthorized modifications

### Malware Detection
- Compare suspicious firmware against known families
- Identify potential malware insertions
- Analyze firmware authenticity

### Supply Chain Security
- Verify firmware source and integrity
- Detect unauthorized firmware modifications
- Track firmware provenance

## ⚡ Performance

- **Feature Extraction**: ~100-500 firmware files per minute
- **Classification**: ~50-200ms per unknown firmware
- **Memory Usage**: ~50MB + 2x largest firmware file
- **Storage**: JSON database + CSV features (typically <10MB)

## 🛠️ Technical Details

### Supported Assembly Formats
- ARM assembly (.asm, .elf.asm)
- .text section processing
- Standard ARM instruction set

### Branch Operations Detected
```python
branch_ops = {
    'b', 'bl', 'bx', 'blx', 'bne', 'beq', 'bcs', 'bcc', 
    'bmi', 'bpl', 'bvs', 'bvc', 'bhi', 'bls', 'bge', 
    'blt', 'bgt', 'ble', 'bal'
}
```

### Feature Hash Generation
- Sort 3D vectors for consistent ordering
- JSON serialization with sorted keys
- SHA256 hash for unique signatures

## 🔧 Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- Works on Windows, macOS, and Linux

## 🆚 Comparison with Main Tool

| Feature | SimModeler | Main fa CLI |
|---------|------------|-------------|
| Dependencies | None | Many (sklearn, pytorch, etc.) |
| Database | JSON file | SQLite database |
| ML Algorithms | Similarity-based | 25+ ML algorithms |
| Visualization | Text output | Charts and LaTeX |
| Installation | Single file | Full package |
| Use Case | Quick analysis | Research platform |

## 🚀 Getting Started

1. **Download** the `firmware_classifier.py` file
2. **Prepare** your firmware directory structure
3. **Extract** unique features from your firmware collection
4. **Classify** unknown firmware samples
5. **Analyze** results and similarities

This tool provides the core firmware classification functionality in a simple, standalone package perfect for quick analysis and research experiments.