---
name: citation-management
description: Comprehensive citation management for hardware development and electronics engineering. Search IEEE Xplore, standards databases, and vendor documentation for technical documents, extract accurate metadata, validate citations, and generate properly formatted BibTeX entries. Use this skill when you need to find technical documents, verify citation information, convert document numbers to BibTeX, or ensure reference accuracy in technical design documentation.
version: "1.0.0"
---
# Citation Management Skill

## Overview

Manage technical citations systematically throughout the hardware design and development process. This skill provides tools and strategies for searching technical databases (IEEE Xplore, standards libraries, vendor documentation), extracting accurate metadata from multiple sources (IEEE, vendor websites, standards organizations), validating citation information, and generating properly formatted BibTeX entries.

Critical for maintaining technical documentation accuracy, avoiding design reference errors, and ensuring project traceability. Integrates seamlessly with hardware design documentation and project reports.

## When to Use This Skill

Use this skill when:

- Searching for specific technical documents on IEEE Xplore or standards databases
- Converting standard numbers, vendor document IDs, or patent numbers to properly formatted BibTeX
- Extracting complete metadata for technical documents (authors, title, standard number, version, date, etc.)
- Validating existing technical citations for accuracy
- Cleaning and formatting BibTeX files for technical documentation
- Finding key reference documents in specific technology areas
- Verifying that citation information matches the actual technical document
- Building a bibliography for design reports or project documentation
- Checking for duplicate technical citations
- Ensuring consistent technical document citation formatting

## Core Workflow

### Phase 1: Technical Document Discovery and Search

**Goal**: Find relevant documents using technical database search engines.

#### IEEE Xplore Search

IEEE Xplore provides technical literature in electrical engineering and computer science.

**Basic Search**:

```bash
# Search for papers on a specific technical topic
python scripts/search_ieee_xplore.py "PCB design signal integrity" \
  --limit 50 \
  --output results.json

# Search with year filter
python scripts/search_ieee_xplore.py "embedded system security" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output embedded_security.json
```

**Advanced Search Strategies**:

- Use quotation marks for exact phrases: `"power management"`
- Search by author: `author:Smith`
- Search in title: `intitle:"FPGA design"`
- Exclude terms: `circuit design -simulation`
- Use sort options to find highly cited technical documents
- Filter by date ranges to get recent standards

**Best Practices**:

- Use specific, targeted technical terms
- Include key acronyms and standard numbers
- Filter by recent years for fast-evolving technology areas
- Check "Cited by" to find key technical documents
- Export top results for further analysis

#### Standards Database Search

**Basic Search**:

```bash
# Search for technical standards
python scripts/search_standards.py "IEEE 802.11" \
  --limit 100 \
  --output wifi_standards.json

# Search with category filters
python scripts/search_standards.py \
  --query '"safety" AND "power supply"' \
  --categories "IEC,UL" \
  --output safety_standards.json
```

**Advanced Queries**:

- Use standard numbers: `"IPC-2221"`
- Category tags: `"PCB"[Category]`, `"safety"[Category]`
- Boolean operators: `AND`, `OR`, `NOT`
- Version filters: `revision:2020:2024`
- Standard types: `"Standard"[Document Type]`
- Combine with standards organization APIs for automation

**Best Practices**:

- Use official terminology from standards organizations
- Include multiple related standards when building complex queries
- Retrieve standard numbers for easy metadata extraction
- Export to JSON or directly to BibTeX

#### Google Scholar Search

Google Scholar provides comprehensive academic literature across all disciplines, including hardware engineering research.

**Basic Search**:

```bash
# Search for academic papers on hardware topics
python scripts/search_google_scholar.py "antenna design 5G" \
  --limit 50 \
  --output antenna_papers.json

# Search with year filter
python scripts/search_google_scholar.py "power electronics GaN" \
  --year-start 2020 \
  --limit 100 \
  --output gan_papers.json
```

**Advanced Search Strategies**:

- Use quotation marks for exact technical phrases: `"signal integrity"`
- Search by author: `author:"Smith J"`
- Search in title: `intitle:"FPGA implementation"`
- Exclude terms: `antenna -simulation`
- Use site-specific search: `site:ieee.org "power converter"`
- Combine multiple technical terms for precision

**Best Practices**:

