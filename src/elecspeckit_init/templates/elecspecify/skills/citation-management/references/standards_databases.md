# Technical Standards Databases Guide

Comprehensive guide to searching technical standards from IEEE, IEC, IPC, JEDEC, ISO, UL, ANSI and other standards organizations for hardware development and electronics engineering.

## Overview

Technical standards are critical references for hardware development:
- **Purpose**: Define requirements, test methods, safety criteria
- **Authority**: Published by recognized standards organizations
- **Compliance**: Often legally required for product certification
- **Best practices**: Industry-agreed design and testing methodologies
- **Interoperability**: Ensure compatibility between components and systems

## Major Standards Organizations

### IEEE (Institute of Electrical and Electronics Engineers)

**Coverage**: Electrical engineering, electronics, telecommunications, computing

**Key Standard Series**:
- **IEEE 802**: Networking standards (802.11 WiFi, 802.3 Ethernet)
- **IEEE 1547**: Distributed energy resources interconnection
- **IEEE C37**: Power system protection and control
- **IEEE 1584**: Arc flash hazard calculation
- **IEEE 519**: Harmonic control in electrical power systems

**Access**:
- Website: https://standards.ieee.org/
- Subscription required for full text
- Some standards available for free preview

**Search Tips**:
```
# By number
IEEE 802.11
IEEE Std 1547-2018

# By topic
wireless LAN
grid interconnection
```

### IEC (International Electrotechnical Commission)

**Coverage**: Electrical, electronic, and related technologies

**Key Standard Series**:
- **IEC 61010**: Safety requirements for electrical equipment
- **IEC 60950 / 62368**: IT and audio/video equipment safety
- **IEC 61000**: Electromagnetic compatibility (EMC)
- **IEC 60601**: Medical electrical equipment
- **IEC 61508**: Functional safety

**Access**:
- Website: https://www.iec.ch/
- Purchase required for full text
- Previews and summaries available

**Search Tips**:
```
# By number
IEC 61010-1
IEC 61000-4-2

# By topic
safety power supply
EMC immunity
```

### IPC (Association Connecting Electronics Industries)

**Coverage**: PCB design, assembly, quality standards

**Key Standards**:
- **IPC-2221**: Generic PCB design standard
- **IPC-2222**: Rigid organic printed board design
- **IPC-A-610**: Acceptability of electronic assemblies
- **IPC-J-STD-001**: Requirements for soldered electrical connections
- **IPC-6012**: Qualification and performance of rigid PCBs
- **IPC-7351**: Generic requirements for surface mount design

**Access**:
- Website: https://www.ipc.org/
- Standards available for purchase
- Free standards for IPC members

**Search Tips**:
```
# By number
IPC-2221B
IPC-A-610

# By topic
PCB design spacing
solder joint inspection
```

### JEDEC (Solid State Technology Association)

**Coverage**: Semiconductor and solid-state technology standards

**Key Standard Series**:
- **JESD22**: Reliability test methods for packaged devices
- **JESD51**: Thermal measurement standards
- **JESD79**: DDR memory standards
- **JESD209**: Mobile memory standards (LPDDR)
- **JESD204**: Serial interface for data converters

**Access**:
- Website: https://www.jedec.org/
- Most standards available for free download (membership required)

**Search Tips**:
```
# By number
JESD22-A114
JESD51-2

# By topic
temperature cycling
thermal resistance
```

### ISO (International Organization for Standardization)

**Coverage**: Quality management, environmental, general technical standards

**Key Standards for Electronics**:
- **ISO 9001**: Quality management systems
- **ISO/IEC 27001**: Information security management
- **ISO 14001**: Environmental management
- **ISO 26262**: Automotive functional safety
- **ISO 13485**: Medical devices quality management

**Access**:
- Website: https://www.iso.org/
- Purchase required for full text
- Some freely available standards

**Search Tips**:
```
# By number
ISO 9001:2015
ISO 26262

# By topic
quality management
automotive safety
```

### UL (Underwriters Laboratories)

**Coverage**: Safety certification standards

**Key Standards**:
- **UL 60950-1**: IT equipment safety (replaced by UL 62368-1)
- **UL 62368-1**: Audio/video and ICT equipment safety
- **UL 1410**: TV and video equipment
- **UL 508**: Industrial control equipment
- **UL 1642**: Lithium battery safety

**Access**:
- Website: https://ul.com/
- Standards available for purchase
- UL Standards & Engagement portal

**Search Tips**:
```
# By number
UL 60950-1
UL 62368-1

# By topic
power supply safety
battery certification
```

### ANSI (American National Standards Institute)

**Coverage**: Coordinates US standards system

**Key Standards**:
- ANSI standards often incorporate IEEE, IEC standards
- ANSI C (electrical codes)
- ANSI/TIA (telecommunications)

**Access**:
- Website: https://www.ansi.org/
- Webstore: https://webstore.ansi.org/

## Search Strategies

