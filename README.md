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
- ✅ **Unified Knowledge Source Config**: `/elecspeckit.kbconfig` manages all external sources (IPC standards, company KB, reference designs)
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

### 3. Knowledge Sources Configuration

Stored in `.elecspecify/memory/knowledge-sources.json`, supports 4 types:

- **standards**: Industry standards (e.g., IPC-2221B PCB design standard)
- **company_kb**: Company knowledge base (design guidelines, FA reports)
- **reference_designs**: Reference designs (TI, ADI eval boards)
- **web**: Online knowledge bases (e.g., Metaso academic search, Volces Q&A)

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

Using `uv` (recommended):

```bash
uv tool install elecspeckit-cli
```

Or using `pip`:

```bash
pip install elecspeckit-cli
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

- **Claude Code** or **Qwen Code**

Non-interactive initialization (for CI/CD):

```bash
elecspeckit init --platform claude
```

### Step 3: Use Workflow Commands in AI Assistant

In Claude Code or Qwen Code, execute commands in this recommended order:

1. **`/elecspeckit.kbconfig`** - Verify and configure external knowledge sources
2. **`/elecspeckit.constitution`** - Supplement project constraints and design principles
3. **`/elecspeckit.specify <feature-description>`** - Generate feature specification (spec.md)
4. **`/elecspeckit.plan`** - Generate architecture design (plan.md, research.md, data-model.md)
5. **`/elecspeckit.tasks`** - Generate task breakdown (tasks.md)
6. **`/elecspeckit.docs`** - Generate all 7 role-specific views

Optional quality improvement commands:

- **`/elecspeckit.clarify`** - Clarify spec ambiguities
- **`/elecspeckit.checklist`** - Generate quality checklist
- **`/elecspeckit.analyze`** - Analyze document consistency

## Workflow Commands

### Configuration Commands

#### `/elecspeckit.constitution` - Maintain Project Constitution

Create or update project-level design principles and constraints as guidelines for all feature specs.

#### `/elecspeckit.kbconfig` - Configure External Knowledge Sources

Manage knowledge sources including industry standards, company KB, reference designs, and online knowledge bases.

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

- **GitHub Issues**: https://github.com/toponex/elecspeckit-cli/issues
- **Email**: lyk0510abc@gmail.com
