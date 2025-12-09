---
description: Run ElecSpeckit checklist workflow to generate requirement-quality checklists for the current hardware feature.
handoffs:
  - label: Generate Docs
    agent: elecspeckit.docs
    prompt: Use updated checklists as quality gate before docs
    send: true
---

## Command: `/elecspeckit.checklist`

**Goal**  
为当前 ElecSpeckit 硬件特性的文档（尤其是 `spec.md` 和 `plan.md`）生成或更新“需求质量检查清单”，把需求当成“用自然语言写的代码”，用 checklist 作为“Unit Tests for Requirements”，而不是测试实现行为。

**适用范围**
- 特性目录：当前 ElecSpeckit 特性所在的目录，例如 `specs/<feature-id>/`；
- 主要输入：`FEATURE_DIR/tasks.md`（必须），可参考 `spec.md`、`plan.md` 等辅助文档；
- 目标文件夹：`FEATURE_DIR/checklists/`；
- 每次命令运行可以创建或追加一个 checklist 文件（如 `requirements.md`、`ux.md`、`api.md`、`template-boundary.md` 等），不强制覆盖已有清单；
- **重要**: 本命令仅生成 checklist 文件，不修改 `spec.md`、`plan.md`、`tasks.md` 或 `docs/` 等实现文档。

**Execution Steps（给 AI 助手执行用）**

1. 在目标硬件项目根目录工作，与用户一起确认本次要处理的 `FEATURE_DIR`（例如 `specs/<feature-id>/`），并据此构造：
   - `FEATURE_TASKS = FEATURE_DIR/tasks.md`（主要输入，必须）；
   - `FEATURE_SPEC = FEATURE_DIR/spec.md`（可选参考）；
   - `FEATURE_PLAN = FEATURE_DIR/plan.md`（可选参考）。
2. 读取 ElecSpeckit 特性的上下文：
   - 必须：`FEATURE_TASKS`；
   - 可选参考：`FEATURE_SPEC`、`FEATURE_PLAN`、`data-model.md`、`contracts/`、`research.md`、`quickstart.md`。  
3. 确认本次 checklist 的主题（例如“requirements quality”、“API requirements”、“性能要求”、“模板边界”等）：  
   - 若用户未说明，可从当前命令或最近一次 `/elecspeckit.analyze` 的结果中推断；  
   - 不同主题可对应不同文件名，例如：`requirements.md`、`api.md`、`performance.md`、`template-boundary.md`。  
4. 在 `FEATURE_DIR/checklists/` 下创建或追加 checklist 文件：  
   - 命名规则：`<domain>.md`（如 `requirements.md`）。  
5. 按以下维度组织 checklist 条目（每条使用 `- [ ] CHK### ...` 格式，编号从 CHK001 开始递增）：  
   - Requirements Completeness（需求完整性）  
   - Requirements Clarity（需求清晰度）  
   - Requirements Consistency（一致性）  
   - Acceptance Criteria Quality（验收标准质量）  
   - Scenario Coverage（场景覆盖：主流程、异常、恢复等）  
   - Edge Case Coverage（边界情况）  
   - Non-Functional Requirements（性能、安全、可用性、本地化、可观察性等）  
   - Dependencies & Assumptions（依赖与假设）  
   - Ambiguities & Conflicts（模糊点与冲突）  
6. 每条 checklist 条目应：  
   - 用问题形式表述关注点，例如：  
     - “功能 block 列表是否覆盖了所有用户故事中的关键场景？[Completeness, Spec §US2]”  
     - “`tradeoff_factors` 是否在规格与 plan 中以可度量方式呈现？[Clarity, Plan §ArchitecturePlan]”  
   - 引用来源（`[Spec §X]`、`[Plan §Y]`）或标记 `[Gap]` / `[Ambiguity]` / `[Assumption]`；  
   - 避免测试实现行为（不写“验证 CLI 返回 0 exit code”之类）。  
7. 确保至少 80% 的条目有 traceability：  
   - 即引用 `Spec`/`Plan`/`Data-Model` 中的章节或使用 `FR-xxx`、`SC-xxx` 等编号；  
   - 对于纯“Gap”条目，也应指出是哪个方面的潜在缺失（例如“恢复场景”或“日志结构与指标映射”）。  
8. 保存 checklist 文件后，向用户返回：  
   - 新建或更新的 checklist 文件路径（如 `FEATURE_DIR/checklists/requirements.md`）；  
   - 本次新增条目数量；  
   - 简要说明本 checklist 覆盖的质量维度（例如“覆盖硬件板卡的性能 NFR 与模板边界要求”）。  

**Notes**  
- checklist 是“对规范写得好不好”的单元测试，而不是实现是否正确；  
- 可以结合 `/elecspeckit.clarify` 和 `/elecspeckit.analyze` 的结果，针对 `[CLARIFY]` 或分析报告中标记的风险点补充专门条目，确保澄清问题与风险有明确处理位置；  
- 模板本身不绑定具体的检查实现，由项目自行选择工具和脚本。  