### Finding Relevant Standards

**By Application Domain**:
```
Power Supply Design:
- IEC 61010-1 (Safety)
- IEC 60950-1 / 62368-1 (IT equipment)
- IEC 61000 series (EMC)
- IEEE 519 (Harmonics)

PCB Design:
- IPC-2221 (Generic design)
- IPC-2222 (Rigid PCB)
- IPC-7351 (Surface mount)
- IEC 61000-4-2 (ESD)

Wireless Products:
- IEEE 802.11 (WiFi)
- IEEE 802.15.4 (Zigbee)
- FCC Part 15 (RF emissions)
- IEC 61000-4-3 (RF immunity)

Motor Drives:
- IEC 61800 series (Adjustable speed drives)
- IEEE 519 (Harmonics)
- UL 508C (Power conversion equipment)
```

**By Compliance Need**:
```
Safety Certification:
- UL standards
- IEC 61010, 60950, 62368
- EN standards (European)

EMC Compliance:
- IEC 61000 series
- FCC Part 15
- EN 55032, EN 55035

Regional Requirements:
- North America: UL, CSA, FCC
- Europe: EN, CE marking
- China: CCC, GB standards
- Japan: PSE, VCCI
```

### Standard Number Patterns

**IEEE Standards**:
```
Pattern: IEEE [Std] NUMBER[.SUBNUM]-YEAR
Examples:
- IEEE 802.11-2020
- IEEE Std 1547-2018
- IEEE 519-2014
```

**IEC Standards**:
```
Pattern: IEC NUMBER[-PART]:YEAR
Examples:
- IEC 61010-1:2020
- IEC 60950-1:2005
- IEC 61000-4-2
```

**IPC Standards**:
```
Pattern: IPC-[PREFIX-]NUMBER[REVISION]
Examples:
- IPC-2221B
- IPC-A-610
- IPC-7351B
```

**JEDEC Standards**:
```
Pattern: JESD{SERIES}-{SPEC}[REVISION]
Examples:
- JESD22-A114
- JESD79-4A
- JESD51-2
```

## Using Standards in Design

### Requirements Cascade

1. **System Level**: ISO 9001, industry-specific standards
2. **Safety**: IEC 61010, UL standards
3. **EMC**: IEC 61000 series
4. **Component Level**: JEDEC, IPC standards
5. **Testing**: JESD22, IEC test standards

### Citation in Documentation

**Design specifications**:
```
This power supply shall comply with:
- IEC 61010-1:2020 (Safety requirements)
- IEC 61000-6-3:2020 (EMC emissions)
- IEC 61000-6-2:2019 (EMC immunity)
```

**Test plans**:
```
Thermal cycling per JESD22-A104
ESD testing per IEC 61000-4-2 Level 3
```

**PCB fabrication drawings**:
```
Board shall meet IPC-6012 Class 2 requirements
Spacing per IPC-2221B Table 6-1
```

### Version Control

**Important**: Standards are updated regularly
- Always cite specific year/version
- Check for superseded standards
- Note transition periods for new versions

## Command-Line Tools

### Search Standards Databases

```bash
# Search for IEC standards
python scripts/search_standards.py "IEC 61010" \
  --organizations "IEC" \
  --limit 20 \
  --output iec_safety.json

# Search multiple organizations
python scripts/search_standards.py "power supply safety" \
  --organizations "IEC,UL,EN" \
  --status current \
  --format bibtex \
  --output safety_standards.bib
```

### Convert Standard Numbers to BibTeX

```bash
# Single standard
python scripts/docnum_to_bibtex.py "IEEE 802.11-2020"

# Multiple standards
python scripts/docnum_to_bibtex.py --input standards_list.txt \
  --output standards.bib
```

### Extract Metadata

```bash
# From standard number
python scripts/extract_metadata.py \
  --standard "IEC 61010-1:2020" \
  --output standard_citation.bib
```

## BibTeX Formatting

### Standard Entry Type

Use `@standard` for technical standards:

```bibtex
@standard{ieee80211_2020,
  title        = {IEEE Standard for Information Technology--
                  Telecommunications and Information Exchange
                  between Systems - Local and Metropolitan Area
                  Networks--Specific Requirements - Part 11:
                  Wireless LAN Medium Access Control (MAC) and
                  Physical Layer (PHY) Specifications},
  number       = {IEEE 802.11-2020},
  organization = {Institute of Electrical and Electronics Engineers},
  year         = {2020},
  month        = {feb},
  doi          = {10.1109/IEEESTD.2021.9363693},
  url          = {https://standards.ieee.org/standard/802_11-2020.html}
}

@standard{iec61010_1_2020,
  title        = {Safety Requirements for Electrical Equipment for
                  Measurement, Control, and Laboratory Use -
                  Part 1: General Requirements},
  number       = {IEC 61010-1:2020},
  organization = {International Electrotechnical Commission},
  year         = {2020},
  edition      = {4th},
  url          = {https://webstore.iec.ch/publication/63646}
}

@standard{ipc2221b,
  title        = {Generic Standard on Printed Board Design},
  number       = {IPC-2221B},
  organization = {IPC - Association Connecting Electronics Industries},
  year         = {2018},
  note         = {Revision B}
}
```

