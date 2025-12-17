---
name: arxiv-search
description: Search arXiv preprint repository for papers in electronic engineering, embedded systems, computer science, physics, mathematics, and related fields.
---
# arXiv Search Skill

This skill provides access to arXiv, a free distribution service and open-access archive for scholarly articles, particularly covering professional fields such as electronic engineering, embedded systems, hardware design, signal processing, IoT, RF circuits, AI accelerators, while also including related disciplines like computer science, physics, and mathematics.

## When to Use This Skill

Use this skill when you need to:

- Find the latest research papers and preprints in fields such as electronic engineering, embedded systems, and hardware design
- Search for the latest advancements in specific chip (e.g., STM32, ESP32) applications and driver development
- Access cutting-edge research in circuit design, signal integrity, power management, IoT protocols, and related areas
- Stay updated on research trends in cross-disciplinary fields like embedded AI, TinyML, and edge computing
- Find research related to hardware description languages (e.g., VHDL, Verilog) and electronic design automation (EDA) tools

## How to Use

The skill provides a Python script that searches arXiv and returns formatted results, implemented using the arxiv Python package. It can return information such as paper titles and abstracts.

### Basic Usage

**Note:** Always use the absolute path from your skills directory (shown in the system prompt above).

If running the skill from a virtual environment:

```bash
.venv/bin/python [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

Or for system Python:

```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

Replace `[YOUR_SKILLS_DIR]` with the absolute skills directory path from your system prompt (e.g., `~/.deepagents/agent/skills` or the full absolute path).

**Arguments:**

- `query` (required): The search query string (e.g., "neural networks protein structure", "single cell RNA-seq")
- `--max-papers` (optional): Maximum number of papers to retrieve (default: 10)

### Examples

Search for embedded AI related papers:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "TinyML embedded systems" --max-papers 5
```

Search for hardware security related research:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "hardware security trust verification"
```

Search for new methods in RF circuit design:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "RF circuit design machine learning"
```

## Output Format

The script returns formatted results with:

- **Title**: Paper title
- **Summary**: Abstract/summary text

Each paper is separated by blank lines for readability.

## Features

- **Relevance sorting**: Results ordered by relevance to query
- **Fast retrieval**: Direct API access with no authentication required
- **Simple interface**: Clean, easy-to-parse output
- **No API key required**: Free access to arXiv database

## Dependencies

This skill requires the `arxiv` Python package. The script will detect if it's missing and show an error.

**If you see "Error: arxiv package not installed":**

If running deepagents from a virtual environment (recommended), use the venv's Python:

```bash
.venv/bin/python -m pip install arxiv
```

Or for system-wide install:

```bash
python3 -m pip install arxiv
```

The package is not included in elecspeckit-cli by default since it's skill-specific. Install it on-demand when first using this skill.

## Using with ElecSpeckit CLI

You can combine the latest algorithms or theories found in this Skill with other skills in the CLI for practical application.

## Notes

- arXiv categories highly relevant to electronic engineering and embedded systems include:
  - cs.AR (hardware architecture)
  - cs.ET (emerging technologies, including nanoelectronics, quantum computing, etc.)
  - eess.SP (signal processing)
  - eess.AS (audio and speech processing, includes embedded DSP content)
  - physics.app-ph (applied physics)
- Papers are preprints and may not be peer-reviewed
- Results include both recent uploads and older papers
- Best for theoretical research and algorithm verification in electronic engineering, embedded systems, and hardware design fields
