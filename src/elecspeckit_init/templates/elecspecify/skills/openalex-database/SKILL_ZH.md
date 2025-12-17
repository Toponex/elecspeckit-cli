---
name: openalex-database
description: Query and analyze scholarly literature using the OpenAlex database. This skill should be used when searching for academic papers, analyzing research trends, finding works by authors or institutions, tracking citations, discovering open access publications, or conducting bibliometric analysis across 240M+ scholarly works. Use for literature searches, research output analysis, citation analysis, and academic database queries.
---


# [需要翻译] Skill 名称

**注意**: 此文档为自动生成的占位符，需要完整的中文翻译。

## 翻译要求

1. 保留 YAML front matter（上方 --- 之间的内容）不变
2. 翻译所有英文内容为中文
3. 保留技术术语为英文：Claude Code, /elecspeckit.*, API, JSON, YAML, Python
4. 保持与 SKILL.md 相同的章节结构
5. 确保文档长度 >= 200 行（SC-002）

## 原始英文内容（供参考）

```
# OpenAlex Database

## Overview

OpenAlex is a comprehensive open catalog of 240M+ scholarly works, authors, institutions, topics, sources, publishers, and funders. This skill provides tools and workflows for querying the OpenAlex API to search literature, analyze research output, track citations, and conduct bibliometric studies.

## Quick Start

### Basic Setup

Always initialize the client with an email address to access the polite pool (10x rate limit boost):

```python
from scripts.openale
...
```