## Standard Status Tracking

### Status Types

- **Current**: Active standard, latest version
- **Superseded**: Replaced by newer version
- **Withdrawn**: No longer maintained
- **Draft**: Under development

### Version History

Track standard evolution:
```
IEC 60950-1:2005 (Superseded)
  ↓
IEC 60950-1:2005 + A1:2009 (Superseded)
  ↓
IEC 62368-1:2014 (Superseded)
  ↓
IEC 62368-1:2018 (Current)
```

### Validation Workflow

```bash
# Check if standards are current
python scripts/validate_citations.py design_standards.bib \
  --check-standard-status \
  --report validation_report.json
```

## Regional Variations

### North America
- UL (United States)
- CSA (Canada)
- NOM (Mexico)
- FCC (Radio frequency)

### Europe
- EN standards (Harmonized European standards)
- CE marking requirements
- CENELEC (European electrical standards)

### Asia
- GB (China)
- JIS (Japan)
- KS (Korea)
- CNS (Taiwan)

### Cross-References

Many standards have regional equivalents:
```
IEC 61010-1 ≈ EN 61010-1 (Europe)
IEC 61010-1 ≈ UL 61010-1 (US)
IEC 60950-1 ≈ EN 60950-1 ≈ UL 60950-1
```

## Compliance Documentation

### Design Review Citations

```markdown
## Safety Compliance

Power supply design complies with:
- **IEC 61010-1:2020**: Measurement and control equipment
- **UL 61010-1**: US national differences
- **Spacing**: Per IEC 61010-1 Table 19 (working voltage 300V)
- **Insulation**: Basic insulation, 3mm minimum

## EMC Compliance

Conducted emissions: IEC 61000-6-3:2020 Class B
Radiated emissions: CISPR 32 Class B
ESD immunity: IEC 61000-4-2 Level 3 (±6kV contact)
```

### Test Report Citations

```markdown
## Test Results Summary

| Test | Standard | Level | Result |
|------|----------|-------|--------|
| Conducted Emissions | CISPR 32 | Class B | Pass |
| ESD Contact | IEC 61000-4-2 | Level 3 | Pass |
| Temperature Cycling | JESD22-A104 | Condition G | Pass |
```

## Best Practices

### Standard Selection

1. **Start with system requirements**: Safety, EMC, quality
2. **Identify mandatory standards**: Regulatory requirements
3. **Add relevant technical standards**: Design guidelines
4. **Check for updates**: Use current versions
5. **Document deviations**: If not fully compliant, document why

### Purchasing Strategy

1. **Essential standards**: Purchase full text
2. **Reference-only**: Use previews and summaries
3. **Membership**: Consider if frequently using standards
4. **Bundles**: Some organizations offer collections

### Version Management

1. **Citation format**: Always include year/version
2. **Transition planning**: Monitor standard updates
3. **Legacy products**: Document which version was used
4. **Update tracking**: Set reminders for standard reviews

## Common Standard Searches

### Power Electronics

```
IEC 61010-1        # Measurement equipment safety
IEC 62368-1        # IT/AV equipment safety
IEC 61000-6-3      # EMC emissions generic
IEEE 519           # Harmonic control
UL 508C            # Power conversion equipment
```

### PCB Design

```
IPC-2221B          # Generic PCB design
IPC-2222           # Rigid organic PCB
IPC-6012           # PCB qualification
IPC-A-610          # Acceptability criteria
IEC 61000-4-2      # ESD requirements
```

### Wireless/RF

```
IEEE 802.11        # WiFi
IEEE 802.15.4      # Low-power wireless
FCC Part 15        # Unlicensed RF devices
IEC 61000-4-3      # RF immunity
CISPR 32           # RF emissions
```

### Automotive

```
ISO 26262          # Functional safety
ISO 16750          # Environmental conditions
IEC 62228          # Battery systems
SAE J1772          # EV charging
```

## Additional Resources

### Standards Organization Portals
- IEEE Standards: https://standards.ieee.org/
- IEC Webstore: https://webstore.iec.ch/
- IPC Standards: https://www.ipc.org/
- JEDEC: https://www.jedec.org/
- ISO: https://www.iso.org/

### Regulatory Resources
- FCC (US): https://www.fcc.gov/
- CE Marking (EU): https://ec.europa.eu/growth/single-market/ce-marking/
- CCC (China): https://www.cqc.com.cn/

## Related Guides

- `ieee_xplore_search.md`: Searching IEEE technical literature
- `metadata_extraction.md`: Extracting standard metadata
- `bibtex_formatting.md`: Formatting standard citations
- `citation_validation.md`: Validating standard references
