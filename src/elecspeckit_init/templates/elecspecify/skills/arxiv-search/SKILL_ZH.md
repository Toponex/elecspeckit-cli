---
name: arxiv-search
description: 搜索 arXiv 预印本库，涵盖物理学、数学、计算机科学、定量生物学及相关领域的论文。
---
# arXiv Search Skill (arXiv 搜索技能)

本技能提供对 arXiv 的访问权限，这是一个免费的学术文章分发服务和开放获取存档库，涵盖物理学、数学、计算机科学、定量生物学、定量金融学、统计学、电气工程、系统科学和经济学。

## 何时使用本技能

在以下情况时使用本技能:

- 查找期刊出版前的预印本和最新研究论文
- 搜索计算生物学、生物信息学或系统生物学领域的论文
- 获取与生物学相关的数学或统计学方法论文
- 查找应用于生物学问题的机器学习论文
- 获取可能尚未收录在 PubMed 中的最新研究

## 使用方法

本技能提供一个 Python 脚本，可搜索 arXiv 并返回格式化结果。

### 基本用法

**注意:** 始终使用从您的技能目录的绝对路径（如上方的系统提示中所示）。

如果从虚拟环境运行 deepagents:

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

搜索机器学习论文:

```bash
.venv/bin/python ~/.deepagents/agent/skills/arxiv-search/arxiv_search.py "deep learning drug discovery" --max-papers 5
```

搜索计算生物学论文:

```bash
.venv/bin/python ~/.deepagents/agent/skills/arxiv-search/arxiv_search.py "protein folding prediction"
```

搜索生物信息学方法论文:

```bash
.venv/bin/python ~/.deepagents/agent/skills/arxiv-search/arxiv_search.py "genome assembly algorithms"
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

如果从虚拟环境运行 deepagents（推荐），使用虚拟环境的 Python:

```bash
.venv/bin/python -m pip install arxiv
```

或进行系统级安装:

```bash
python3 -m pip install arxiv
```

该包默认不包含在 deepagents 中，因为它是技能特定的。首次使用本技能时按需安装。

## 注意事项

- arXiv 在以下领域特别强大:
  - 计算机科学 (cs.LG, cs.AI, cs.CV)
  - 定量生物学 (q-bio)
  - 统计学 (stat.ML)
  - 物理学和数学
- 论文是预印本，可能未经同行评审
- 结果包括最近上传的论文和较旧的论文
- 最适合生物学领域的计算/理论研究
