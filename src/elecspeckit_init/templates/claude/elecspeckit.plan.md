---
description: Run ElecSpeckit planning workflow for the current hardware feature.
handoffs:
  - label: Generate Tasks
    agent: elecspeckit.tasks
    prompt: Generate implementation and verification tasks from this plan
    send: true
  - label: Generate Docs
    agent: elecspeckit.docs
    prompt: Generate multi-role docs based on this plan
    send: true
---

## Command: `/elecspeckit.plan`

**Goal**  
在基于 ElecSpeckit 的硬件项目中，根据当前特性的 `spec.md` 生成和维护 `plan.md`、`research.md`、`data-model.md`（以及必要时的 `quickstart.md` 等），为后续 `/elecspeckit.tasks` 和 `/elecspeckit.docs` 阶段提供清晰的技术规划。

**Execution Steps (for the AI assistant)**  
1. **Setup**（路径与上下文）  
   - 在目标硬件项目根目录工作，与用户确认当前特性所在的 `FEATURE_DIR`（例如 `specs/00X-shortname/`）；  
   - 运行 `.elecspecify/scripts/powershell/setup-plan.ps1 -Json`（如已按约定实现），从 JSON 中解析：  
     - `FEATURE_SPEC      = FEATURE_DIR/spec.md`；  
     - `IMPL_PLAN         = FEATURE_DIR/plan.md`；  
     - `FEATURE_RESEARCH  = FEATURE_DIR/research.md`；  
     - `FEATURE_DATA_MODEL = FEATURE_DIR/data-model.md`；  
     - `FEATURE_QUICKSTART = FEATURE_DIR/quickstart.md`（如需要）；  
     - 以及 `SPECS_DIR`、`BRANCH` 等元信息。  
   - 如脚本尚未实现，可由你在对话中与用户协作确认这些路径。  
2. **Initialize plan.md**（从模板创建或对齐结构）  
   - 若 `IMPL_PLAN` 不存在或几乎为空：  
     - 不要求用户手工创建文件，而是根据 `.elecspecify/templates/plan-template.md` 自动建立一个 `plan.md` 骨架，至少包含：  
       - 技术上下文（语言/依赖/目标平台等）；  
       - 宪法检查（Constitution Check）；  
       - 命令行为设计（本特性与 `/elecspeckit.*` 的关系）；  
       - 阶段规划（Phase 0/1/2/…）；  
       - 复杂性跟踪或等效治理小节。  
   - 若已有 `plan.md`：在保留工程师已有内容的前提下，对照模板补齐缺失的小节与标题（增量对齐结构）。  
3. **Phase 0：Outline & Research → research.md**  
   - 从 `FEATURE_SPEC` 与宪法中提取本特性的关键未知项与“需要澄清/研究”的点（技术上下文中的 `NEEDS CLARIFICATION` 等）；  
   - 对每个未知项生成一条研究任务，并在 `FEATURE_RESEARCH` 中用结构化形式记录：  
     - Decision: [选用的器件/拓扑/策略]  
     - Rationale: [为何选择它]  
     - Alternatives considered: [评估过的其他方案]  
   - 若 `FEATURE_RESEARCH` 尚不存在：创建 `research.md` 并填入上述结构；若已存在则更新/追加相关条目。  
4. **Phase 1：Design & Data Model → data-model.md / quickstart.md**  
   - 从 `FEATURE_SPEC` 中识别硬件实体和关系（板卡、接口、电源域、保护电路等），在 `FEATURE_DATA_MODEL` 中描述：  
     - 实体名称、关键属性；  
     - 实体之间的关系（信号链/供电/热耦合等）；  
     - 与需求中的验证点对应关系。  
   - 如项目需要快速上手文档，在 `FEATURE_QUICKSTART` 中起草：  
     - 如何在实验台/系统中连接本特性板卡；  
     - 基本上电/关机/安全操作步骤；  
     - 首轮验证建议（最小可行测试集合）。  
5. **Architecture & Tradeoffs → plan.md**  
   - 基于研究结论和数据模型，在 `IMPL_PLAN` 中补全“Architecture / Tradeoffs / 阶段规划”小节：  
     - 选择的拓扑/板层/接口方案；  
     - 安规/性能/成本/可制造性之间的权衡；  
     - 与项目宪法中关键原则的对齐情况。  
   - 使用“一问一答”的方式与用户交互，每次只问 1 个架构问题，并通过 A/B/C/D + E.其他（≤20 字）选项收敛决策。  
   - 每处理完约 5 个问题，询问用户是否继续；如用户选择停止，则结束本轮计划更新。  
6. **Ensure alignment with tasks/docs**  
   - 在已有 `tasks.md` 和 checklist / analyze / clarify 结果的基础上：  
     - 确保计划中的阶段划分（设置、基础、US1/US2/US3、优化）与 `tasks.md` 中的任务结构大致一致；  
     - 如发现 `spec/plan/tasks` 不一致，应在 `plan.md` 的“复杂性跟踪”或等效小节中记录差异，并为 `/elecspeckit.tasks` 预留修正任务。  
7. **Summarize outputs**  
   - 向用户总结本轮 `/elecspeckit.plan` 的主要改动：  
     - `IMPL_PLAN` 更新了哪些部分；  
     - `FEATURE_RESEARCH` / `FEATURE_DATA_MODEL` / `FEATURE_QUICKSTART` 是否被创建或扩展；  
   - 确认当前计划是否为下一步 `/elecspeckit.tasks` 拆分任务和 `/elecspeckit.docs` 生成文档提供了足够信息。  

**Notes**  
- 计划文件应保持“需求驱动”的风格：从 `spec.md` 和项目宪法出发，解释“为什么选择某种硬件方案”，而不是只罗列实现细节。  
- `research.md` 与 `data-model.md` 用于承载可追溯的决策过程和实体关系，便于后续在 `/elecspeckit.tasks`、`/elecspeckit.docs` 中复用这些信息。  
- 模板不绑定特定后端模块或脚本路径，具体 ElecSpeckit 规划逻辑由目标项目自身实现并通过测试保障。  