- Combine with IEEE Xplore for comprehensive technical literature coverage
- Use for finding interdisciplinary research (hardware + software, hardware + materials science)
- Good for finding application-oriented papers and design methodologies
- Check citation counts to identify influential papers
- Use for finding review papers and survey articles
- Export results and cross-reference with standards databases

**When to Use Google Scholar**:

- Broad literature survey across multiple technical domains
- Finding papers not indexed in IEEE Xplore (e.g., materials science, physics)
- Searching for specific author's work across multiple venues
- Finding newer preprints and conference papers
- Cross-disciplinary hardware research (robotics, biomedical devices, etc.)

### Phase 2: Metadata Extraction

**Goal**: Convert document identifiers (standard numbers, vendor doc IDs, patent numbers) to complete, accurate metadata.

#### Quick Document Number to BibTeX Conversion

For single document numbers, use the quick conversion tool:

```bash
# Convert single standard number
python scripts/docnum_to_bibtex.py "IEEE 802.11-2020"

# Convert multiple document numbers from file
python scripts/docnum_to_bibtex.py --input doc_nums.txt --output references.bib

# Different output formats
python scripts/docnum_to_bibtex.py "IPC-2221B" --format json
```

#### Comprehensive Metadata Extraction

For standard numbers, vendor document IDs, patent numbers, or technical document URLs:

```bash
# Extract from standard number
python scripts/extract_metadata.py --standard "IEC 61010-1"

# Extract from vendor document ID
python scripts/extract_metadata.py --vendor-doc "TI-SLUU551"

# Extract from patent number
python scripts/extract_metadata.py --patent "US10245678B2"

# Extract from URL
python scripts/extract_metadata.py --url "https://standards.ieee.org/standard/802_11-2020.html"

# Batch extraction (from file, mixed identifiers)
python scripts/extract_metadata.py --input tech_doc_ids.txt --output citations.bib
```

**Metadata Sources**:

1. **Standards Organization APIs**: Primary source for technical standards

   - Comprehensive metadata for standard documents
   - Official information from publishing organizations
   - Includes standard number, title, version, publication date, status
   - May require API keys for access
2. **Vendor Documentation Libraries**: Chip and component technical docs

   - Vendor-provided datasheets and application notes
   - Includes device numbers, versions, revision history
   - Parameter tables and datasheet information
3. **Patent Database APIs**: Technical patent documents

   - Official patent metadata
   - Includes patent number, inventors, filing dates
   - May require API keys for access
4. **Technical Literature Databases**: Academic and technical literature

   - Metadata for conference papers and journal articles
   - Author affiliations, conference information
   - Requires subscriptions or API keys

**Extracted Content**:

- **Required fields**: title, standard/document number, version, publication date
- **Technical standards**: publishing organization, standard number, revision, effective date
- **Vendor documents**: vendor name, document type, device number, revision
- **Patent documents**: patent number, inventors, filing date, publication date
- **Technical papers**: authors, conference/journal, volume/issue, pages
- **Additional info**: abstract, keywords, technical domain, citation URL

### Phase 3: BibTeX Formatting

**Goal**: Generate clean, properly formatted technical document citation entries.

#### Understanding BibTeX Entry Types for Technical Documents

**Technical Document-Specific Entry Types**:

- `@standard`: Technical standards and specifications
- `@manual`: Technical manuals and guides
- `@patent`: Patent documents
- `@techreport`: Technical reports and white papers
- `@misc`: Vendor datasheets, application notes

**Required Fields by Type**:

```bibtex
@standard{ieee802.11_2020,
  title        = {IEEE Standard for Information Technology--Telecommunications and Information Exchange between Systems - Local and Metropolitan Area Networks--Specific Requirements - Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications},
  number       = {802.11-2020},
  organization = {Institute of Electrical and Electronics Engineers},
  year         = {2020},
  month        = {feb},
  doi          = {10.1109/IEEESTD.2021.9363693}
}

@manual{ti_ucc28740,
  title        = {UCC28740 65-kHz, Flyback-Switch Mode Power Supply Controller},
  number       = {SLUSCJ3},
  organization = {Texas Instruments},
  year         = {2019},
  month        = {apr},
  note         = {Rev. C}
}

@patent{us10245678b2,
  title        = {Power Management System for Integrated Circuits},
  number       = {US10245678B2},
  author       = {Smith, John and Lee, Robert},
  year         = {2019},
  month        = {mar},
  assignee     = {Texas Instruments Incorporated}
}
```

