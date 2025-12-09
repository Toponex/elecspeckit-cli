---
description: Run ElecSpeckit task generation and review workflow for the current hardware feature.
handoffs:
  - label: Generate Docs
    agent: elecspeckit.docs
    prompt: Generate multi-role docs based on updated tasks
    send: true
---

## Command: `/elecspeckit.tasks`

**Goal**  
基于 ElecSpeckit 的 `spec.md` 与 `plan.md`，为当前硬件特性更新或检查 `tasks.md` 任务清单，确保从用户故事到实现步骤的链路完整，并与 clarify / checklist / analyze 的结论一致。

**Execution Steps (for the AI assistant)**  
1. 在目标硬件项目根目录工作，与用户确认当前特性的 `FEATURE_DIR = specs/00X-shortname/`，并在其中找到：  
   - `FEATURE_SPEC  = FEATURE_DIR/spec.md`；  
   - `IMPL_PLAN     = FEATURE_DIR/plan.md`；  
   - `FEATURE_TASKS = FEATURE_DIR/tasks.md`（如尚不存在，可根据 `.elecspecify/templates/tasks-template.md` 创建骨架）。  
2. 从 `spec.md` 中提取用户故事、功能需求和成功标准（SC-001～SC-010），并对照 `plan.md` 中的阶段划分（设置、基础、US1/US2/US3、优化），梳理出需要落地的任务类别。  
3. 打开 `tasks.md`，检查并按以下原则维护任务：  
   - 每个用户故事（例如 US1/US2/US3）都有独立的一组任务，且可以单独完成和测试；  
   - 任务描述使用统一格式：`- [ ] Txxx [P?] [US?] 描述 + 文件路径`；  
   - 所有与模板、CLI 行为、日志、本地化相关的任务与 spec/plan 中的 FR/SC 一一对应。  
4. 将 clarify / checklist / analyze 的结论纳入任务清单：  
   - 对于 checklist 或 analyze 中标记的 Gap/Ambiguity，确保存在对应的治理或实现任务（例如补充文档、调整架构、增加 edge case 覆盖）；  
   - 对于 `/elecspeckit.clarify` 生成的澄清问题，如已得到答案，应通过任务推动把回答落实到 spec/plan/docs。  
5. 在任务中明确依赖关系与并行机会：  
   - 标记可以并行的任务为 `[P]`，避免不同任务争用同一文件；  
   - 保持“先测试再实现”的顺序（先 TDD 任务，再实现任务），并在任务描述中指出依赖的测试文件。  
6. 向用户报告：  
   - 调整后的任务总数与 US1/US2/US3 覆盖情况；  
   - 哪些 checklist/analyze/clarify 中提到的问题已经通过任务体现，哪些仍需后续迭代。  

**Notes**  
- 任务清单是 ElecSpeckit 工作流中“plan → tasks → docs”之间的关键桥梁，应随 `spec.md` / `plan.md` 的变更保持同步；  
- 不要在任务中泄露特定实现细节（例如具体库的内部结构），重点放在“要做什么”和“改动哪些文件”，实现细节由代码与测试负责；  
- 模板不假设具体的任务生成实现，由项目自行选择工具并通过测试验证。  
