---
description: Configure ElecSpeckit knowledge sources for the current project.
handoffs:
  - label: Update Constitution
    agent: elecspeckit.constitution
    prompt: Refresh project constitution after knowledge sources update
    send: false
---

## Command: `/elecspeckit.kbconfig`

**Goal**
通过受控流程维护 `.elecspecify/memory/knowledge-sources.json`，只允许通过本地 Python 脚本修改 JSON 文件，避免 LLM 直接重写配置导致结构损坏，使后续 `/elecspeckit.constitution`、`/elecspeckit.specify`、`/elecspeckit.plan` 等命令可以安全引用知识源配置。

**工程师如何使用**
- 首先在空目录中执行 `elecspeckit --init`，生成 `.elecspecify/memory/constitution.md` 与 `knowledge-sources.json` 的初始模板（包含 Metaso 和 Volces 预置条目），以及 `.elecspecify/scripts/win/python/` 下的管理脚本；
- 然后在同一目录作为工作区打开 Claude Code，在对话中运行：
  `/elecspeckit.kbconfig {可选补充说明}`
- 本命令不会直接在对话中重写 `knowledge-sources.json`，而是：
  - 读取当前配置文件并给出结构化视图；
  - 与工程师交互确认需要增删改查的条目；
  - 调用 `.elecspecify/scripts/win/python/kbconfig_*.py` 脚本执行 CRUD 操作；
  - 在关键步骤前展示即将执行的命令行，只有在工程师明确同意后才真正执行脚本。

**Knowledge Sources Schema (per FR-014)**

`knowledge-sources.json` 包含四大类别：

1. **`standards`** (行业/企业标准)
   - `enabled`: 布尔值
   - `sources[]`: 数组，每个条目包含：
     - `id`: 唯一标识符
     - `standard_number`: 标准编号 (如 "IPC-2221B")
     - `year`: 发布年份 (整数)
     - `deprecated`: 是否已废弃 (布尔值)
     - `title`: 标准标题
     - `abstract`: 摘要说明
     - `location`: 文件路径或 URL
     - `enabled`: 是否启用 (布尔值)

2. **`company_kb`** (公司知识库)
   - `enabled`: 布尔值
   - `sources[]`: 数组，每个条目包含：
     - `id`: 唯一标识符
     - `type`: 文档类型 (如 "guideline", "specification")
     - `title`: 文档标题
     - `authors`: 作者列表 (数组)
     - `year`: 发布年份 (整数)
     - `abstract`: 摘要说明
     - `location`: 文件路径或内部链接
     - `enabled`: 是否启用 (布尔值)

3. **`reference_designs`** (参考设计)
   - `enabled`: 布尔值
   - `sources[]`: 数组，每个条目包含：
     - `id`: 唯一标识符
     - `name`: 参考设计名称
     - `vendor`: 供应商 (如 "TI", "Analog Devices")
     - `url`: 官方链接
     - `key_parameters`: 关键参数 (对象，如 {"输出功率": "65W", "效率": ">95%"})
     - `location`: 本地文件路径
     - `enabled`: 是否启用 (布尔值)

4. **`web`** (外部 API 知识源)
   - `enabled`: 布尔值
   - `sources[]`: 数组，**默认预置 Metaso 和 Volces 两个条目**，每个条目包含：
     - `id`: 唯一标识符 (如 "metaso", "volces")
     - `name`: 显示名称
     - `url`: API 端点 URL (实际端点，非占位符)
     - `api_key`: API 密钥 (格式: `{{PLACEHOLDER:说明}}` 或 `ENV:变量名`)
     - `method`: HTTP 方法 ("POST" 或 "GET")
     - `headers`: 请求头 (对象，如 `{"Authorization": "Bearer {{api_key}}", "Content-Type": "application/json"}`)
     - `body_template`: 请求体模板 (对象，支持 `{{query}}` 变量替换)
     - `response_parser`: 响应解析器 (对象，**必须使用安全的 JSONPath 表达式，禁止 `eval`, `exec`, `__import__` 等危险字符**)
     - `enabled`: 是否启用 (布尔值，默认 `false`)

**安全约束 (per FR-015)**

- **response_parser 安全性**:
  - 必须使用安全的 JSONPath 表达式 (如 `$.data.results[*].title`)
  - 禁止包含 `eval()`, `exec()`, `__import__()`, `compile()`, `open()` 等危险函数
  - 推荐库: `jsonpath-ng` (Python)
  - 查询脚本在执行前必须验证 response_parser 语法，拒绝危险表达式

- **占位符约束**:
  - `api_key` 字段使用 `{{PLACEHOLDER:说明}}` 或 `ENV:变量名` 格式
  - `enabled=true` 的条目不得包含 `{{PLACEHOLDER:` 字符串
  - ENV 引用格式: `ENV:METASO_API_KEY` (从环境变量读取)

**Execution Steps（给 AI 助手）**

