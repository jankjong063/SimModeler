# Academic Citation Guidelines

## How to Cite SimModeler in Academic Publications

If you use SimModeler in your research, please cite our work using the following formats:

### BibTeX Citation
```bibtex
@software{simmodeler2025,
  title={SimModeler: 3D Offset-Based Firmware Birthmark Extraction for Hardware Classification},
  author={Firmware Birthmark Research Group},
  year={2025},
  url={https://github.com/[your-repo]/SimModeler},
  note={Open-source firmware analysis tool for academic research}
}

@article{firmware_birthmark_methodology2025,
  title={Hardware-Specific Firmware Birthmark Extraction Using 3D Offset Patterns},
  author={[Author Names]},
  journal={[Target Journal - e.g., IEEE Transactions on Information Forensics and Security]},
  year={2025},
  note={Under review}
}
```

### IEEE Style Citation
SimModeler Development Team, "SimModeler: 3D Offset-Based Firmware Birthmark Extraction for Hardware Classification," GitHub repository, 2025. [Online]. Available: https://github.com/[your-repo]/SimModeler

### APA Style Citation
Firmware Birthmark Research Group. (2025). *SimModeler: 3D Offset-Based Firmware Birthmark Extraction for Hardware Classification* [Computer software]. GitHub. https://github.com/[your-repo]/SimModeler

## Research Context

### Primary Research Areas
- **Firmware Security Analysis**
- **Hardware Fingerprinting**
- **Cybersecurity Machine Learning**
- **IoT Device Classification**
- **Supply Chain Security**

### Key Contributions
1. **3D Offset Feature Extraction**: Novel method for extracting hardware-specific patterns from firmware assembly code
2. **Lightweight Classification**: Standalone tool requiring no external dependencies
3. **ArduPilot Hardware Differentiation**: Demonstrated ability to distinguish flight controller hardware types
4. **Academic Research Tool**: Designed specifically for reproducible academic research

### Related Publications
Please also consider citing these related works that provide context for firmware birthmark research:

```bibtex
@inproceedings{firmware_birthmarks_survey2024,
  title={A Survey of Firmware Birthmark Techniques for IoT Device Identification},
  author={[Previous Authors]},
  booktitle={Proceedings of IEEE Conference on Computer and Communications Security},
  year={2024}
}
```

## Usage in Academic Papers

### Recommended Acknowledgment Text
"This research utilized SimModeler, an open-source firmware analysis tool developed by the Firmware Birthmark Research Group, for extracting 3D offset-based hardware fingerprints from ArduPilot firmware samples."

### Methodology Section Example
"We employed SimModeler's 3D offset pattern extraction algorithm to analyze firmware samples. The tool extracts feature vectors in the form [opcode_offset, codeblock_offset, branch_offset] for each assembly instruction, creating unique hardware-specific fingerprints that enable classification of different flight controller platforms running identical firmware versions."

### Results Section Example
"Using SimModeler, we successfully extracted 43,686 unique features from 25 firmware samples across 5 different hardware platforms (CubeOrange, MatekF405, KakuteH7, FlywooF745, Pixhawk4), achieving classification accuracies of 20.3-24.6% similarity scores for correct hardware identification."

## Contact for Academic Collaboration

For academic collaboration, questions about methodology, or requests for research data:

- **GitHub Issues**: For technical questions and bug reports
- **Academic Email**: [research-contact@institution.edu]
- **Research Group**: Firmware Birthmark Research Group

## Ethical Considerations

When citing this work, please note:

1. **Defensive Security Focus**: This tool is designed for defensive cybersecurity research
2. **Academic Use Only**: Commercial applications require separate licensing
3. **Responsible Disclosure**: Any security findings should follow responsible disclosure practices
4. **Data Privacy**: Ensure firmware samples do not contain sensitive information

## Contributing to Research

We welcome academic contributions in the form of:

- **Algorithm Improvements**: Enhanced feature extraction methods
- **New Hardware Support**: Additional firmware platform analysis
- **Evaluation Datasets**: Curated firmware sample collections
- **Comparative Studies**: Benchmarking against other firmware analysis tools

Thank you for using SimModeler in your research and helping advance the field of firmware security analysis!