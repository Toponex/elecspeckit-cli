# Hardware Design Citation Quality Checklist

Use this checklist to ensure your technical document citations are accurate, complete, and properly formatted before final submission of hardware design documentation.

## Pre-Submission Checklist

### ✓ Technical Document Accuracy

- [ ] All standard numbers include year/version (e.g., IEEE 802.11-2020)
- [ ] Vendor document revision codes are specified (e.g., Rev. C)
- [ ] Patent numbers include country code and kind code
- [ ] Standard organization names are complete and correct
- [ ] Vendor/manufacturer names are correct and consistent

### ✓ Required Fields

- [ ] All @standard entries have: title, number, organization, year
- [ ] All @manual entries have: title, organization, year, number (document ID)
- [ ] All @patent entries have: title, number, year
- [ ] All @techreport entries have: title, institution, year
- [ ] IEEE standards include DOI when available
- [ ] All entries have unique citation keys

### ✓ Standard Version Currency

- [ ] All cited standards are current (not superseded)
- [ ] If citing superseded standard, note status in comments or `note` field
- [ ] Standard edition numbers are correct (for IEC, ISO standards)
- [ ] Standard year matches the version actually referenced in design
- [ ] Run: `python scripts/validate_citations.py refs.bib --check-standard-status`

### ✓ Vendor Document Verification

- [ ] Vendor document numbers match actual documents
- [ ] Revision letters are the latest version (unless citing specific revision)
- [ ] Device/part numbers are correct
- [ ] Document types are correctly identified (datasheet, app note, user guide)
- [ ] Vendor names use standard abbreviations (TI, AD, ST, NXP, etc.)

### ✓ Formatting Consistency

- [ ] Standard numbers follow organization format
  - IEEE: IEEE 802.11-2020 (not IEEE 802.11/2020)
  - IEC: IEC 61010-1:2020 (colon before year)
  - IPC: IPC-2221B (hyphen, revision letter)
  - JEDEC: JESD22-A114 (no spaces)
- [ ] Citation keys follow consistent format (org+number+year)
- [ ] Organization names are not abbreviated in `organization` field
- [ ] Revision codes in `note` field format: "Rev. C" or "Revision B"
- [ ] Patent numbers: US10245678B2 (no spaces or hyphens)

### ✓ Duplicate Detection

- [ ] No duplicate standard numbers
- [ ] No duplicate vendor document IDs
- [ ] No duplicate patent numbers
- [ ] No duplicate citation keys
- [ ] Different revisions of same document properly distinguished
- [ ] Run: `python scripts/validate_citations.py refs.bib --check-duplicates`

### ✓ URLs and DOIs

- [ ] IEEE standard DOIs are correctly formatted
- [ ] URLs resolve to correct documents
- [ ] Vendor document URLs point to official vendor websites
- [ ] Patent URLs use stable services (patents.google.com, USPTO, EPO)
- [ ] No broken links
- [ ] Run: `python scripts/validate_citations.py refs.bib --check-urls`

### ✓ Special Characters and Formatting

- [ ] BibTeX special characters properly escaped
- [ ] Technical terms with special capitalization protected with braces
  - {IEEE}, {JEDEC}, {IEC}, {ISO}
  - {PCB}, {EMI}, {EMC}, {RF}
  - {WiFi}, {Bluetooth}, {USB}
- [ ] Chemical formulas use LaTeX math mode if needed
- [ ] No smart quotes (use straight quotes)
- [ ] Accented characters in author names handled correctly

### ✓ Technical Accuracy

- [ ] Parameter specifications match cited datasheet
- [ ] Standard requirements match cited version
- [ ] Component ratings match vendor specifications
- [ ] Test method references are correct
- [ ] Compliance claims match cited standards

### ✓ Design Document Integration

- [ ] All standards mentioned in design doc are in bibliography
- [ ] All vendor documents referenced are cited
- [ ] Patent citations match any IP discussions
- [ ] Test standards match test plan references
- [ ] Compliance standards match certification claims

### ✓ Regulatory and Compliance

- [ ] Safety standards are current and applicable
- [ ] EMC standards match target markets/regions
- [ ] Regional standards correctly identified (UL vs IEC vs EN)
- [ ] Certification requirements documented in `note` field
- [ ] Compliance status noted where relevant

## Hardware-Specific Validation Checks

### Power Supply Design

- [ ] IEC 61010-1 or IEC 62368-1 cited for safety
- [ ] IEC 61000-6-3 cited for EMC emissions
- [ ] IEC 61000-6-2 cited for EMC immunity (if industrial)
- [ ] IEEE 519 cited if grid-connected
- [ ] UL or EN equivalents cited for regional certification

### PCB Design

- [ ] IPC-2221 or IPC-2222 cited for design rules
- [ ] IPC-6012 cited for board qualification
- [ ] IPC-A-610 cited for acceptability criteria
- [ ] IEC 61000-4-2 cited for ESD requirements
- [ ] Specific spacing/clearance requirements match standard tables

### Wireless/RF Products

- [ ] IEEE 802.11 (WiFi) or 802.15.4 (Zigbee) cited if applicable
- [ ] FCC Part 15 or equivalent regional standard cited
- [ ] IEC 61000-4-3 cited for RF immunity
- [ ] CISPR 32 or EN 55032 cited for emissions
- [ ] Antenna design references include IEEE papers or app notes

### Motor Drives/Power Electronics

- [ ] IEC 61800 series cited for adjustable speed drives
- [ ] IEEE 519 cited for harmonic control
- [ ] UL 508C or IEC 61800-5-1 cited for power conversion safety
- [ ] Relevant semiconductor vendor app notes cited