1. **初始化路径**
   在目标项目根目录工作，固定路径：
   - `KB_PATH = .elecspecify/memory/knowledge-sources.json`
   - `SCRIPTS_DIR = .elecspecify/scripts/win/python/`
   - `KB_VALIDATE = {SCRIPTS_DIR}/kbconfig_validate.py`
   - `KB_ADD = {SCRIPTS_DIR}/kbconfig_add.py`
   - `KB_UPDATE = {SCRIPTS_DIR}/kbconfig_update.py`
   - `KB_LIST = {SCRIPTS_DIR}/kbconfig_list.py`
   - `KB_DELETE = {SCRIPTS_DIR}/kbconfig_delete.py`

   如果 `KB_PATH` 不存在或为空，提示工程师使用 `elecspeckit --init` 重新初始化。

2. **读取并展示当前配置**
   只读读取 `KB_PATH` 内容，构建结构化视图：
   - 四个顶层类别: `standards`, `company_kb`, `reference_designs`, `web`
   - 每个类别的 `enabled` 状态和 `sources[]` 条目数量
   - **web.sources[]** 中的 Metaso 和 Volces 条目状态 (enabled, api_key 是否为占位符)
   - 突出显示包含 `{{PLACEHOLDER:` 的字段和 `enabled=false` 的条目

   如发现语法错误或缺失关键字段，提示"配置不完整或格式异常"。

3. **交互收集操作意图**
   与工程师对话，明确本轮操作：

   **查询操作**:
   - 列出所有知识源: `python {KB_LIST} --config {KB_PATH}`
   - 列出特定类别: `python {KB_LIST} --config {KB_PATH} --category standards`

   **添加操作** (示例):
   - 添加标准: `python {KB_ADD} --category standards --id IPC-2221B --standard_number IPC-2221B --year 2018 --title "PCB设计通用标准" --location "F:\standards\ipc2221b.pdf" --config {KB_PATH}`
   - 添加参考设计: `python {KB_ADD} --category reference_designs --id TI-PMP22682 --name "TI 65W PD充电器" --vendor TI --url "https://www.ti.com/tool/PMP22682" --location "F:\ref_designs\TI-PMP22682" --config {KB_PATH}`

   **更新操作** (示例):
   - 配置 Metaso API 密钥: `python {KB_UPDATE} --category web --id metaso --api_key "ENV:METASO_API_KEY" --enabled true --config {KB_PATH}`
   - 配置 Volces API 密钥: `python {KB_UPDATE} --category web --id volces --api_key "ENV:VOLCES_API_KEY" --enabled true --config {KB_PATH}`
   - 禁用某个条目: `python {KB_UPDATE} --category standards --id IPC-2221B --enabled false --config {KB_PATH}`

   **删除操作** (示例):
   - 删除条目: `python {KB_DELETE} --category standards --id IPC-2221B --config {KB_PATH}`

   **验证操作**:
   - 验证配置: `python {KB_VALIDATE} {KB_PATH}`

4. **展示并执行命令**
   - 在对话中展示完整的命令行
   - 提示工程师:
     - 可以复制到终端手工执行，或
     - 明确回复"执行/yes"授权 AI 助手代为调用
   - 只有在明确授权后，才实际调用脚本
   - 展示脚本输出结果

5. **汇报变更结果**
   重新读取 `KB_PATH`，用简短列表汇报已生效的变更：
   - 格式: "类别 + 操作 + 条目摘要"
   - 示例: "standards: add 'IPC-2221B'"、"web: metaso enabled=true, api_key=ENV:METASO_API_KEY"

6. **多轮修改支持**
   - 每轮处理一小批操作，避免一次性大范围修改
   - 每轮结束询问工程师是否继续
   - 工程师回复"stop/够了/先这样"时结束

7. **最终验证**
   命令结束前，调用 `KB_VALIDATE` 验证配置：
   - 验证通过: 提示"知识源配置已通过验证，可以继续运行 `/elecspeckit.constitution`"
   - 验证失败: 列出问题，建议回滚或重新运行 `/elecspeckit.kbconfig` 修复

**重要提示**

- **Metaso 和 Volces 预置条目**: `elecspeckit --init` 会自动在 `web.sources[]` 中创建 Metaso 和 Volces 两个条目，包含完整的 API 端点配置，但 `api_key` 为占位符，`enabled=false`。工程师需要通过本命令配置实际的 API 密钥并启用。

- **ENV 变量格式**: 推荐使用 `ENV:METASO_API_KEY` 格式引用环境变量，而非硬编码密钥到配置文件。查询脚本会在运行时自动从环境变量读取。

- **response_parser 安全**: 添加或更新 web 知识源时，确保 `response_parser` 只包含安全的 JSONPath 表达式 (如 `$.data.results`, `$.choices[*].message.content`)，避免代码注入风险。

- **不直接编辑 JSON**: 本命令不允许 AI 助手直接编辑 `knowledge-sources.json`，所有修改必须通过 Python 脚本完成，确保结构完整性和数据安全。
