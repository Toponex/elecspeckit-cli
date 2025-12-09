---
description: Run ElecSpeckit constitution workflow for the current project.
handoffs:
  - label: Specify First Feature
    agent: elecspeckit.specify
    prompt: Write first hardware feature spec based on this constitution
    send: true
---

## Command: `/elecspeckit.constitution`

**Goal**  
在具体硬件项目中，为当前仓库建立一份“项目级 ElecSpeckit 宪法”，说明该项目在库优先、CLI 优先、TDD、可观察性、中文本地化，以及本领域安全/性能/合规等方面的基本规则，为后续 `/elecspeckit.specify`、`/elecspeckit.plan`、`/elecspeckit.tasks` 提供共同约束。

**工程师如何使用**  
- 首先在一个空目录中执行 `elecspeckit --init`，生成 `.elecspecify/memory/constitution.md` 与 `knowledge-sources.json` 的初始模板，以及 `.elecspecify/scripts/` 下的占位脚本；如后续仅需重置宪法模板，可在同一目录下执行 `elecspeckit --reset-constitution`；  
- 然后在同一目录作为工作区打开 Claude Code，按顺序运行：  
  1）`/elecspeckit.kbconfig`：先把 `.elecspecify/memory/knowledge-sources.json` 中的 `[在此…]` 占位条目替换为项目真实的标准/公司知识库/参考设计/web 信息源；  
  2）`/elecspeckit.constitution {可选补充说明}`：在知识源配置通过校验后，再逐步补充/修订宪法条款；  
- 本命令不会要求工程师一次性写出完整宪法，而是：  
  - 自动加载当前 `.elecspecify/memory/constitution.md` 内容；  
  - 结合补充说明和少量问题，逐步补充/修订条款；  
  - 在需要时提示如何“仅更新模板”或“在后续步骤中更新 spec/plan/tasks/docs”，而不是直接覆盖业务文档。

**Execution Steps（给 AI 助手）**

0. 先对知识源配置做门禁检查：  
   - 固定使用 `KB_PATH = .elecspecify/memory/knowledge-sources.json` 和 `KB_VALIDATE_SCRIPT = .elecspecify/scripts/kbconfig_validate.py`；  
   - 调用：  
     ```text
     python .elecspecify/scripts/kbconfig_validate.py --kb .elecspecify/memory/knowledge-sources.json
     ```  
   - 解析脚本输出的 JSON（例如 `{"status": "ok"}` 或 `{"status": "invalid", "reasons": [...]}`）：  
     - 若 `status != "ok"`，必须向工程师解释当前 `knowledge-sources.json` 仍未配置完成（例如仍包含 `[在此…]` 占位条目），提示先运行 `/elecspeckit.kbconfig` 完成知识源配置，然后**结束本次 `/elecspeckit.constitution` 流程**，不继续修改宪法；  
     - 只有当 `status == "ok"` 时，才可以继续后续步骤。  

1. 在目标项目根目录工作，**固定使用** `.elecspecify/memory/constitution.md` 作为宪法文件路径：  
   - 设定 `CONSTITUTION_PATH = .elecspecify/memory/constitution.md`；  
   - 如果该文件不存在或无法读取，先提醒用户需要在当前目录运行 `elecspeckit --init`（或在已存在 ElecSpeckit 项目中执行 `elecspeckit --reset-constitution`）生成或重置初始模板，然后结束本次指令。  
2. 读取 `CONSTITUTION_PATH` 当前内容和用户输入的简短补充描述，结合仓库已有信息（如已有 spec/plan）判断信息密度：  
   - 若信息很少，仅说明大致项目类型，则先创建一个包含若干小节的宪法骨架：  
     - 项目范围与目标  
     - 库优先与 CLI 优先约定  
     - 测试驱动与集成测试要求  
     - 可观察性与日志最小要求  
     - 中文与本地化约定  
     - 领域特定规则（例如安全、电磁兼容、性能/功耗约束）  
   - 对每个小节可以先填入占位说明，标出 `[CLARIFY]`。  