#### Formatting and Cleanup

Use the formatting tool to standardize technical citation files:

```bash
# Format and clean BibTeX file
python scripts/format_bibtex.py tech_references.bib \
  --output formatted_references.bib

# Sort entries by standard number
python scripts/format_bibtex.py tech_references.bib \
  --sort number \
  --output sorted_references.bib

# Sort by publication date (newest first)
python scripts/format_bibtex.py tech_references.bib \
  --sort year \
  --descending \
  --output sorted_references.bib

# Remove duplicates
python scripts/format_bibtex.py tech_references.bib \
  --deduplicate \
  --output clean_references.bib

# Validate and report issues
python scripts/format_bibtex.py tech_references.bib \
  --validate \
  --report validation_report.txt
```

**Formatting Operations**:

- Standardize technical document field order
- Consistent indentation and spacing
- Proper formatting of standard numbers
- Standardized abbreviations for vendor names
- Consistent document number formatting
- Remove unnecessary fields
- Fix common errors (missing commas, braces)

### Phase 4: Citation Validation

**Goal**: Verify accuracy and currency of all technical citations.

#### Comprehensive Validation

```bash
# Validate BibTeX file
python scripts/validate_citations.py tech_references.bib

# Validate and auto-fix common issues
python scripts/validate_citations.py tech_references.bib \
  --auto-fix \
  --output validated_references.bib

# Generate detailed validation report
python scripts/validate_citations.py tech_references.bib \
  --report validation_report.json \
  --verbose
```

**Technical Document-Specific Validation Checks**:

1. **Standard Version Validation**:

   - Standard number format correctness
   - Whether revision is the latest version
   - Standard status is currently effective
2. **Document Number Validation**:

   - Vendor document number format correctness
   - Document version is current
   - Document is still valid (not obsolete)
3. **Patent Status Validation**:

   - Patent number format correctness
   - Patent is still in force
   - Check for continuation patents
4. **Currency Checks**:

   - Technical standard is within validity period
   - Vendor document has newer versions available
   - Patent has expired
5. **Technical Parameter Consistency**:

   - Referenced device parameters match latest datasheets
   - Standard requirements match cited version
   - No contradictions in technical specifications

### Phase 5: Integration with Hardware Design Workflow

#### Building Bibliography for Design Documentation

Complete workflow for creating technical document citation lists:

```bash
# 1. Search for documents on your technical topic
python scripts/search_ieee_xplore.py \
  '"signal integrity" AND "high-speed PCB"' \
  --year-start 2020 \
  --limit 200 \
  --output signal_integrity_docs.json

# 2. Extract document numbers from search results and convert to BibTeX
python scripts/extract_metadata.py \
  --input signal_integrity_docs.json \
  --output signal_refs.bib

# 3. Add specific documents by standard number
python scripts/docnum_to_bibtex.py "IPC-2221B" >> signal_refs.bib
python scripts/docnum_to_bibtex.py "JESD22-A114" >> signal_refs.bib

# 4. Format and clean BibTeX file
python scripts/format_bibtex.py signal_refs.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output references.bib

# 5. Validate all technical citations
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 6. Review validation report and fix any remaining issues
cat validation.json

# 7. Use in your design documentation
# Include in references section of project documentation
```

## Search Strategies

### IEEE Xplore Best Practices

**Finding Key Technical Documents**:

- Sort by citation count to find influential technical papers
- Look for review articles for state-of-the-art understanding
- Check "Cited by" to assess technical impact
- Use citation alerts to track new technical developments

**Advanced Operators**:

```
"exact phrase"           # Exact phrase match
author:lastname          # Search by author
intitle:keyword          # Search in title only
conference:name          # Search specific conference
-year:2023              # Exclude specific year
"power" AND "management" # Combine terms
2018..2024              # Year range
```

**Search Examples**:

```bash
# Find recent technical reviews
"5G" intitle:review 2023..2024

# Find company-specific technical patents
assignee:"Texas Instruments" "power converter"

# Find influential foundational tech
"CMOS" 1963..1980 sort:citations

# Exclude simulation-related, focus on design methodology
"antenna design" -simulation -modeling
```

## Tools and Scripts

### search_ieee_xplore.py

Search IEEE Xplore and export results.

**Features**:

