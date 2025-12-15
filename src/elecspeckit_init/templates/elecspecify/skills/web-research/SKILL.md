---
name: "web-research"
description: "执行结构化网络研究任务"
requires_api: false
---

# web-research Skill

## 概述

web-research 是一个结构化网络研究工具，帮助执行系统化的在线信息收集任务。适用于：

- 技术方案调研
- 市场信息收集
- 竞品分析
- 最新技术趋势追踪

## 依赖

**无需额外依赖**。使用 Claude Code 内置的 WebSearch 功能。

## 使用

### 基本用法

```
使用 web-research 调研LLC谐振转换器的最新技术进展
```

### 结构化研究

```
执行web-research: GaN功率器件市场分析
- 主要厂商
- 价格趋势
- 技术参数对比
```

## 功能特性

1. **结构化输出**: 按类别组织研究结果
2. **多源验证**: 交叉验证信息准确性
3. **时效性**: 优先搜索最新信息
4. **可追溯性**: 提供信息来源链接

## ElecSpeckit 集成指南

### 在 /elecspeckit.plan 中使用

**场景**: Phase 0 研究 - 技术方案调研

```
用户: /elecspeckit.plan

AI: Phase 0 研究 - 电源模块方案选择

    [内部调用] web-research:
    - LLC vs Flyback 效率对比
    - 主流厂商参考设计
    - 成本分析

    研究结论: LLC方案效率更高(>92%)，适合高功率应用...
```

### 在 /elecspeckit.specify 中使用

**场景**: 编写规格时验证技术可行性

```
用户: /elecspeckit.specify 无线充电模块

AI: [内部调用] web-research:
    查询当前无线充电标准(Qi, PMA, A4WP)
    调研主流方案参数范围

    基于调研结果编写规格...
```

### 典型使用流程

1. **方案调研**: 技术路线选择
2. **器件调研**: 可用器件和供应商
3. **标准查询**: 行业标准和认证要求
4. **竞品分析**: 同类产品对比

## 最佳实践

### ✅ 推荐做法

- 明确研究目标和范围
- 使用结构化的问题列表
- 记录信息来源和时间
- 交叉验证关键数据

### ❌ 避免做法

- 不验证信息来源可靠性
- 使用过时的信息
- 忽略地域性差异

## 示例

### 示例 1: 技术调研

```
用户: 使用 web-research 调研 2024 年 GaN 器件的最新进展

AI: [执行结构化研究]

    ## GaN 功率器件 2024 年进展

    ### 主要厂商
    - TI: 发布650V GaN产品线
    - Infineon: 推出高频开关GaN模块
    - GaN Systems: 扩大200V-650V产品覆盖

    ### 技术参数
    - 开关频率: 可达MHz级
    - 效率提升: 比Si MOSFET高3-5%
    - 热阻: RθJC 降低20-30%

    ### 价格趋势
    - 2024年平均降价15%
    - 预计2025年与Si价格接近

    来源:
    [1] TI 官网产品页
    [2] Power Electronics News (2024-02)
    [3] Yole Development Market Report
```

## 相关 Skills

- **docs-seeker**: 搜索本地文档
- **arxiv-search**: 搜索学术论文
- **perplexity-search**: 高级 AI 搜索

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
