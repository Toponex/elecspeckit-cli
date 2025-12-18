---
name: docs-write
description: Write documentation following conversational, clear, and user-focused style. Use when creating or editing documentation files (markdown, MDX, etc.) for ElecSpeckit CLI and hardware engineering projects.
allowed-tools: Read, Write, Grep, Bash, Glob
version: "1.0.0"
---
# Documentation Writing Skill

Write conversational, clear, and user-focused documentation.

## Overview

This skill provides proven documentation writing guidelines and best practices to help you create clear, useful, and easy-to-understand technical documentation. Whether writing API docs, user guides, or technical specifications, these principles help you create high-quality documentation.

## When to Use

- Create or edit Markdown documents
- Write MDX files
- Write README files
- Create API documentation
- Write user guides
- Write technical specifications
- Write tutorials and how-to guides
- Create release notes
- Write troubleshooting documentation
- Write hardware design documentation
- Write embedded systems development guides

## Core Principles

### 1. Know Your Audience

Before you start writing, ask yourself three questions:

1. **Who is this for?** Match complexity to audience. Don't oversimplify hard things or overcomplicate simple ones.

   - **Beginners**: Need more context and step-by-step guidance
   - **Experienced developers**: Can skim quickly, want key information fast
   - **Mixed audience**: Provide layered information, use "Advanced" sections
2. **What do they need?** Get them to the answer fast. Nobody wants to be in docs longer than necessary.

   - Show most common use cases first
   - Put advanced topics in separate sections
   - Provide clear navigation structure
3. **What did you struggle with?** Those common questions you had when learning? Answer them (without literally including the question).

   - Document your "aha" moments
   - Clarify easily confused concepts
   - Provide concrete examples, not abstract explanations

### 2. Writing Process

#### Draft Phase

- **Write out the steps/explanation as you'd tell a colleague**

  - Use natural language
  - Avoid overly formal phrasing
  - Imagine you're explaining face-to-face
- **Lead with what to do, then explain why**

  ```markdown
  ✅ Good:
  Set SAML before adding users. This ensures all users use SSO login from the start.

  ❌ Bad:
  To ensure all users can use SSO login, you need to set up SAML before adding users...
  ```
- **Use headings that state your point**

  ```markdown
  ✅ Good: Set SAML before adding users
  ❌ Bad: SAML configuration timing
  ```

#### Edit Phase

- **Read aloud. Does it sound like you talking?** If it's too formal, simplify.

  ```markdown
  ✅ Good: Open the config file and change the port number.
  ❌ Bad: The port parameter in the configuration file should be modified to update the service listening port.
  ```
- **Cut anything that doesn't directly help the reader**

  - Remove redundant explanations
  - Don't repeat obvious things
  - Delete filler words like "as you know", "obviously"
- **Check each paragraph has one clear purpose**

  - Each paragraph should convey one main idea
  - If a paragraph covers multiple topics, split it
  - Use transition sentences to connect paragraphs