3. 基于当前骨架构造高优先级问题，并为每个问题设计结构化选项（例如 A/B/C/D + E.其他）：  
   - 例如：“本项目最优先保证的是哪一类约束？A：安全/安规 B：性能/功耗 C：成本/面积 D：可制造性/可维护性 E：其他（≤20字）”；  
   - 再如：“是否必须强制 TDD？A：是，所有关键模块 B：仅核心模块 C：不强制 D：按模块重要性灵活决定 E：其他（≤20字）”。  
4. 以“一问一答”方式与用户交互：  
   - 每次只发出 1 个问题，提示用户仅需回复选项字母或少量中文；  
   - 构造选项时推荐使用 “A/B/C/D + E.其他（≤20 字）” 的形式：  
     - 例如：“本项目最优先保证的是哪一类约束？A：安全/安规 B：性能/功耗 C：成本/面积 D：可制造性/可维护性 E：其他（≤20字）”；  
     - 再如：“是否必须强制 TDD？A：是，所有关键模块 B：仅核心模块 C：不强制 D：按模块重要性灵活决定 E：其他（≤20字）”；  
   - 解析回答后，立即在宪法文档中：  
     - 在 `## Clarifications` / `### Session YYYY-MM-DD` 下追加 `- Q: ... → A: ...`；  
     - 在对应小节中用一两句中文明确记录该决策（替换掉原先的占位 `[CLARIFY]`）。  
5. 重复第 3～4 步，逐个处理当前宪法中的 `[CLARIFY]` 标记：  
- 如用户回复“stop/够了/先这样”，立即停止提问，结束本次运行；  
- 否则应持续提问，直到当前会话中已识别的重要 `[CLARIFY]` 问题都得到明确回答，而不是简单地问满固定数量后就停止。  
6. 将更新后的完整宪法内容写回 `CONSTITUTION_PATH`（`.elecspecify/memory/constitution.md`），并用简短列表总结本轮新增的关键规则（例如“安全优先”“必须为核心模块编写集成测试”等）。  
7. 根据更新后的宪法内容，判断是否对 ElecSpeckit 模板、知识源配置与文档结构产生影响，并与用户确认下一步：  
   - 选项 A：“仅更新模板”——在对话中列出需要调整的 `.elecspecify/templates/*` 文件和建议修改点，引导用户在模板层面完成约束对齐；  
   - 选项 B：“审查/更新知识源配置”——根据最新宪法中的“外部知识与 web 信息源约定”章节，与工程师一起检查 `.elecspecify/memory/knowledge-sources.json` 是否需要调整（例如是否启用 web、推荐结果数量区间、是否需要新增或移除某些 sources 条目），并在需要时建议工程师重新运行 `/elecspeckit.kbconfig` 或手工编辑该文件；  
   - 选项 C：“在后续步骤中审查/更新 spec/plan/tasks/docs”——提示用户在完成模板与知识源配置更新后，通过 `/elecspeckit.plan`、`/elecspeckit.tasks`、`/elecspeckit.docs` 分别对现有特性文档进行审查和增量更新；  
   - 无论用户选择哪一项，本命令 **不得直接修改** 任何 `spec/plan/tasks/docs` 文件，只能对 `.elecspecify/memory/constitution.md` 给出建议或执行更新，并通过自然语言建议工程师如何维护 `.elecspecify/memory/knowledge-sources.json` 与 `.elecspecify/templates/*`。

**Notes**  
- 宪法文件应尽量短小但明确，避免把细节设计塞进宪法；细节应放在每个特性的 spec/plan 中。  
- 项目在未来迭代中可以多次调用 `/elecspeckit.constitution`，每次新增或修订少量规则，并通过 Clarifications 区域记录决策历史。  