### Embedded Systems

- [ ] Microcontroller datasheets cited with correct revision
- [ ] RTOS documentation cited if applicable
- [ ] Communication protocol standards cited (SPI, I2C, CAN, etc.)
- [ ] Relevant IEEE or vendor reference designs cited

### Test and Measurement

- [ ] JESD22 series cited for reliability testing
- [ ] IEC 61000-4-x cited for EMC test methods
- [ ] Relevant test equipment vendor manuals cited
- [ ] Calibration standards cited if applicable

## Citation Style Guidelines

### Standard Citations

**Correct**:
```bibtex
@standard{ieee80211_2020,
  title        = {IEEE Standard for Information Technology--Telecommunications...},
  number       = {IEEE 802.11-2020},
  organization = {Institute of Electrical and Electronics Engineers},
  year         = {2020},
  doi          = {10.1109/IEEESTD.2021.9363693}
}
```

**Incorrect**:
- Missing year in number field
- Abbreviated organization name
- Missing DOI for IEEE standards
- Inconsistent citation key format

### Vendor Document Citations

**Correct**:
```bibtex
@manual{ti_ucc28740,
  title        = {UCC28740 65-kHz, Flyback-Switch Mode Power Supply Controller},
  number       = {SLUSCJ3},
  organization = {Texas Instruments},
  year         = {2019},
  note         = {Rev. C}
}
```

**Incorrect**:
- Missing revision in note field
- Abbreviated vendor name in organization field
- Missing document number
- Incorrect year

### Patent Citations

**Correct**:
```bibtex
@patent{us10245678b2,
  title    = {Power Management System for Integrated Circuits},
  number   = {US10245678B2},
  author   = {Smith, John A. and Lee, Robert W.},
  year     = {2019},
  assignee = {Texas Instruments Incorporated}
}
```

**Incorrect**:
- Spaces or hyphens in patent number
- Missing kind code (B2, A1, etc.)
- Missing assignee field
- Incorrect author format

## Common Issues and Fixes

### Issue: Standard Superseded

**Problem**: Citing IEC 60950-1:2005 when IEC 62368-1:2018 is now current

**Fix**:
```bibtex
% Use current standard
@standard{iec62368_1_2018,
  title        = {Audio/video, information and communication technology equipment - Part 1: Safety requirements},
  number       = {IEC 62368-1:2018},
  organization = {International Electrotechnical Commission},
  year         = {2018},
  note         = {Supersedes IEC 60950-1:2005}
}
```

### Issue: Missing Revision Code

**Problem**: Citing TI datasheet without revision

**Fix**:
```bibtex
% Check datasheet for revision (usually on first or last page)
@manual{ti_doc,
  ...
  note         = {Rev. D}  % Add specific revision
}
```

### Issue: Ambiguous Standard Reference

**Problem**: Design says "per IEEE 802.11" without version

**Fix**:
- Check which specific version was used
- Update citation to include year
- Update design document to reference specific version

### Issue: Vendor Document Not Found

**Problem**: Cannot locate vendor document by number

**Fix**:
- Verify document number spelling/format
- Check for document number changes/updates
- Use vendor search with device part number
- Contact vendor technical support

## Final Validation Steps

### Automated Checks

```bash
# Run complete validation
python scripts/validate_citations.py hardware_refs.bib \
  --check-standards \
  --check-vendors \
  --check-patents \
  --check-urls \
  --report validation_report.json

# Review report
cat validation_report.json
```

### Manual Review

1. **Spot-check critical citations**:
   - Safety standards
   - Key vendor datasheets
   - Referenced patents

2. **Cross-reference with design documents**:
   - All cited standards mentioned in design spec
   - All component datasheets in BOM are cited
   - Test standards match test plan

3. **Verify compliance claims**:
   - Standards support certification claims
   - Regional variants correctly cited
   - Version currency verified

4. **Check citation formatting**:
   - Consistent citation key style
   - Proper BibTeX field usage
   - Correct entry types

## Pre-Submission Summary

Before submitting design documentation with citations:

- [ ] All technical documents cited with complete metadata
- [ ] Standard versions are current and correct
- [ ] Vendor document revisions specified
- [ ] All automated validation checks pass
- [ ] Manual spot-checks completed
- [ ] Citations match design document references
- [ ] Compliance requirements documented
- [ ] URLs tested and resolve correctly
- [ ] BibTeX file validates without errors
- [ ] Bibliography formatted consistently

## Tools Reference

**Validation**:
```bash
python scripts/validate_citations.py refs.bib
```

**Format and clean**:
```bash
python scripts/format_bibtex.py refs.bib --output clean_refs.bib
```

**Extract metadata**:
```bash
python scripts/docnum_to_bibtex.py "IEEE 802.11-2020"
python scripts/extract_metadata.py --standard "IEC 61010-1:2020"
```

**Search databases**:
```bash
python scripts/search_ieee_xplore.py "power electronics"
python scripts/search_standards.py "EMC" --organizations "IEC,IEEE"
```

## Related Resources

- `ieee_xplore_search.md`: IEEE technical literature search guide
- `standards_databases.md`: Technical standards search guide
- `metadata_extraction.md`: Citation metadata extraction guide
- `bibtex_formatting.md`: BibTeX formatting guidelines
- `citation_validation.md`: Citation validation procedures

## Notes

- This checklist is specific to hardware and electronics engineering
- Adapt as needed for your specific design domain
- Maintain checklist as standards and requirements evolve
- Document any deviations from checklist in design review notes
