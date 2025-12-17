# 实施计划: [硬件特性]

**分支**: `[###-feature-name]` | **日期**: [DATE] | **规范**: `/specs/[###-feature-name]/spec.md`
**输入**: 功能规范来自 `specs/[###-feature-name]/spec.md`

**注意**: 此模板由 `/elecspeckit.plan` 命令参考填充，用于指导硬件特性的架构设计与实施计划。

<!--
ElecSpecKit Skills 使用提示:
在编写实施计划和进行架构研究时，可以使用以下 Skills：

**研究与分析类**:
- web-research: 技术方案调研
- arxiv-search: 学术论文搜索
- openalex-database: 学术数据库查询
- docs-seeker: 查找技术文档和数据手册
- citation-management: 管理参考文献

**元器件选型类**:
- mouser-component-search: 搜索元器件库存和价格（需要 API 密钥）

**架构设计类**:
- architecture-diagrams: 生成系统架构图
- mermaid-tools: 创建电路框图、时序图
- embedded-systems: 嵌入式系统设计建议

**领域分析类** (v0.2.1 占位符):
- circuit-commutation-analysis: 电路换流拓扑分析
- thermal-simulation: 热设计仿真
- emc-analysis: EMC/EMI 分析

提示：在 research.md 中记录使用 Skills 的调研过程和结果
-->

## 摘要

[从功能规范中提取：主要硬件需求 + 当前考虑的技术路径（例如板层、接口方案、关键器件选型方向）]  

## 技术上下文

<!--
  操作要求: 用本硬件特性的技术细节替换此部分内容。
-->

**板卡类型/形态**: [例如，4 层嵌入式核心板 / 插卡 / 背板 / 模块等]  
**关键接口**: [例如，Ethernet, USB, UART, SPI, GPIO 等]  
**主要器件族**: [例如，MCU/SoC 型号、PHY、PMIC、存储器等]  
**供电与电源策略**: [例如，多路电源、上电顺序、冗余等]  
**散热与机械约束**: [例如，功耗预算、散热方式、尺寸限制]  
**目标环境**: [例如，工业级温度范围、电磁环境、振动/冲击等级]  
**本地化要求**: 默认支持中文规范与文档，关键技术术语使用英文。  

## 宪法检查

*门禁：研究阶段前必须通过。设计阶段后重新检查。*

基于项目级 ElecSpeckit 宪法（`.elecspecify/memory/constitution.md`），说明本特性在以下方面的遵循情况：  

**库优先架构**：  
- 重用已有板级库/模块的设计，还是引入新器件/新库？  

**CLI优先接口**：  
- 与 Elecspeckit CLI / `/elecspeckit.*` 模板的集成方式（例如哪些步骤通过命令驱动完成）。  

**测试驱动开发**：  
- 对本特性的关键路径（如电源、接口信号）的验证策略和必备测试。  

**可观察性与日志**：  
- 是否需要在板卡上暴露额外测试点/调试接口，以满足可观察性要求。  

**中文本地化支持**：  
- 是否需要为本特性生成面向不同角色的中文文档（PM/测试/FA/客户等）。  

**门禁状态**: [ ] 通过 / [ ] 失败 - 如有偏离必须在“复杂性跟踪”中说明原因。  

## 命令行为设计（/elecspeckit.*）

> 说明本特性相关的 `/elecspeckit.specify` / `/elecspeckit.plan` / `/elecspeckit.tasks` / `/elecspeckit.docs` / Clarify / Checklist / Analyze 在此特性中的角色和约束。  

- `/elecspeckit.specify`：如何从自然语言硬件需求生成/更新本特性的 `spec.md`。  
- `/elecspeckit.plan`：如何基于 `spec.md` 生成 `plan.md`、`research.md`、`data-model.md`，以及本节的具体使用方式。  
- `/elecspeckit.tasks`：如何将架构拆解为可执行任务，对应 `tasks.md` 的结构。  
- `/elecspeckit.docs`：如何基于 `spec/plan/tasks` 生成多角色视图和 ProductDocumentation 草稿。  
- Clarify / Checklist / Analyze：作为质量和一致性辅助的角色。  

## 阶段规划

> 按阶段（Phase 0/1/2/...）规划从架构研究到实现与文档的过程。以下为示例结构：  

### Phase 0：研究与可行性分析

- 研究不同器件/接口方案的优缺点和约束（记录在 `research.md` 中）。  
- 初步整理关键实体与关系（在 `data-model.md` 中记录）。  

### Phase 1：架构与接口定义

- 确定板层、接口拓扑、关键器件及冗余策略。  
- 更新 `plan.md` 中的 Architecture 和 Tradeoffs 小节。  

### Phase 2：任务分解与验证规划

- 使用 `/elecspeckit.tasks` 生成/更新 `tasks.md`，按用户故事拆分实现与验证任务。  

### Phase 3：文档与交付

- 使用 `/elecspeckit.docs` 生成多角色文档和 ProductDocumentation 草稿。  

## 项目结构（针对本特性）

```text
specs/[###-feature-name]/
├── spec.md              # 功能规格（由 /elecspeckit.specify 维护）
├── plan.md              # 实施计划（本文件）
├── research.md          # 研究与决策记录
├── data-model.md        # 数据/实体模型
├── quickstart.md        # 如何搭建/验证本特性的快速指南
├── tasks.md             # 任务列表（由 /elecspeckit.tasks 维护）
├── docs/                # 多角色视图与对外文档草稿（由 /elecspeckit.docs 维护）
└── checklists/          # 规格与计划的质量检查清单
```

## 复杂性跟踪

> **仅在宪法检查有必须证明的偏离或架构决策较复杂时填写。**  

| 违规/偏离 | 为何需要 | 拒绝的更简单替代方案原因 |
|-----------|---------|--------------------------|
|           |         |                          |

