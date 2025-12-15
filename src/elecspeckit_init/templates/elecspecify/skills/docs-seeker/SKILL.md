---
name: "docs-seeker"
description: "搜索和定位项目文档、技术规格书、数据手册"
requires_api: false
---

# docs-seeker Skill

## 概述

docs-seeker 是一个文档搜索和定位工具，专为硬件/电子项目设计。它可以帮助你快速找到：

- 项目内部文档（规格书、设计文档、测试报告）
- 芯片数据手册（Datasheet）
- 技术参考手册（Reference Manual）
- 应用笔记（Application Note）
- 行业标准文档（IPC、ISO、IEC 等）

## 依赖

**无需额外依赖**。此 Skill 使用 Claude Code 内置的文件搜索功能。

## 使用

### 基本用法

在 Claude Code 对话中直接调用：

```
请使用 docs-seeker 查找 STM32F407 的数据手册
```

### 搜索项目文档

```
使用 docs-seeker 搜索项目中的 AC-DC 电源模块设计文档
```

### 搜索特定章节

```
在 ESP32 技术参考手册中查找 I2C 接口配置章节
```

## 功能特性

1. **智能路径推断**: 根据文件类型自动推断可能的存储位置
   - 数据手册: `docs/datasheets/`, `references/datasheets/`
   - 应用笔记: `docs/app-notes/`, `references/`
   - 标准文档: `standards/`, `docs/standards/`

2. **模糊匹配**: 支持部分匹配和关键词搜索

3. **硬件适配**: 优先搜索硬件项目常见的文档类型

## ElecSpeckit 集成指南

### 在 /elecspeckit.plan 中使用

**场景**: Phase 0 研究阶段，查找参考设计和芯片数据手册

```
用户: /elecspeckit.plan

AI: 开始 Phase 0 研究...
    问题 1: AC-DC 拓扑选择 - Flyback vs LLC

    [内部调用] 使用 docs-seeker 搜索:
    - Flyback 应用笔记
    - LLC 参考设计文档
    - 相关芯片数据手册

    基于查找到的文档，分析各拓扑优缺点...
```

### 在 /elecspeckit.specify 中使用

**场景**: 编写规格时，引用标准文档和参考设计

```
用户: /elecspeckit.specify CAN 通信接口模块

AI: [内部调用] 使用 docs-seeker 查找:
    - ISO 11898 CAN 标准文档
    - CAN 收发器数据手册
    - CAN 接口设计应用笔记

    生成规格时引用这些文档...
```

### 典型使用流程

1. **架构设计阶段**: 查找参考设计、应用笔记
2. **器件选型阶段**: 查找芯片数据手册、选型指南
3. **合规验证阶段**: 查找行业标准文档
4. **设计评审阶段**: 查找设计检查清单

## 最佳实践

### ✅ 推荐做法

- 明确指定文档类型（数据手册、应用笔记、标准）
- 提供芯片型号或关键词（如 "STM32F407", "LLC 拓扑"）
- 指定具体章节或参数（如 "电气特性", "I2C 配置"）

### ❌ 避免做法

- 不要使用过于宽泛的关键词（如 "芯片", "设计"）
- 不要在没有文档的情况下假设内容

## 示例

### 示例 1: 查找数据手册

```
用户: 使用 docs-seeker 查找 TPS54620 数据手册中的电气特性参数

AI: [搜索 TPS54620 数据手册]
    找到: docs/datasheets/TPS54620.pdf

    提取电气特性章节:
    - 输入电压范围: 4.5V - 17V
    - 输出电流: 最大 6A
    - 开关频率: 200kHz - 2.5MHz
    ...
```

### 示例 2: 查找应用笔记

```
用户: 查找 LLC 谐振转换器的设计应用笔记

AI: [搜索 LLC 应用笔记]
    找到:
    - references/app-notes/AN-4151_LLC_Design_Guide.pdf
    - references/designs/LLC_Reference_Design.pdf

    关键设计要点:
    - 谐振频率选择
    - 变压器设计
    - 控制环路设计
    ...
```

### 示例 3: 查找标准文档

```
用户: 查找 IPC-2221 PCB 设计标准

AI: [搜索 IPC-2221 标准]
    找到: standards/IPC-2221B.pdf

    相关章节:
    - 走线宽度和间距
    - 过孔设计
    - 热管理
    ...
```

## 故障排除

### 问题: 找不到文档

**解决方案**:
1. 检查文档是否在项目目录中
2. 尝试使用更具体的关键词
3. 检查文档文件名是否包含关键词

### 问题: 找到的文档不是目标文档

**解决方案**:
1. 提供更完整的芯片型号或文档名称
2. 指定文档类型（数据手册 vs 应用笔记）
3. 提供文档发布者信息（如 "TI 的 LLC 应用笔记"）

## 技术细节

### 搜索策略

1. **路径优先级**:
   - `docs/datasheets/`
   - `references/`
   - `standards/`
   - 项目根目录

2. **文件类型优先级**:
   - `.pdf` (最高)
   - `.md`, `.txt`
   - `.doc`, `.docx`

3. **关键词匹配**:
   - 文件名匹配
   - 内容搜索（如果支持）

### 性能优化

- 使用 Claude Code 内置索引加速搜索
- 缓存常用文档路径
- 优先搜索最近访问的文档

## 相关 Skills

- **web-research**: 在线搜索文档和参考资料
- **arxiv-search**: 搜索学术论文
- **citation-management**: 管理文档引用

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
