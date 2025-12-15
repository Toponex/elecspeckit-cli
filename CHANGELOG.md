# Changelog

All notable changes to ElecSpeckit CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-15

### Added

#### Claude Skills Support
- ✨ **23+ Professional Skills Auto-Deployment**: Automatically deploy the following Skills to `.claude/skills/` when initializing Claude Code projects:
  - **Information Retrieval (5)**: docs-seeker, arxiv-search, web-research, perplexity-search, openalex-database
  - **Document Generation & Visualization (7)**: docx, pdf, xlsx, pptx, architecture-diagrams, mermaid-tools, docs-write
  - **Data Analysis (2)**: hardware-data-analysis, citation-management
  - **Embedded Development (4)**: embedded-systems, hardware-protocols, esp32-embedded-dev, embedded-best-practices
  - **Component Procurement (1)**: mouser-component-search
  - **Domain Analysis (3)**: circuit-commutation-analysis, thermal-simulation, emc-analysis (placeholder)
  - **Meta Skill (1)**: skill-creator

- ⚙️ **New `/elecspeckit.skillconfig` Command**: Complete Skills configuration management with 5 subcommands:
  - `list`: List all Skills and their status (supports JSON and text format)
  - `enable`: Enable specified Skill (updates config + renames file)
  - `disable`: Disable specified Skill (updates config + renames file)
  - `update`: Update API key configuration (supports atomic update and validation)
  - `validate`: Validate consistency between configuration and files

- 📦 **Skills Automated Management**:
  - Atomic configuration update mechanism (temp file + validation + rename)
  - Smart merge: Preserve user-configured API keys and enabled status during upgrades
  - Automatic backup: Backup to `.elecspecify/backup/skills.bak.YYYYMMDD-HHMMSS/` before upgrade

- 🔒 **Enhanced API Security Architecture**:
  - API keys stored in `.elecspecify/memory/skill_config.json` with file permission 0600
  - Python scripts execute on server side, keys not passed to LLM context
  - Returns structured data without sensitive information
  - Complete security audit (automated scanning + manual code review)

#### Testing & Quality Assurance
- ✅ **Comprehensive Test Coverage**:
  - Unit tests: 47 tests passed
  - Integration tests: 37 tests passed
  - Contract tests: 17 tests passed
  - All core framework functionality verified

- 📋 **Contract Documentation**:
  - `contracts/skillconfig_scripts_contract.md`: Defines skillconfig script I/O contracts and atomic update mechanism
  - `contracts/api_error_schema.json`: Defines API error response format specification
  - `contracts/component_search_api_reference.md`: Defines Mouser API call specification
  - `contracts/skill_config_schema.json`: Defines Skills configuration file JSON Schema

### Changed

- 🔄 **Removed kb_config Mechanism**:
  - Deleted old `knowledge-sources.json` configuration file
  - Deleted `/elecspeckit.kbconfig` command and all subcommands
  - Deleted all kbconfig Python scripts (kbconfig_add.py, kbconfig_update.py, kbconfig_validate.py, kbconfig_list.py, kbconfig_delete.py)
  - Functionality completely replaced by Claude Skills mechanism

- 📝 **Platform Selection Optimization**:
  - Claude Code marked as "Claude Code (recommended)"
  - Qwen Code displays warning after selection: "Note: Qwen platform does not support Claude Skills functionality. Some advanced features (e.g., automatic knowledge base queries, document discovery) will be unavailable"

- 📚 **Documentation Updates**:
  - README_ZH.md added detailed `/elecspeckit.skillconfig` command documentation
  - Added complete usage scenarios and security notes
  - Updated version changelog (v0.2.0 section)

### Removed

- ❌ **Codex Platform Support**: Completely removed Codex-related templates and test files
- ❌ **kb_config Related Files**:
  - `.claude/commands/elecspeckit.kbconfig.md`
  - `.claude/scripts/win/python/kbconfig_*.py`
  - `.claude/memory/knowledge-sources.json`
  - `.qwen/commands/elecspeckit.kbconfig.toml`
  - `.qwen/scripts/kbconfig_*.py`
  - `.qwen/memory/knowledge-sources.json`
  - `packages/elecspeckit-cli/src/elecspeckit_init/templates/codex/`

### Security

- 🔐 **API Key Security Audit Passed**:
  - No hardcoded API keys found
  - SKILL.md only contains placeholder examples
  - Key storage file permissions correct (0600)
  - Complies with FR-025.1 API security architecture requirements

### Upgrade Guide

Upgrading from v0.1.0 to v0.2.0:

1. **Automatic Detection and Backup**:
   - Running `elecspeckit init` automatically detects v0.1.0 projects
   - Old kb_config configuration files automatically backed up to `.elecspecify/backup/`

2. **Claude Skills Auto-Deployment**:
   - When selecting Claude Code platform, 23+ Skills automatically deployed to `.claude/skills/`
   - Generates `.elecspecify/memory/skill_config.json` configuration file

