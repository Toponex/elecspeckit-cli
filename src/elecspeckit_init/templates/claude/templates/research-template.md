---
description: "硬件架构研究与选型决策模板"
---

# Research: Phase 0 架构选型研究

本文档用于记录硬件功能开发中 Phase 0 识别的架构级研究问题，跟踪研究过程、候选方案对比和最终决策。

## 如何使用本模板

1. **识别研究问题**: 在规格分析和初步架构规划时，列出需要深入研究的技术选型问题（如拓扑选择、器件选型、层叠结构等）
2. **推荐信息源**: 基于 `.elecspecify/memory/knowledge-sources.json` 为每个问题推荐相关的参考设计、标准文档、公司知识库或 web 搜索
3. **执行查询**: 使用 `.elecspecify/scripts/win/python/` 下的查询脚本（如 `query_reference_design.py`、`query_metaso.py`、`query_standards.py`）获取技术资料
4. **记录候选方案**: 将查询结果提取为候选方案，说明各方案的技术特性、优缺点和成本影响
5. **补充决策**: 由工程师在 Decision 和 Rationale 字段中填写最终选择和决策依据

## Phase 0 研究问题列表

---

### 研究问题 1: [待补充问题标题]

**Question**
<!-- 示例: "AHB vs LLC拓扑选择(65W PD充电头)" -->
[待补充需要研究的架构级问题]

**Suggested sources**
<!-- 从 knowledge-sources.json 推荐的信息源 -->
<!-- 示例: -->
<!-- - **reference_designs**: TI PMP22682(65W AHB参考), ON Semi NCP13992参考设计(65W LLC参考) -->
<!-- - **web**: Metaso学术搜索 -->
<!-- - **standards**: IEC 62368-1 -->
[待补充推荐的信息源，包括 reference_designs、company_kb、web、standards 等类别]

**Research steps**
<!-- 具体查询步骤及命令 -->
<!-- 示例: -->
<!-- 1. 查询TI PMP22682参考设计了解AHB拓扑特性: -->
<!--    ```bash -->
<!--    python .elecspecify/scripts/win/python/query_reference_design.py "PMP22682 65W AHB topology characteristics" -->
<!--    ``` -->
<!-- 2. 查询Metaso学术搜索拓扑对比: -->
<!--    ```bash -->
<!--    python .elecspecify/scripts/win/python/query_metaso.py "AHB LLC 65W 拓扑对比 效率 成本" -->
<!--    ``` -->
<!-- 3. 查询IEC标准: -->
<!--    ```bash -->
<!--    python .elecspecify/scripts/win/python/query_standards.py "IEC 62368-1 拓扑安全要求" -->
<!--    ``` -->
[待补充具体查询步骤，包括命令行调用]

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
