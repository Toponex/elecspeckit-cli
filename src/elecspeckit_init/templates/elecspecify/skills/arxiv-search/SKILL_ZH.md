---
name: arxiv-search
description: 搜索 arXiv 预印本库，涵盖电子工程、嵌入式系统、计算机科学、物理学、数学及相关领域的论文。
---
# arXiv Search Skill (arXiv 搜索技能)

本技能提供对 arXiv 的访问权限，这是一个免费的学术文章分发服务和开放获取存档库，特别涵盖电子工程、嵌入式系统、硬件设计、信号处理、物联网、射频电路、AI加速器等专业领域，同时包括计算机科学、物理学和数学等相关学科。

## 何时使用本技能

在以下情况时使用本技能:

- 查找电子工程、嵌入式系统、硬件设计等领域的最新研究论文和预印本
- 搜索特定芯片（如 STM32、ESP32）应用、驱动开发的最新进展
- 获取电路设计、信号完整性、电源管理、物联网协议等方面的前沿研究
- 跟进嵌入式人工智能、TinyML、边缘计算等交叉领域的研究动态
- 查找硬件描述语言（如 VHDL、Verilog）、电子设计自动化（EDA）工具相关研究

## 使用方法

本技能提供一个 Python 脚本，可搜索 arXiv 并返回格式化结果，其实现基于 arxivPython 包，能够返回论文的标题、摘要等信息。

### 基本用法

**注意:** 始终使用从您的技能目录的绝对路径（如上方的系统提示中所示）。

如果从虚拟环境运行这个技能:

```bash
.venv/bin/python [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

或使用系统 Python:

```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

将 [YOUR_SKILLS_DIR]替换为系统提示中的绝对技能目录路径 (e.g., `~/.deepagents/agent/skills` 或完整的绝对路径)。

**参数:**

- `query` (必需): 搜索查询字符串 (e.g., "neural networks protein structure", "single cell RNA-seq")
- `--max-papers` (可选): 要检索的最大论文数（默认：10）

### 示例

搜索嵌入式AI相关论文:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "TinyML embedded systems" --max-papers 5
```

搜索硬件安全相关研究:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "hardware security trust verification"
```

搜索射频电路设计新方法:

```bash
.venv/bin/python ~/.elecspeckit/skills/arxiv-search/arxiv_search.py "RF circuit design machine learning"
```

## 输出格式

脚本返回格式化结果，包含:

- **标题**: 论文标题
- **摘要**: 摘要文本

每个论文之间用空行分隔以提高可读性。

## 功能特点

- **相关性排序**: 结果按查询相关性排序
- **快速检索**: 直接 API 访问，无需认证
- **简单接口**: 清晰、易于解析的输出
- **无需 API 密钥**: 免费访问 arXiv 数据库

## 依赖项

本技能需要 `arxiv` Python 包。脚本会检测是否缺少该包并显示错误。

**如果看到 "Error: arxiv package not installed":**

如果从虚拟环境运行技能（推荐），使用虚拟环境的 Python:

```bash
.venv/bin/python -m pip install arxiv
```

或进行系统级安装:

```bash
python3 -m pip install arxiv
```

该包默认不包含在 elecspeckit-cli 中，因为它是技能特定的。首次使用本技能时按需安装。

## 与 ElecSpeckit CLI 协同使用

您可以将在此 Skill 中发现的最新算法或理论，与 CLI 中的其他技能结合进行实践。

## 注意事项

- arXiv 中与电子工程和嵌入式系统高度相关的分类包括:
  - cs.AR (硬件架构)
  - cs.ET (新兴技术，包含纳米电子、量子计算等)
  - eess.SP (信号处理)
  - eess.AS (音频与语音处理，含嵌入式DSP内容)
  - physics.app-ph (应用物理学)
- 论文是预印本，可能未经同行评审
- 结果包括最近上传的论文和较旧的论文
- 最适合电子工程、嵌入式系统、硬件设计领域的理论研究和算法验证