3. **Configure API Keys** (optional):
   ```bash
   /elecspeckit.skillconfig update mouser-component-search --api-key "YOUR_KEY"
   /elecspeckit.skillconfig enable mouser-component-search
   ```

4. **Verify Upgrade**:
   ```bash
   /elecspeckit.skillconfig list
   /elecspeckit.skillconfig validate
   ```

### Known Issues

The following issues will be resolved in v0.2.1:

- ⚠️ Python scripts for some Skills (mouser-component-search, perplexity-search) not fully implemented
- ⚠️ Some Skills' SKILL.md missing ElecSpeckit integration guide section
- ⚠️ esp32-embedded-dev and hardware-protocols SKILL.md format incomplete
- ⚠️ Need to add cross-platform file permission verification tests

### Dependencies

New dependency libraries (automatically installed via `uv tool install .`):

**Scientific Computing Libraries**:
- numpy>=1.24.0
- scipy>=1.10.0
- pandas>=2.0.0
- matplotlib>=3.7.0

**Document Processing Libraries**:
- python-docx>=0.8.11
- PyPDF2>=3.0.0
- openpyxl>=3.1.0
- python-pptx>=0.6.21

**Network & API Libraries**:
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- litellm>=1.0.0
- pyalex>=0.13
- pypuppeteer>=1.0.0
- arxiv>=2.0.0

**Embedded Development (Optional)**:
- pyserial>=3.5 (install via `uv tool install .[embedded]`)
- esptool>=4.5 (install via `uv tool install .[embedded]`)

---

## [0.1.0] - 2025-12-09

### Added
- **Project Initialization**: Interactive platform selection (Claude Code / Qwen Code) with `elecspeckit init`
- **System Check**: Pre-initialization environment validation with `elecspeckit check`
- **15 Workflow Commands** for hardware project management:
  - `/elecspeckit.constitution` - Maintain project constitution
  - `/elecspeckit.kbconfig` - Configure external knowledge sources
  - `/elecspeckit.specify` - Generate feature specifications
  - `/elecspeckit.plan` - Generate architecture design documents
  - `/elecspeckit.tasks` - Generate task breakdown
  - `/elecspeckit.doc-hw` - Generate HW engineer view
  - `/elecspeckit.doc-bom` - Generate BOM/supply chain view
  - `/elecspeckit.doc-test` - Generate test view
  - `/elecspeckit.doc-fa` - Generate FA/manufacturing view
  - `/elecspeckit.doc-pm` - Generate project manager view
  - `/elecspeckit.doc-datasheet` - Generate product documentation view
  - `/elecspeckit.doc-kb` - Generate knowledge base view
  - `/elecspeckit.clarify` - Clarify spec ambiguities
  - `/elecspeckit.checklist` - Generate quality checklist
  - `/elecspeckit.analyze` - Analyze document consistency
- **Knowledge Sources Configuration**: Support for 4 types (standards, company_kb, reference_designs, web)
- **Role-Based Views**: Auto-generate 7 role-specific documents from tasks.md
- **Project Upgrade**: Re-run `elecspeckit init` to update templates with automatic backup
- **Git Integration**: Automatic repository initialization with `.gitignore`
- **Template Backup**: Timestamped backups (`.bak.YYYYMMDD-HHMMSS`) when upgrading
- **Internationalization**: English README.md and Chinese README_ZH.md with language switchers

### Fixed
- **Hardware Testing Templates**: Replaced software TDD assumptions with hardware-appropriate three-layer testing classification:
  - **L1 (Calculation/Simulation)**: Programmable tests (SPICE, parameter calculations) - "write test scripts"
  - **L2 (Prototype Functional Testing)**: Requires hardware (voltage, ripple, efficiency) - "write test plans + optional automation"
  - **L3 (Environmental/Certification Testing)**: Requires specialized equipment (EMC, temperature cycling, aging) - "write submission plans"
- Updated `tasks-template.md`, `elecspeckit.tasks.md`, and `constitution-template.md` with L1/L2/L3 classification
- Changed constitution chapter from "测试驱动与集成测试要求" to "验证与测试策略" (Verification & Test Strategy)

### Changed
- **License**: Apache License 2.0 with NOTICE file (includes Specify attribution)
- **Repository URLs**: Unified to https://github.com/Toponex/elecspeckit-cli
- **Package Metadata**: Updated author email to lyk0510abc@gmail.com
- **Documentation**: All package metadata (pyproject.toml, README.md) now in English to avoid encoding issues

### Documentation
- Comprehensive English README.md (242 lines) with installation, quick start, and all workflow commands
- Detailed Chinese README_ZH.md (836 lines) with step-by-step guides and usage scenarios
- LLM hallucination warning in both language versions
- Pre-release checklist and common issues documented

---

## Future Releases

### Planned Features
- Additional document generation commands
- Enhanced knowledge source query capabilities
- Improved template customization
- Multi-project workspace support

---

For detailed development progress, see: https://github.com/Toponex/elecspeckit-cli