- **Verify examples actually work** (don't give examples that error)

  - Run all code examples
  - Test all commands
  - Ensure version compatibility

#### Polish Phase

- **Make links descriptive** (never "here")

  ```markdown
  ✅ Good: Check out the [SAML documentation](link) for detailed configuration steps.
  ❌ Bad: Click [here](link) for more information.
  ```
- **Backticks only for code/variables, bold for UI elements**

  ```markdown
  ✅ Good: Click the **Filter** button and set the `max_connections` parameter.
  ❌ Bad: Click the `Filter` button and set the **max_connections** parameter.
  ```
- **American spelling, serial commas**

  - Use American spelling in English content
  - Use commas before the last item in a list
  - Keep terminology consistent
- **Keep images minimal and scoped tight**

  - Only use images when text can't explain clearly
  - Crop images to show only relevant parts
  - Use annotations or arrows to highlight key points
  - Provide alt text

#### Format Phase

For projects using specific formatting tools (like Prettier), run formatting after edits:

```bash
yarn prettier --write <file-path>
```

This ensures consistent formatting across all documentation.

## Common Patterns

### Instructions

**Recommended**:

```markdown
Run:
\`\`\`bash
command-to-run
\`\`\`

Then:
\`\`\`bash
next-command
\`\`\`

This ensures you're getting the latest changes.
```

**Not**: "(remember to run X before Y...)" buried in a paragraph.

### Headings

```markdown
✅ Good: Use environment variables for configuration
❌ Bad: Environment variables (too vague)
❌ Bad: How to use environment variables for configuration (too wordy)
```

### Links

```markdown
✅ Good: Check out the [SAML documentation](link)
❌ Bad: Read the docs [here](link)
```

## Watch Out For

### 1. Don't describe tasks as "easy"

You don't know the reader's context. What's easy for you might be hard for them.

```markdown
❌ Bad: Simply add the configuration...
✅ Good: Add the configuration...
```

### 2. Be specific about product names

When talking about features, use "ElecSpeckit" or "it", not "we":

```markdown
❌ Bad: We provide powerful search functionality...
✅ Good: ElecSpeckit provides powerful search functionality...
```

### 3. Avoid overly formal language

- "utilize" → "use"
- "reference" → "check" or "see"
- "offerings" → "features" or "options"

### 4. Don't be too peppy

Avoid multiple exclamation points:

```markdown
❌ Bad: This is amazing! You'll love it! Let's get started!
✅ Good: This feature helps you work faster. Let's get started.
```

### 5. Don't bury the action in explanation

Lead with what to do, then explain:

```markdown
❌ Bad: Because you need to ensure data consistency, you should run this command...
✅ Good: Run this command to ensure data consistency:
```

### 6. Test your code examples

Always verify code examples work. Don't give examples that error.

### 7. Avoid numbers that will become outdated

```markdown
❌ Bad: As of 2024, we have 50 Skills...
✅ Good: ElecSpeckit provides multiple Skills...
```

## Quick Reference

### Word Choice

| Write This              | Not This                             |
| ----------------------- | ------------------------------------ |
| people, companies       | users (in generic context)           |
| summarize               | aggregate (unless technical term)    |
| take a look at          | reference                            |
| can't, don't            | cannot, do not                       |
| **Filter** button | `Filter` button                    |
| Check out the[docs](link)  | Click[here](link)                       |
| Set `DEBUG=true`      | Set**DEBUG** to **true** |

### Formatting Conventions

| Element        | Format                       | Example                          |
| -------------- | ---------------------------- | -------------------------------- |
| UI elements    | **bold**               | Click the**Save** button   |
| Code/variables | `backticks`                | Set `max_retries` to 3         |
| File paths     | `backticks`                | Edit `config/settings.yaml`    |
| Commands       | ` ```code block``` `       | See examples below               |
| Emphasis       | *italic* or **bold** | *Important*: Back up your data |
| Key presses    | `backticks`                | Press `Ctrl+C` to exit         |

## Document Type Guidelines

### API Documentation

**Structure**:

```markdown
## Method Name

Brief description of what the method does.

### Parameters

- `param1` (type): Description
- `param2` (type, optional): Description

### Returns

Return type and description.

### Example

\`\`\`python
result = method_name(param1="value")
print(result)
\`\`\`

### Errors

- `ErrorType1`: When thrown
- `ErrorType2`: When thrown
```

**Key Points**:

- Always include working examples
- Document all parameters, including optional ones
- Specify return value types
- List possible errors/exceptions

### User Guides

**Structure**:

```markdown
# Title

## What You'll Learn

Brief list.

## Prerequisites

- Requirement 1
- Requirement 2

## Steps

### Step 1: Do Something

Specific instructions.

### Step 2: Do Something Else

More instructions.

## Troubleshooting

Common problems and solutions.
```

**Key Points**:

- Start with learning objectives
- List prerequisites
- Use numbered steps
- Include troubleshooting section

### Technical Specifications

**Structure**:

```markdown
# Feature Name

## Overview

High-level description.

## Goals

- Goal 1
- Goal 2

## Technical Design

### Architecture

Description or diagram.

### Data Model

Tables, fields, etc.

### API Design

Endpoints and methods.

## Implementation Plan

Phases or milestones.

## Testing Strategy

How to verify.
```

**Key Points**:

- Clear objectives
- Include architecture diagrams
- Detailed data models
- Define acceptance criteria

### Embedded Systems Documentation

**Hardware Configuration**:

```markdown
## Hardware Connections

| ESP32 Pin | Component | Description |
|-----------|-----------|-------------|
| GPIO 21 | SDA | I2C data line |
| GPIO 22 | SCL | I2C clock line |
| 3.3V | VCC | Power supply (3.3V) |
| GND | GND | Ground |
```

**Code Examples**:

```markdown
### Initialize I2C

\`\`\`c
#include <Wire.h>

void setup() {
  Wire.begin(21, 22);  // SDA=21, SCL=22
  Serial.begin(115200);
}
\`\`\`
```

### ElecSpeckit CLI Documentation

**Command Documentation**:

```markdown
## /speckit.init

Initialize ElecSpeckit project structure.

### Usage

\`\`\`bash
elecspeckit init [options]
\`\`\`

### Options

- `--platform <name>`: Target platform (claude, cursor)
- `--force`: Overwrite existing files
- `--verbose`: Show detailed output

### Example

\`\`\`bash
# Initialize for Claude platform
elecspeckit init --platform claude

# Force overwrite with verbose output
elecspeckit init --platform cursor --force --verbose
\`\`\`

### What Gets Created

- `.elecspecify/` - Configuration directory
- `skills/` - Skill definitions
- `templates/` - Document templates
- `constitution.md` - Project principles

### Troubleshooting

**Issue**: Permission denied when creating directories

**Solution**: Ensure you have write permissions in the target directory.
```

**Skill Documentation**:

```markdown
## Skill Name

Brief description of what the skill does.

### When to Use

- Use case 1
- Use case 2
- Use case 3

### Features

- Feature 1
- Feature 2
- Feature 3

### Example Workflows

#### Basic Usage

Step-by-step example.

#### Advanced Usage

More complex example.

### Configuration

Required configuration and optional settings.

### API Keys

If the skill requires API keys, explain how to set them up.

### Troubleshooting

Common issues and solutions.
```

**Hardware Design Documentation**:

```markdown
## PCB Design Guidelines

### Layer Stackup

\`\`\`
Layer 1: Signal (Top)
Layer 2: Ground
Layer 3: Power
Layer 4: Signal (Bottom)
\`\`\`

### Design Rules

| Parameter | Value | Standard |
|-----------|-------|----------|
| Trace width (signal) | 0.2mm | IPC-2221 |
| Clearance | 0.15mm | IPC-2221 |
| Via diameter | 0.3mm | IPC-2221 |

### Component Placement

1. Place critical components first
2. Group by function
3. Consider signal flow
4. Minimize trace lengths for high-speed signals

### References

- IPC-2221B: Generic Standard on Printed Board Design
- IPC-A-610: Acceptability of Electronic Assemblies
```

## Checklist

Before publishing documentation, check:

- [ ] Is the title clear about what's inside?
- [ ] Is there a clear audience?
- [ ] Are steps in logical order?
- [ ] Have all code examples been tested?
- [ ] Are links descriptive?
- [ ] Do images have alt text?
- [ ] Is the right formatting used (bold vs backticks)?
- [ ] Is the tone friendly but professional?
- [ ] Have you removed unnecessary content?
- [ ] Does it sound natural when read aloud?
- [ ] Are technical terms defined on first use?
- [ ] Is version information included where relevant?

## ElecSpeckit-Specific Guidelines

### Constitution Documentation

When documenting project principles:

- Keep principles concise (1-2 sentences each)
- Make principles actionable
- Explain the "why" behind each principle
- Use examples to illustrate principles
- Reference specific standards or best practices

### Template Documentation

When documenting templates:

- Show both the template structure and filled example
- Explain each section's purpose
- Note which sections are required vs optional
- Provide guidance on how to customize
- Link to related skills or tools

### Slash Command Documentation

Format slash commands consistently:

```markdown
### /command.name

Brief description.

**Usage**: `/command.name [arguments]`

**Example**:
\`\`\`bash
/command.name --option value
\`\`\`

**What it does**:
1. Action 1
2. Action 2
3. Action 3
```

### Hardware-Specific Terminology

Keep technical terms in English even in non-English docs:

- PCB, FPGA, MCU, ADC, DAC
- I2C, SPI, UART, CAN
- GPIO, PWM, ADC, DAC
- EMI, EMC, ESD, RF

Provide Chinese translations in parentheses on first use if needed.

## Tools and Resources

### Useful Commands

```bash
# Format markdown files
prettier --write "**/*.md"

# Check links in markdown
markdown-link-check README.md

# Spell check
aspell check document.md
```

### Reference Links

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [IPC Standards](https://www.ipc.org/) for hardware documentation
- [IEEE Standards](https://standards.ieee.org/) for technical documentation
