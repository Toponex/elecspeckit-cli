---
description: Run ElecSpeckit clarify workflow to resolve high-value ambiguities in the current hardware spec.
handoffs:
  - label: Update Plan
    agent: elecspeckit.plan
    prompt: Reflect clarified requirements in the implementation plan
    send: true
---

## Command: `/elecspeckit.clarify`

**Goal**  
在 ElecSpeckit 特性中，对当前特性的规范文件进行“澄清优先”的审阅与补充：基于结构化问题，识别并记录关键模糊点、缺失决策和不完整场景，并把结论直接整合回规范中（Clarifications 区域 + 相关章节）。

**Scope（针对 ElecSpeckit 硬件规格）**  
- 当前分支对应的特性目录：`FEATURE_DIR/`  
- 主要文档：`FEATURE_SPEC`（必要）、`FEATURE_DIR` 下的 `plan.md`、`data-model.md`、`research.md`、`quickstart.md`（如存在则参考）。  

**Execution Steps（给 AI 助手执行用）**

1. 在目标项目根目录定位当前 ElecSpeckit 特性的 `FEATURE_DIR` 与 `FEATURE_SPEC`：  
   - 例如选择 `specs/<feature-id>/` 作为 `FEATURE_DIR`，其中的 `spec.md` 作为 `FEATURE_SPEC`；  
   - 如路径或特性 ID 不明确，应先向用户确认。  
2. 加载 `FEATURE_SPEC`，按以下维度做一次静态扫描并在心里打标签：  
   - 功能范围与行为（用户目标/成功条件、out-of-scope 是否明确）；  
   - 领域与数据模型（实体/字段/关系是否与 data-model 一致）；  
   - 交互与 UX 流（关键路径、错误/空/加载状态）；  
   - 非功能（性能、可扩展性、可靠性、可观测性、安全与合规）；  
   - 集成与外部依赖（外部 API、数据格式、协议/版本假设）；  
   - 边界条件与失败场景；  
   - 约束与权衡（技术约束、权衡决策是否显性）；  
   - 术语一致性与“Completion Signals”（验收标准是否可测量）。  
3. 按影响度优先级，内部构造 3～5 个澄清问题（不要一次全问出来），问题类型示例：  
   - “是否需要覆盖哪些异常/恢复场景？”  
   - “性能目标是大致范围还是有明确阈值？”  
   - “特定角色（PM/测试/文档）的视图期望什么粒度？”  
4. 逐个问用户，每次只问 1 个问题：  
   - 优先用结构化选项（A/B/C/D + E.其他 ≤20 字），让用户通过选项或少量中文作答；  
   - 给出你推荐的选项（Recommended），并附 1～2 句理由。  
5. 对每个得到明确回答的问题：  
   - 在 `FEATURE_SPEC` 中确保存在 `## Clarifications` 区域；  
   - 在其下为当天建立 `### Session YYYY-MM-DD` 子标题（如尚不存在）；  
   - 追加一条 bullet：`- Q: <问题> → A: <最终答案>`；  
   - 在对应章节做最小必要修改，例如：  
     - 功能/非功能需求小节补充明确阈值；  
     - 数据模型章节补充字段/关系；  
     - Edge Cases/错误处理小节补充新的场景；  
     - 若存在旧的矛盾表述，进行替换而不是叠加。  
6. 每次修改后保存 `FEATURE_SPEC`，并快速自检：  
   - 新增 Clarifications 区域结构正确；  
   - 没有残留与新答案相冲突的旧表述；  
   - 术语（例如 ElecSpeckit、CLI 名称）使用前后一致。  
7. 采用“每批次约 5 个问题”的节奏：  
   - 每当累计问完 5 个问题后，向用户确认是否继续澄清更多领域（例如：“是否继续澄清更多规格问题？Y/N”）；  
   - 如用户说明先到这里（如“stop/够了/先这样”或选择 N），则停止继续提问；  
   - 否则，从剩余的高优先级模糊点中继续选出下一批（最多 5 个）问题，一问一答地推进；  
   - 对于明显低风险或可在 plan/tasks/docs 阶段处理的模糊点，可以在 Clarifications 中标注为“可后续澄清”，避免一次会话中过度打扰用户。  

**Output to User**  
- 告知本次共问了多少个问题，处理了哪些领域（例如“性能”、“集成”、“角色文档”等）；  
- 给出 Clarifications 区域的路径：`FEATURE_SPEC`；  
- 简要罗列哪些类别已经“Resolved”（例如性能目标、关键外部依赖），哪些留待后续 Clarify/Plan 再处理。  

**Notes**  
- 模板仅描述 ElecSpeckit 工作流与澄清方法，不绑定具体脚本或后端实现；  
- 如在澄清过程中发现需要调整工作流本身，应在 ElecSpeckit 框架层的 `/speckit.*` 规范中单独演进，而不是在具体硬件项目中临时修改流程。  
