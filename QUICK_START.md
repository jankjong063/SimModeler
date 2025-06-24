# SimModeler Quick Start Guide

## 📦 GitHub Repository Ready Setup

This SimModeler package is optimized for GitHub distribution with .zip compressed sample data to comply with file size limits.

## 🚀 Getting Started

### Step 1: Setup Sample Data

```bash
# Extract sample firmware from compressed zip
python setup_sample_data.py
```

This will create a `sample_firmware/` directory with test data.

### Step 2: Extract Features

```bash
# Method 1: Extract from directory
python firmware_classifier.py extract ./sample_firmware

# Method 2: Extract directly from zip (no need to extract first)
python firmware_classifier.py extract ./sample_firmware_mini.zip

# Method 3: With custom output directory
python firmware_classifier.py extract ./sample_firmware --output ./my_results
```

### Step 3: Classify Unknown Firmware

```bash
# Classify a firmware file
python firmware_classifier.py classify ./sample_firmware/ProjectA/v1.0/firmware/firmware.elf.asm

# Or specify custom features file
python firmware_classifier.py classify unknown.asm --features ./my_results/unique_features.csv
```

## 📊 Expected Output

### Feature Extraction
```
✅ Processing 3 projects (ProjectA, ProjectB, ProjectC)
✅ 302 unique features extracted
✅ Files created:
   - firmware_database.json
   - unique_features.csv
```

### Classification Results
```
🎯 Classification Results for firmware.elf.asm
================================================================================
Rank  Project              Similarity   Matched    Total      Confidence
================================================================================
1     ProjectA            0.156        47         302        low
2     ProjectB            0.000        0          302        low
3     ProjectC            0.000        0          302        low

🏆 Best Match: ProjectA with 15.6% similarity
```

## 💡 Features

✅ **ZIP Support**: Extract features directly from .zip files  
✅ **Small Sample Data**: Only 61KB compressed test data  
✅ **GitHub Ready**: All files under 10MB limit  
✅ **No Dependencies**: Uses only Python standard library  
✅ **Automatic Cleanup**: Temporary files automatically removed  

## 🔧 File Structure

```
SimModeler/
├── firmware_classifier.py       # Main tool
├── setup_sample_data.py        # Sample data extractor
├── sample_firmware_mini.zip    # Compressed test data (61KB)
├── README.md                   # Full documentation
├── QUICK_START.md              # This guide
├── LICENSE                     # Academic license
└── .gitignore                  # Git ignore rules
```

## 🎯 Use Cases

- **Academic Research**: Firmware birthmark analysis
- **Hardware Classification**: Identify firmware hardware targets
- **Educational**: Learn 3D offset pattern extraction
- **Development**: Test firmware analysis algorithms

## ⚡ Performance

- **Feature Extraction**: ~3-6 projects in <1 second (sample data)
- **Classification**: ~100-200ms per firmware file
- **Memory Usage**: <50MB for sample data
- **Storage**: ~61KB zip + <1MB extracted

Perfect for GitHub distribution and academic collaboration! 🎓