# ElecSpeckit CLI

English | [简体中文](README_ZH.md)

**AI-Driven Specification-Based Development Workflow for Hardware/Electronics Projects**

ElecSpeckit CLI is a command-line tool designed specifically for hardware engineers, deeply integrated with AI programming assistants (Claude Code or Qwen Code) to help teams manage complex hardware projects in a **specification-driven** manner—from requirement clarification, architecture design, task breakdown to multi-role document generation, standardizing the entire workflow.

## Why ElecSpeckit?

Hardware project pain points:

- 📋 **Unclear Requirements**: Vague customer needs leading to costly rework
- 🏗️ **Untraceable Design Decisions**: Why this chip? Why this topology? No one remembers after months
- 👥 **Chaotic Cross-Role Collaboration**: HW engineers, test engineers, FA, PM speak different languages, lacking unified info source
- 📚 **Scattered Knowledge**: Industry standards, reference designs, company KB lack centralized access
- 🔄 **Outdated Documentation**: Design changed, BOM didn't, test cases neither—consistency nightmare

ElecSpeckit Solutions:

- ✅ **AI-Assisted Requirement Clarification**: `/elecspeckit.clarify` auto-discovers spec ambiguities with multiple-choice Q&A
- ✅ **Structured Architecture Decisions**: `/elecspeckit.plan` guides Phase 0 research (topology selection, component selection) with traceable rationale
- ✅ **Auto-Generated Role Views**: One `tasks.md` auto-generates 7 role-specific views (HW/BOM/Test/FA/PM/Datasheet/KB) with zero sync latency
- ✅ **Claude Skills Integration**: Claude Code platform supports 15 specialized Skills for component search, standards query, and design validation (Qwen platform has limited skill support)
- ✅ **Document Consistency Check**: `/elecspeckit.analyze` auto-detects inconsistencies between spec/plan/tasks, verifying requirement coverage, constitution alignment, and terminology consistency

## ⚠️ Important Notice

ElecSpeckit constrains AI output through code rules, but due to inherent limitations of the Transformer architecture, **LLMs may still produce "hallucinations" in standard names, file references, and parameter specifications**.

**Mandatory Review**: All LLM-generated design files (spec, plan, tasks, docs) must be thoroughly reviewed by engineers/designers before use to prevent hallucinated content from causing design failures. Human review is the final line of quality assurance.

## Core Concepts

### 1. Project Constitution

Stored in `.elecspecify/memory/constitution.md`, defines project-level design principles and constraints:

- Reliability Principle: All power supplies must have OCP and OVP protection
- Safety Principle: Isolation voltage must meet IEC 61010-1 standard
- Cost Constraint: Unit cost not exceeding ¥500

### 2. Feature Directory

Each feature (e.g., "AC-DC Power Module", "CAN Communication Interface") corresponds to `specs/00X-shortname/`:

- `spec.md` - Specification (requirements, acceptance criteria, clarifications)
- `plan.md` - Architecture design (Phase 0 research, module breakdown, interface definitions)
- `tasks.md` - Task breakdown (with `[VIEW:XXX]` tags for different roles)
- `docs/` - Auto-generated 7 role-specific view documents

### 3. Claude Skills (Claude Code Only)

Claude Code platform provides 15 specialized Skills (stored in `.claude/skills/`):

- **Component Search**: Query Mouser, Digikey, LCSC, ICkey for component availability and pricing
- **Standards Query**: Access local IPC/ISO standards and reference designs
- **Design Validation**: Automated checks against project constitution and industry best practices

**Note**: Qwen Code platform does not support Skills functionality. Some advanced features (automatic knowledge base queries, document discovery) will be unavailable on Qwen platform.

### 4. Role-Based Views

Auto-extracted from `tasks.md` based on `[VIEW:XXX]` tags to generate role-specific documents:

