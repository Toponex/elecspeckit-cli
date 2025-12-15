---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
requires_api: false
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Dependencies

### Python Libraries

```bash
pip install pypdf pdfplumber reportlab pytesseract pdf2image
```

**说明**:
- `pypdf`: PDF reading, writing, merging, splitting
- `pdfplumber`: Text and table extraction with layout preservation
- `reportlab`: PDF generation from scratch
- `pytesseract`: OCR for scanned PDFs (requires Tesseract system tool)
- `pdf2image`: Convert PDF pages to images

### System Tools

- **poppler-utils**: Command-line PDF tools (pdftotext, pdfimages)
- **qpdf**: Advanced PDF manipulation
- **Tesseract OCR**: For scanning text from images in PDFs

## 使用

此 Skill 提供全面的 PDF 处理能力，支持：
- **提取内容**：文本、表格、图片、元数据提取
- **创建 PDF**：从零开始生成 PDF 文档
- **合并与拆分**：合并多个 PDF 或拆分单个 PDF
- **表单处理**：填写和提取 PDF 表单数据
- **OCR 识别**：从扫描 PDF 中提取文本

典型使用场景：
- 批量 PDF 处理和自动化
- 文档内容提取和分析
- 报告生成和模板填充
- 数据表格提取到 Excel

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## ElecSpeckit 集成指南

此 Skill 在 ElecSpeckit 工作流的文档处理和数据提取阶段自动使用，帮助从数据手册、应用笔记和标准文档中提取关键信息。

### 在 /elecspeckit.specify 中使用

**场景**: 从数据手册提取电气参数

```
用户: /elecspeckit.specify AC-DC 电源模块

AI: [内部调用] pdf Skill:
    从 TPS54620 数据手册提取参数:
    - 使用 pdfplumber 提取电气特性表格
    - 解析输入电压范围、输出电流规格
    - 转换为结构化数据

    在 spec.md 中引用提取的参数:
    - 输入电压: 4.5V - 17V (来源: TPS54620 数据手册 Table 6-1)
    - 输出电流: 最大 6A
```

### 在 /elecspeckit.plan 中使用

**场景**: 提取参考设计原理图和应用笔记

```
用户: /elecspeckit.plan

AI: Phase 0 研究 - LLC 拓扑设计

    [内部调用] pdf Skill:
    - 提取 TI AN-4151 应用笔记中的设计公式
    - 从参考设计PDF提取关键参数表
    - 使用 OCR 识别扫描版图纸中的文字

    提取的设计参数应用到 plan.md:
    - 谐振频率选择: 100-200kHz (参考 AN-4151)
    - 变压器设计方法: 按应用笔记第3.2节
```

### 在 /elecspeckit.tasks 中使用

**场景**: BOM 表格提取和元器件清单生成

```
用户: 从参考设计PDF提取BOM表

AI: [内部调用] pdf Skill:
    使用 pdfplumber.extract_tables():
    - 提取元器件清单表格
    - 转换为 Excel 格式
    - 生成可编辑的 BOM 清单

    输出: BOM_from_Reference_Design.xlsx
```

### 典型使用流程

1. **数据手册解析**: 提取电气参数表格
2. **应用笔记提取**: 提取设计公式和参考电路
3. **标准文档查询**: 从PDF标准中提取合规要求
4. **BOM 生成**: 从参考设计提取元器件清单
5. **OCR 识别**: 从扫描PDF提取文本和表格

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md |

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md
