#!/bin/bash

# SimModeler Usage Examples
# Simple firmware classifier usage examples

echo "🚀 SimModeler - Simple Firmware Classifier Usage Examples"
echo "========================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if script exists
if [ ! -f "firmware_classifier.py" ]; then
    echo "❌ Error: firmware_classifier.py not found"
    echo "Please run this script from the SimModeler directory"
    exit 1
fi

echo -e "${BLUE}📋 Available Commands:${NC}"
echo ""
python firmware_classifier.py --help
echo ""

echo -e "${BLUE}🔍 Extract Command Help:${NC}"
echo ""
python firmware_classifier.py extract --help
echo ""

echo -e "${BLUE}🎯 Classify Command Help:${NC}"
echo ""
python firmware_classifier.py classify --help
echo ""

echo -e "${YELLOW}💡 Usage Examples:${NC}"
echo ""

echo -e "${GREEN}1. Extract unique features from firmware directory:${NC}"
echo "   python firmware_classifier.py extract /path/to/firmware/root"
echo "   python firmware_classifier.py extract /path/to/firmware/root --output ./results"
echo ""

echo -e "${GREEN}2. Classify unknown firmware:${NC}"
echo "   python firmware_classifier.py classify unknown_firmware.asm"
echo "   python firmware_classifier.py classify unknown_firmware.asm --features ./results/unique_features.csv"
echo ""

echo -e "${GREEN}3. Real ArduPilot example:${NC}"
echo "   # Extract features from ArduPilot firmware collection"
echo "   python firmware_classifier.py extract /Users/.../ardupilotplanefirmware"
echo ""
echo "   # Classify unknown ArduPilot firmware"
echo "   python firmware_classifier.py classify mystery_firmware.asm"
echo ""

echo -e "${GREEN}4. Batch classification:${NC}"
echo "   for firmware in unknown_firmware/*.asm; do"
echo "       echo \"Classifying: \$firmware\""
echo "       python firmware_classifier.py classify \"\$firmware\""
echo "   done"
echo ""

echo -e "${YELLOW}📁 Expected Directory Structure:${NC}"
echo "firmware_root/"
echo "├── ArduCopter/"
echo "│   ├── v4.0.0/"
echo "│   │   └── arducopter.elf.asm"
echo "│   ├── v4.1.0/"
echo "│   │   └── arducopter.elf.asm"
echo "│   └── latest/"
echo "│       └── arducopter.elf.asm"
echo "├── ArduPlane/"
echo "│   ├── v4.0.0/"
echo "│   │   └── arduplane.elf.asm"
echo "│   └── stable/"
echo "│       └── arduplane.elf.asm"
echo "└── AntennaTracker/"
echo "    └── v1.0.0/"
echo "        └── antennatracker.elf.asm"
echo ""

echo -e "${YELLOW}📊 Output Files:${NC}"
echo "• firmware_database.json     - Feature database"
echo "• unique_features.csv        - Unique features per project"
echo ""

echo -e "${YELLOW}🧪 Test the tool:${NC}"
echo "python quick_test.py         - Run built-in test"
echo "python example.py            - See programmatic examples"
echo ""

echo -e "${GREEN}✅ Ready to use! Start with:${NC}"
echo "   python firmware_classifier.py extract /your/firmware/directory"