- `[VIEW:HW]` → `docs/hw-view.md` - HW engineer focus (schematics, component selection)
- `[VIEW:BOM]` → `docs/bom-view.md` - BOM engineer focus (materials, suppliers, cost)
- `[VIEW:TEST]` → `docs/test-view.md` - Test engineer focus (acceptance scenarios, test cases)
- `[VIEW:FA]` → `docs/fa-view.md` - FA engineer focus (DFM assessment, test points)
- `[VIEW:PM]` → `docs/pm-view.md` - PM focus (milestones, risks, schedule)
- `[VIEW:DATASHEET]` → `docs/product-doc.md` - External product docs (filtering internal info)
- `[VIEW:KB]` → `docs/kb-view.md` - KB admin focus (design lessons, ADR records)

## Installation

Clone the repository and install from source:

```bash
# Clone from GitHub
git clone https://github.com/Toponex/elecspeckit-cli.git
cd elecspeckit-cli

# Install using uv
uv tool install .
```

## Quick Start

### Step 1: Check System Environment

Check tool availability before initialization:

```bash
elecspeckit check
```

### Step 2: Initialize Project

Initialize ElecSpeckit project in an empty directory:

```bash
cd /path/to/your/hardware-project
elecspeckit init
```

Interactive platform selection:

- **Claude Code (recommended)** - Full Skills support with 15 specialized tools
- **Qwen Code** - Basic functionality, limited Skills support

Non-interactive initialization (for CI/CD):

```bash
elecspeckit init --platform claude
```

### Step 3: Use Workflow Commands in AI Assistant

In Claude Code or Qwen Code, execute commands in this recommended order:

1. **`/elecspeckit.constitution`** - Define project constraints and design principles
2. **`/elecspeckit.specify <feature-description>`** - Generate feature specification (spec.md)
3. **`/elecspeckit.plan`** - Generate architecture design (plan.md, research.md, data-model.md)
4. **`/elecspeckit.tasks`** - Generate task breakdown (tasks.md)
5. **`/elecspeckit.docs`** - Generate all 7 role-specific views

Optional quality improvement commands:

- **`/elecspeckit.clarify`** - Clarify spec ambiguities
- **`/elecspeckit.checklist`** - Generate quality checklist
- **`/elecspeckit.analyze`** - Analyze document consistency

## Workflow Commands

### Configuration Commands

#### `/elecspeckit.constitution` - Maintain Project Constitution

Create or update project-level design principles and constraints as guidelines for all feature specs.

### Spec & Architecture Commands (P1 Core Workflow)

#### `/elecspeckit.specify <feature-description>` - Generate Feature Specification

Auto-create or update `specs/00X-shortname/spec.md` from simple feature description, including user stories, acceptance criteria, and clarifications.

#### `/elecspeckit.plan` - Generate Architecture Design

Based on `spec.md`, generate `plan.md` (architecture), `research.md` (Phase 0 research), and `data-model.md` (interface definitions).

### Task & Document Commands

#### `/elecspeckit.tasks` - Generate Task Breakdown

Based on `plan.md`, generate dependency-ordered `tasks.md` with role tags (`[VIEW:XXX]`) and task types (`[MANUAL]`/`[AUTO]`).

#### `/elecspeckit.doc-hw` - Generate HW Engineer View

Extract `[VIEW:HW]` tasks from `tasks.md` to generate `docs/hw-view.md`.

#### `/elecspeckit.doc-bom` - Generate BOM/Supply Chain View

Extract `[VIEW:BOM]` tasks to generate `docs/bom-view.md`.

#### `/elecspeckit.doc-test` - Generate Test View

Extract acceptance scenarios and `[VIEW:TEST]` tasks to generate `docs/test-view.md`.

#### Other document generation commands:

- `/elecspeckit.doc-fa` - FA/Manufacturing view
- `/elecspeckit.doc-pm` - Project manager view
- `/elecspeckit.doc-datasheet` - Product documentation view
- `/elecspeckit.doc-kb` - Knowledge base view

