---
description: "硬件架构研究与选型决策模板"
---

# Research: Phase 0 架构选型研究

本文档用于记录硬件功能开发中 Phase 0 识别的架构级研究问题，跟踪研究过程、候选方案对比和最终决策。

## 如何使用本模板

1. **识别研究问题**: 在规格分析和初步架构规划时，列出需要深入研究的技术选型问题（如拓扑选择、器件选型、层叠结构等）
2. **推荐信息源**: 根据问题性质选择合适的 ElecSpecKit Skills 进行研究
3. **执行查询**: 使用自然语言请求相关 Skills 获取技术资料（如"使用 web-research 搜索 AHB 拓扑特性"）
4. **记录候选方案**: 将查询结果提取为候选方案，说明各方案的技术特性、优缺点和成本影响
5. **补充决策**: 由工程师在 Decision 和 Rationale 字段中填写最终选择和决策依据

## 可用的研究 Skills

**信息检索类**:
- `docs-seeker`: 搜索技术文档、数据手册
- `arxiv-search`: 搜索学术论文
- `web-research`: 网络技术调研
- `openalex-database`: 学术数据库查询

**元器件采购类**:
- `mouser-component-search`: Mouser 元器件搜索（需要 API 密钥）

**文献管理类**:
- `citation-management`: 管理研究参考文献

**领域分析类** (v0.2.1 占位符):
- `circuit-commutation-analysis`: 电路拓扑分析
- `thermal-simulation`: 热仿真
- `emc-analysis`: EMC/EMI 分析

## Phase 0 研究问题列表

---

### 研究问题 1: [待补充问题标题]

**Question**
<!-- 示例: "AHB vs LLC拓扑选择(65W PD充电头)" -->
[待补充需要研究的架构级问题]

**Suggested sources**
<!-- 推荐使用的 ElecSpecKit Skills -->
<!-- 示例: -->
<!-- - **web-research**: 搜索 AHB vs LLC 拓扑对比 -->
<!-- - **arxiv-search**: 搜索相关学术论文 -->
<!-- - **mouser-component-search**: 查询相关元器件 -->
[待补充推荐的 Skills，根据问题性质选择合适的信息检索工具]

**Research steps**
<!-- 具体查询步骤，使用自然语言请求 Skills -->
<!-- 示例: -->
<!-- 1. 使用 web-research 搜索 AHB 拓扑特性: -->
<!--    "请使用 web-research 搜索 '65W AHB topology characteristics efficiency cost'" -->
<!-- 2. 使用 arxiv-search 查找学术论文: -->
<!--    "请使用 arxiv-search 搜索 'LLC resonant converter 65W PD charger'" -->
<!-- 3. 使用 docs-seeker 查找参考设计文档: -->
<!--    "请使用 docs-seeker 搜索 'TI PMP22682 reference design'" -->
[待补充具体查询步骤，描述如何使用 Skills]

**Candidates**
<!-- 执行Research steps后从查询结果中提取的候选方案 -->
<!-- 示例: -->
<!-- - **Candidate A: AHB拓扑** (Source: TI PMP22682参考设计, queried via reference_designs) -->
<!--   - 满载效率: 94-95% -->
<!--   - 成本: 较低 -->
<!--   - 优势: 适合宽输出范围5V-20V, 控制复杂度中等, 母线电压利用率高 -->
<!--   - 劣势: 轻载效率需优化 -->
<!-- -->
<!-- - **Candidate B: LLC拓扑** (Source: Metaso学术搜索 '65W LLC拓扑特性分析') -->
<!--   - 满载效率: 95-96% -->
<!--   - 成本: 高10-15% -->
<!--   - 优势: 轻载效率优秀, 零电压开关范围宽 -->
<!--   - 劣势: 输出范围调节受变压器匝比限制, 变压器设计复杂 -->
[待补充候选方案及其技术特性对比]

**Decision**
[待工程师补充最终选择，例如: "选择 Candidate A: AHB拓扑"]

**Rationale**
[待工程师补充决策依据，例如: "项目需要宽输出范围5-20V调节，AHB拓扑在此应用场景下成本和控制复杂度较优，满载效率94-95%满足DoE Level VI要求。轻载效率通过burst mode优化可达标。"]

---

### 研究问题 2: [待补充问题标题]

**Question**
[待补充需要研究的架构级问题]

**Suggested sources**
[待补充推荐的信息源]

**Research steps**
[待补充具体查询步骤]

**Candidates**
[待补充候选方案及其技术特性对比]

**Decision**
[待工程师补充最终选择]

**Rationale**
[待工程师补充决策依据]

---

### 研究问题 3: [待补充问题标题]

**Question**
[待补充需要研究的架构级问题]

**Suggested sources**
[待补充推荐的信息源]

**Research steps**
[待补充具体查询步骤]

**Candidates**
[待补充候选方案及其技术特性对比]

**Decision**
[待工程师补充最终选择]

**Rationale**
[待工程师补充决策依据]

---

## 模板使用说明

1. **复制问题块**: 根据实际需要，复制上述研究问题块（从 `### 研究问题 X` 到 `---`）添加更多研究问题
2. **保持结构**: 确保每个问题包含完整的 6 个字段（Question, Suggested sources, Research steps, Candidates, Decision, Rationale）
3. **引用 knowledge-sources.json**: Suggested sources 字段中的信息源应来自 `.elecspecify/memory/knowledge-sources.json` 配置
4. **标注来源**: Candidates 字段中应标注每个候选方案的信息来源（如 "Source: TI PMP22682参考设计, queried via reference_designs"）
5. **工程师决策**: Decision 和 Rationale 字段由工程师在研究完成后补充，不应由 AI 自动填写

## 与其他文档的关系

- **plan.md**: 在 Key Decisions 章节引用本文档中的决策记录，说明架构选择的理由
- **knowledge-sources.json**: 本文档的 Suggested sources 和 Research steps 依赖该配置文件
- **spec.md**: 研究问题来源于规格中的技术约束和需求
