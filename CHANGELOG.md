# Changelog

All notable changes to ElecSpeckit CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
