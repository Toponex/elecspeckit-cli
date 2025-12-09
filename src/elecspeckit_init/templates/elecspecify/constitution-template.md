# ElecSpeckit 项目宪法（初始模板）

本文件由 `elecspeckit --init` 创建或重置，作为 ElecSpeckit 在当前项目中的“项目级宪法”起点。
请在 Claude/Qwen 中运行 `/elecspeckit.constitution` 命令，对本文件进行补充和修订。

## 项目范围与目标

- 本项目的硬件产品/板卡类型：[CLARIFY]
- 主要使用场景与环境（温度、电磁环境、供电条件等）：[CLARIFY]

## 库优先与 CLI 优先约定

- 本项目推荐的开发语言与库：[CLARIFY]
- 对 ElecSpeckit CLI 的使用规则（哪些环节必须通过 CLI/模板驱动完成）：[CLARIFY]

## 验证与测试策略

- 对硬件项目验证的基本要求：
  - **L1 计算与仿真验证**（参数计算、SPICE 仿真）：[CLARIFY]
  - **L2 样机功能测试**（输出电压、纹波、效率等）：[CLARIFY]
  - **L3 环境与认证测试**（温度循环、EMC、安规等）：[CLARIFY]
- 必须覆盖的关键测试项或安全相关验证：[CLARIFY]

## 可观察性与日志最小要求

- 需要记录的关键日志事件与字段：[CLARIFY]
- 对结构化日志和采集/存档的基本要求：[CLARIFY]

## 中文与本地化约定

- 对中文界面与文档的基本要求：[CLARIFY]
- 对英文技术术语使用的一致性约定：[CLARIFY]

## 领域特定规则（安全 / 性能 / 合规等）

- 安全/安规相关的强制要求：[CLARIFY]
- 性能、功耗、可靠性等方面的硬约束：[CLARIFY]

## 外部知识与 web 信息源约定

- 是否允许在 `/elecspeckit.specify` / `/elecspeckit.plan` / `/elecspeckit.tasks` 等工作流中使用 web 类信息源：[允许/禁止/仅在特定阶段允许]
- 推荐的单次 web 搜索结果数量区间（例如 10～100），后续脚本在构造 size 参数时必须遵守：[CLARIFY]
- 哪些问题必须优先查阅 `standards`（形式标准）/`company_kb`（公司知识库）/`reference_designs`（参考设计），只有在这些信息不足时才允许使用 `web` 作为补充：[CLARIFY]
- web 结果只能在 `research.md` 中作为“问题 + 候选证据 + 来源”的记录，最终 Decision 由工程师基于这些证据给出，而不是在 LLM 内部直接当成已验证事实：[CLARIFY]

> 提示: 具体可用信息源列表与策略建议，请在 `.elecspecify/memory/knowledge-sources.json` 中维护。

## Clarifications

> 通过 `/elecspeckit.constitution` 命令进行一轮或多轮澄清，
> 在下面按会话记录关键问题与决策。

### Session YYYY-MM-DD

- Q: 示例问题？ → A: 示例回答。