### Quality Assistance Commands (P3)

#### `/elecspeckit.clarify` - Clarify Spec Ambiguities

Analyze `spec.md` to auto-discover ambiguous, contradictory, or missing requirements, presenting them as multiple-choice questions.

#### `/elecspeckit.checklist` - Generate Quality Checklist

Generate checklists based on `tasks.md` to ensure all tasks are verified.

#### `/elecspeckit.analyze` - Analyze Document Consistency

Comprehensive analysis of `spec.md`, `plan.md`, `tasks.md`, and `constitution.md`, outputting structured report identifying inconsistencies, gaps, and conflicts.

### Skills Configuration Management (Claude Code Only)

#### `/elecspeckit.skillconfig` - Manage Claude Skills

Manage deployed Claude Skills' enable/disable status, API key configuration, and consistency validation.

**Note**: This command is only available on Claude Code platform. Qwen Code does not support Skills functionality.

**Subcommands**:

##### `list` - List All Skills
```bash
/elecspeckit.skillconfig list [--format json|text]
```

Display all deployed Skills and their status (enabled/disabled, API configuration).

**Example output**:
```
Deployed Claude Skills (24 total):

Status  Skill Name                    API Req  API Config  Description
==================================================================
[✓]     docs-seeker                   No       N/A         Find technical docs
[✗]     mouser-component-search       Yes      Unconfigured Mouser API integration
[✓]     arxiv-search                  No       N/A         Search academic papers
...

Statistics:
  - Enabled: 20
  - Disabled: 4
  - Requires API: 3 (1 unconfigured)
```

##### `enable` - Enable Skill
```bash
/elecspeckit.skillconfig enable <skill_name>
```

Set specified Skill to enabled state, allowing Claude Code to load it.

**Example**:
```bash
/elecspeckit.skillconfig enable arxiv-search
```

##### `disable` - Disable Skill
```bash
/elecspeckit.skillconfig disable <skill_name>
```

Set specified Skill to disabled state, preventing Claude Code from loading it.

**Use Cases**:
- Temporarily disable unneeded Skills to improve loading speed
- Disable Skills requiring API keys that haven't been configured yet

##### `update` - Update API Key
```bash
/elecspeckit.skillconfig update <skill_name> --api-key <key>
```

Update API key configuration for Skills requiring external APIs (e.g., `mouser-component-search`).

**Example**:
```bash
/elecspeckit.skillconfig update mouser-component-search --api-key "YOUR_MOUSER_API_KEY"
```

**Security Notes**:
- API keys are stored in `.elecspecify/memory/skill_config.json` with file permission 0600
- Python scripts execute server-side, keys are not passed to LLM context
- SKILL.md files contain only placeholder examples, never actual keys

##### `validate` - Validate Configuration Consistency
```bash
/elecspeckit.skillconfig validate
```

Validate consistency between `skill_config.json` and actual SKILL.md files in `.claude/skills/` directory.

**Complete Workflow Example**:
```bash
# 1. View current Skills status
/elecspeckit.skillconfig list

# 2. Configure Mouser API key
/elecspeckit.skillconfig update mouser-component-search --api-key "YOUR_KEY"

# 3. Enable mouser-component-search Skill
/elecspeckit.skillconfig enable mouser-component-search

# 4. Validate configuration consistency
/elecspeckit.skillconfig validate
```

## Upgrading Existing Projects

In an already initialized ElecSpeckit project, re-run initialization to update templates:

```bash
elecspeckit init
```

### Upgrade Behavior

The upgrade process will:

- **Auto-detect existing platform config** (no re-selection needed)
- **Only update template files**:
  - `.claude/commands/elecspeckit.*.md` or `.qwen/commands/elecspeckit.*`
  - `.elecspecify/templates/*`
  - `.elecspecify/scripts/*`
