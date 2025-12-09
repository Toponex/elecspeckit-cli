---
description: Run ElecSpeckit analyze workflow to perform cross-document consistency analysis for the current hardware feature.
handoffs:
  - label: Clarify Spec
    agent: elecspeckit.clarify
    prompt: Clarify top ambiguities found in the analysis report
    send: true
---

## Command: `/elecspeckit.analyze`

**Goal**  
在当前硬件项目中，对某个特性的 `spec.md`、`plan.md`、`tasks.md` 做一次只读的一致性分析，帮助识别：缺失的需求、未覆盖的任务、显式冲突或术语不一致，而不直接修改任何文件。

**工程师如何使用**  
- 典型调用方式：  
  ```text
  /elecspeckit.analyze
  ```  
  或附上一句：`请分析当前特性。`  
- 不要求工程师写长说明，本命令默认自行扫描并出报告。

**Execution Steps（给 AI 助手）**

1. 在目标项目根目录工作，根据用户的简单输入（或上下文）确定要分析的 `FEATURE_DIR`（例如 `specs/<feature-id>/`），并推导：  
   - `FEATURE_SPEC = FEATURE_DIR/spec.md`  
   - `FEATURE_PLAN = FEATURE_DIR/plan.md`  
   - `FEATURE_TASKS = FEATURE_DIR/tasks.md`（如缺失，在报告中标记为缺失）；  
   - 如存在：`FEATURE_DOCS = FEATURE_DIR/docs/`；  
   - 宪法文件路径：`.elecspecify/memory/constitution.md`。  
2. 若上述任一核心文件缺失：  
   - 不要创建新文件，直接在报告中用“CRITICAL” 标记缺失项，并建议用户先运行 `/elecspeckit.specify`、`/elecspeckit.plan` 或 `/elecspeckit.tasks`。  
3. 在不回写文件的前提下，构建粗略的语义模型：  
   - `spec.md`：提取用户故事、功能需求、非功能需求、成功标准、边缘情况；  
   - `plan.md`：提取架构/技术决策、阶段划分、约束与权衡；  
   - `tasks.md`：提取任务 ID、所属用户故事、描述和文件路径。  
4. 分析结果只写入 `FEATURE_DIR/checklists/` 下的报告文件（例如 `analysis.md` 或带时间戳的报告），不得修改 `spec/plan/tasks/docs` 或宪法本身。  
5. 按下列方向做高信号分析（最多列出约 50 条发现）：  
   - 覆盖性：哪些需求在 tasks 中没有任何对应任务；  
   - 冗余：明显重复或矛盾的需求；  
   - 非功能：性能/安全/本地化等要求是否在 tasks 中有对应实现或验证任务；  
   - 一致性：术语是否在 spec/plan/tasks 中保持一致；  
   - 顺序问题：tasks 中是否存在明显违背 plan 阶段顺序的任务（例如先做集成再做基础）。  
6. 将结果以 Markdown 表格形式输出到终端，例如：  
   - “Specification Analysis Report” 表格：列出 ID/Category/Severity/Location/Summary/Recommendation；  
   - 简短的 Coverage Summary：展示部分关键需求是否已有任务覆盖；  
   - 明确说明：本命令没有修改任何文件。  
7. 如果用户在命令后附加了特定关注点（例如“只想看性能和安全”），在分析中优先强调这些部分。

**Notes**  
- `/elecspeckit.analyze` 只负责发现问题和提示下一步操作，不负责修改 spec/plan/tasks；修正应通过 `/elecspeckit.specify`、`/elecspeckit.plan`、`/elecspeckit.tasks` 或手工编辑完成。  
- 对于需要多轮分析的项目，可以在报告中建议后续运行 `/elecspeckit.checklist` 或 `/elecspeckit.clarify` 进一步细化。  