- Automated search with rate limiting
- Pagination support
- Year range filtering
- Export to JSON or BibTeX
- Citation counts and impact metrics

**Usage**:

```bash
# Basic technical search
python scripts/search_ieee_xplore.py "quantum computing hardware"

# Advanced search with filters
python scripts/search_ieee_xplore.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# Export to BibTeX
python scripts/search_ieee_xplore.py "embedded security" \
  --limit 50 \
  --format bibtex \
  --output embedded_security.bib
```

### search_standards.py

Search technical standards databases.

**Features**:

- Support for complex queries (standard number, category, keyword)
- Version range filtering
- Standard status filtering
- Batch metadata retrieval
- Export to JSON or BibTeX

**Usage**:

```bash
# Simple standard search
python scripts/search_standards.py "IEC 62368"

# Complex query
python scripts/search_standards.py \
  --query '"safety" AND "audio equipment"' \
  --organizations "IEC,UL" \
  --status "current" \
  --limit 200 \
  --output audio_safety_standards.json
```

### search_google_scholar.py

Search Google Scholar for academic literature across all disciplines.

**Features**:

- Comprehensive academic literature coverage
- Cross-disciplinary search capability
- Citation count tracking
- Year range filtering
- Export to JSON or BibTeX
- No API key required (web scraping with rate limiting)

**Usage**:

```bash
# Basic academic search
python scripts/search_google_scholar.py "GaN power amplifier"

# Advanced search with filters
python scripts/search_google_scholar.py "machine learning circuit design" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 50 \
  --output ml_circuits.json

# Export to BibTeX
python scripts/search_google_scholar.py "wireless power transfer" \
  --limit 30 \
  --format bibtex \
  --output wpt_papers.bib
```

**Best Practices**:

- Use specific technical terms for better results
- Combine with IEEE Xplore for comprehensive coverage
- Respect rate limits (built-in delays between requests)
- Good for interdisciplinary hardware research
- Use for finding papers across multiple venues

### extract_metadata.py

Extract complete metadata from technical document identifiers.

**Features**:

- Support for standard numbers, vendor doc IDs, patent numbers, URLs
- Query standards organization, vendor, patent database APIs
- Handle multiple identifier types
- Batch processing
- Multiple output formats

**Usage**:

```bash
# Standard number extraction
python scripts/extract_metadata.py --standard "IEC 61010-1:2020"

# Vendor document ID extraction
python scripts/extract_metadata.py --vendor-doc "TI-SLUU551C"

# Patent number extraction
python scripts/extract_metadata.py --patent "US10245678B2"

# Extract from URL
python scripts/extract_metadata.py --url "https://ieeexplore.ieee.org/document/1234567"

# Batch processing
python scripts/extract_metadata.py --input tech_docs.txt --output references.bib
```

## Best Practices

### Technical Citation Strategy

1. **Prioritize Official Sources**: Always use latest documents from standards organizations or vendor official websites
2. **Explicit Version Information**: Annotate specific version and revision date of cited documents
3. **Parameter Consistency**: Critical device parameters must exactly match latest datasheets
4. **Standard Currency**: Use current effective standard versions, avoid referencing obsolete standards
5. **Vendor Document Tracking**: Establish update tracking mechanism for vendor documents

### Design Documentation Management

- **Version Control Integration**: Integrate technical citations with design file version control system
- **Document Status Tracking**: Establish status tracking and update reminders for technical documents
- **Cross-Validation Mechanism**: Important technical parameters require cross-validation from multiple sources
- **Archive Management**: Establish complete archives for historical versions of design documents and technical citations

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: Implement exponential backoff and respect rate limits
2. **Missing Metadata**: Verify document identifiers and try alternative sources
3. **Version Mismatches**: Always specify exact version numbers in citations
4. **Obsolete Standards**: Check standard status before citation
5. **Vendor Document Updates**: Regularly check for newer revisions

### Getting Help

- Check `references/` directory for detailed documentation
- Review script help: `python scripts/[script_name].py --help`
- Consult standards organization websites for official citation formats
- Use vendor technical support for document identification questions

## References

- IEEE Citation Guidelines: https://journals.ieeeauthorcenter.ieee.org/
- IEC Standards Portal: https://www.iec.ch/
- IPC Standards: https://www.ipc.org/
- BibTeX Format Documentation: http://www.bibtex.org/Format/
