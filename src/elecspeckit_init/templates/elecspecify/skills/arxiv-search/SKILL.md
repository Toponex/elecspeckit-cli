---
name: "arxiv-search"
description: "搜索学术论文和研究文献"
requires_api: false
---

# arxiv-search Skill

## 概述

arxiv-search 是一个学术论文搜索工具，通过 arXiv API 搜索电子工程、计算机科学、物理学等领域的最新研究论文。适用于：

- 查找最新的硬件设计方法论
- 研究新型拓扑结构和控制算法
- 验证设计理念的学术基础
- 查找参考实现和仿真模型

## 依赖

### Python 库

```bash
pip install arxiv
```

**说明**: 需要 `arxiv` Python 库访问 arXiv API。

## 使用

### 基本用法

```
请使用 arxiv-search 搜索关于 LLC 谐振转换器的最新论文
```

### 搜索特定主题

```
使用 arxiv-search 查找 2023-2024 年发表的关于无线充电的论文
```

### 搜索特定作者

```
在 arXiv 上搜索作者 "Zhang Wei" 关于电源管理的论文
```

## 功能特性

1. **多领域搜索**: 支持搜索电子工程、计算机科学、物理学等领域
2. **时间过滤**: 可指定论文发表时间范围
3. **关键词匹配**: 支持标题、摘要、关键词搜索
4. **作者搜索**: 可按作者姓名搜索
5. **结果排序**: 按相关性或发表时间排序

## ElecSpeckit 集成指南

### 在 /elecspeckit.plan 中使用

**场景**: Phase 0 研究阶段，查找学术文献验证设计方案

```
用户: /elecspeckit.plan

AI: Phase 0 研究 - LLC 拓扑选择

    [内部调用] 使用 arxiv-search 搜索:
    "LLC resonant converter efficiency optimization"

    找到相关论文:
    1. "A Novel Control Strategy for LLC Resonant Converter" (2023)
    2. "Efficiency Optimization in LLC Converters..." (2024)

    基于论文研究，推荐使用频率调制控制策略...
```

### 在 /elecspeckit.specify 中使用

**场景**: 编写规格时，引用学术研究支持设计选择

```
用户: /elecspeckit.specify 无线充电模块

AI: [内部调用] 使用 arxiv-search 查找:
    "wireless power transfer resonant coupling"

    引用论文验证:
    - 谐振频率选择依据
    - 传输效率理论上限
    - EMI 抑制方法
```

### 典型使用流程

1. **技术调研阶段**: 搜索最新研究方向和技术趋势
2. **方案验证阶段**: 查找理论依据和仿真模型
3. **性能优化阶段**: 搜索优化算法和控制策略
4. **文献综述阶段**: 整理相关研究文献

## 最佳实践

### ✅ 推荐做法

- 使用英文关键词搜索（arXiv 主要收录英文论文）
- 组合多个关键词提高精确度
- 指定时间范围获取最新研究
- 关注高引用量的经典论文

### ❌ 避免做法

- 不要使用过于宽泛的关键词
- 不要忽略论文发表时间（可能过时）
- 不要只看标题，建议阅读摘要

## 示例

### 示例 1: 搜索最新论文

```
用户: 使用 arxiv-search 搜索 2024 年关于 GaN 功率器件的论文

AI: [执行 Python 脚本]
    python arxiv_search.py --query "GaN power device" --start-date 2024-01-01

    搜索结果 (前 5 篇):

    1. "High-Efficiency GaN-Based DC-DC Converter Design" (2024-03)
       摘要: 提出了一种基于 GaN 器件的高效 DC-DC 转换器...
       链接: https://arxiv.org/abs/2403.12345

    2. "Thermal Management in GaN Power Modules" (2024-02)
       摘要: 研究了 GaN 功率模块的热管理策略...
       链接: https://arxiv.org/abs/2402.67890

    ...
```

### 示例 2: 搜索特定主题

```
用户: 查找关于数字电源控制的论文

AI: [执行搜索]
    查询: "digital power control FPGA microcontroller"

    相关论文:
    - "FPGA-Based Digital Control for Switching Regulators"
    - "Microcontroller Implementation of Advanced PWM..."

    关键发现:
    - FPGA 实现可达到纳秒级控制精度
    - 微控制器方案成本更低但响应稍慢
    ...
```

### 示例 3: 验证设计方案

```
用户: 我想使用 LLC + PFC 级联拓扑，有学术依据吗？

AI: [搜索验证]
    arxiv-search: "LLC PFC cascaded topology"

    找到支持文献:
    1. "Two-Stage AC-DC Converter with PFC and LLC..."
       结论: 级联方案可实现 >95% 效率

    2. "Optimal Design of PFC-LLC Cascaded Converter"
       建议: PFC 输出电压 380-400V，LLC 谐振频率 100-200kHz

    设计方案有充分学术支持 ✓
```

## Python 脚本实现

### 文件: arxiv_search.py

```python
#!/usr/bin/env python3
"""
arXiv 论文搜索脚本

使用 arXiv API 搜索学术论文
"""

import argparse
import arxiv
from datetime import datetime


def search_arxiv(query, max_results=10, start_date=None, end_date=None):
    """
    搜索 arXiv 论文

    Args:
        query: 搜索关键词
        max_results: 最大结果数量
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        论文列表
    """
    # 构建搜索查询
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    results = []
    for paper in search.results():
        # 时间过滤
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            if paper.published.replace(tzinfo=None) < start:
                continue

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if paper.published.replace(tzinfo=None) > end:
                continue

        results.append(
            {
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "published": paper.published.strftime("%Y-%m-%d"),
                "summary": paper.summary[:300] + "..." if len(paper.summary) > 300 else paper.summary,
                "url": paper.entry_id,
                "pdf_url": paper.pdf_url,
            }
        )

    return results


def main():
    parser = argparse.ArgumentParser(description="搜索 arXiv 论文")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--max-results", type=int, default=10, help="最大结果数量")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    results = search_arxiv(
        query=args.query,
        max_results=args.max_results,
        start_date=args.start_date,
        end_date=args.end_date,
    )

    if args.json:
        import json

        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for i, paper in enumerate(results, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   作者: {', '.join(paper['authors'][:3])}")
            if len(paper['authors']) > 3:
                print(f"         等 {len(paper['authors'])} 人")
            print(f"   发表: {paper['published']}")
            print(f"   摘要: {paper['summary']}")
            print(f"   链接: {paper['url']}")
            print(f"   PDF:  {paper['pdf_url']}")


if __name__ == "__main__":
    main()
```

## 故障排除

### 问题: arxiv 库未安装

**错误信息**: `ModuleNotFoundError: No module named 'arxiv'`

**解决方案**:
```bash
pip install arxiv
```

### 问题: 搜索结果为空

**解决方案**:
1. 尝试使用更宽泛的关键词
2. 检查时间范围是否过于严格
3. 使用英文关键词（arXiv 主要收录英文论文）

### 问题: API 访问超时

**解决方案**:
1. 检查网络连接
2. 减少 `max_results` 数量
3. 稍后重试（可能是 arXiv 服务器负载高）

## 相关 Skills

- **openalex-database**: 搜索更广泛的学术数据库
- **citation-management**: 管理论文引用
- **web-research**: 在线搜索补充资料

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