- **Generate backups**: Auto-create `.bak.YYYYMMDD-HHMMSS` backups for changed files
- **Protect user content**:
  - ✅ Business docs under `specs/` won't be modified
  - ✅ `.elecspecify/memory/constitution.md` won't be overwritten (unless `--reset`)
  - ✅ Files with identical content will be skipped

### Upgrading from v0.1.0 to v0.2.0

When upgrading from v0.1.0:

1. **Automatic Detection and Backup**:
   - Running `elecspeckit init` automatically detects v0.1.0 projects
   - Old kb_config configuration files are automatically backed up to `.elecspecify/backup/`

2. **Claude Skills Auto-Deployment**:
   - When selecting Claude Code platform, 23+ Skills are automatically deployed to `.claude/skills/`
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

### Reset constitution.md

To restore `constitution.md` to official template initial state:

```bash
elecspeckit init --reset
```

## Common Issues

### Git Not Available

If git is not installed, CLI will skip git initialization with a prompt. You can manually run `git init` later.

### Multi-Platform Config Conflict

If both `.claude/` and `.qwen/` exist, CLI will error:

```
Detected multiple AI platform configs (.claude/ and .qwen/ both exist), please manually delete one and retry
```

**Solution**: Delete one platform directory, then re-run `elecspeckit init`.

## Version History

### v0.2.0 (Current Version)

**Major Changes**:
- ✨ **Claude Skills Support**: Claude Code platform now supports 23+ professional Skills stored in `.claude/skills/` directory
- 🔄 **Removed kb_config Mechanism**: Old `knowledge-sources.json` and `/elecspeckit.kbconfig` commands replaced by Claude Skills
- 📦 **Skills Auto-Deployment**: Automatically deploy Skills for information retrieval, document generation, data analysis, and embedded development when initializing Claude projects
- ⚙️ **New `/elecspeckit.skillconfig` Command**: Manage Skills enable/disable and API key configuration
- 🔒 **Enhanced Security**: API keys stored in permission-restricted `skill_config.json` file (owner read-only)

**Skills Categories**:
- **Information Retrieval (5)**: docs-seeker, arxiv-search, web-research, perplexity-search, openalex-database
- **Document Generation & Visualization (7)**: docx, pdf, xlsx, pptx, architecture-diagrams, mermaid-tools, docs-write
- **Data Analysis (2)**: hardware-data-analysis, citation-management
- **Embedded Development (4)**: embedded-systems, hardware-protocols, esp32-embedded-dev, embedded-best-practices
- **Component Procurement (1)**: mouser-component-search
- **Domain Analysis (3)**: circuit-commutation-analysis, thermal-simulation, emc-analysis (placeholder)
- **Meta Skill (1)**: skill-creator

**Upgrade Notes**:
- v0.1.0 projects will have old kb_config configurations automatically backed up to `.elecspecify/backup/`
- After upgrade, use `/elecspeckit.skillconfig` to manage Skills (no manual configuration needed)

**Known Issues** (to be resolved in v0.2.1):
- Python scripts for some Skills (mouser-component-search, perplexity-search) not fully implemented
- Some Skills' SKILL.md missing ElecSpeckit integration guide section
- esp32-embedded-dev and hardware-protocols SKILL.md format incomplete

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

---

### v0.1.0

Initial release with core specification-driven workflow:
- Project initialization with platform selection (Claude Code / Qwen Code)
- 15 workflow commands for hardware project management
- Role-based document generation (7 views)
- Knowledge sources configuration (replaced by Skills in v0.2.0)
- Hardware-appropriate testing classification (L1/L2/L3)



## License

```
Copyright 2025 Yongkai Li@Toponex

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## Feedback & Contribution

If you encounter issues or have suggestions, please provide feedback via:

- **GitHub Issues**: https://github.com/Toponex/elecspeckit-cli/issues
- **Email**: lyk0510abc@gmail.com
