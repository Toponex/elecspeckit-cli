# /elecspeckit.skillconfig - Skills 配置管理命令

管理已部署的 Claude Skills 的启用/禁用状态、API 密钥配置和一致性验证。

## 功能概述

此命令提供以下子命令用于管理 `.elecspecify/memory/skill_config.json` 和 `.claude/skills/` 目录：

- `list` - 列出所有已部署的 Skills 及其状态
- `enable` - 启用指定的 Skill
- `disable` - 禁用指定的 Skill
- `update` - 更新 Skill 的配置（如 API 密钥）
- `validate` - 验证配置与实际文件的一致性

## 子命令详解

### 1. list - 列出所有 Skills

**功能**: 读取 `skill_config.json` 并显示所有 Skills 的状态清单。

**用法**:
```bash
/elecspeckit.skillconfig list [--format json|text]
```

**参数**:
- `--format` (可选): 输出格式
  - `text` (默认): 人类可读的表格格式
  - `json`: 机器可读的 JSON 格式

**示例 1: 文本格式输出**
```bash
/elecspeckit.skillconfig list
```

**预期输出**:
```
已部署的 Claude Skills（共 24 个）:

状态  Skill 名称                     API需求  API配置  描述
==================================================================
[✓]   docs-seeker                   否       N/A      查找技术文档
[✗]   mouser-component-search       是       已配置   Mouser API集成
[✓]   arxiv-search                  否       N/A      搜索学术论文
...

统计:
  - 已启用: 20
  - 已禁用: 4
  - 需要 API: 3（其中 1 个未配置）
```

**示例 2: JSON 格式输出**
```bash
/elecspeckit.skillconfig list --format json
```

**预期输出**:
```json
{
  "success": true,
  "skills": [
    {
      "name": "docs-seeker",
      "enabled": true,
      "requires_api": false,
      "api_configured": false,
      "description": "查找技术文档（芯片数据手册、标准文档）"
    },
    {
      "name": "mouser-component-search",
      "enabled": false,
      "requires_api": true,
      "api_configured": true,
      "description": "Mouser API集成（元器件搜索、库存查询、定价）"
    }
  ],
  "total": 24,
  "enabled_count": 20,
  "disabled_count": 4,
  "requires_api_count": 3
}
```

**实现**: 调用 `.elecspecify/scripts/skillconfig_list.py`

---

### 2. enable - 启用 Skill

**功能**: 将指定 Skill 的 `enabled` 字段设为 `true`，并将 `(DISABLED)SKILL.md` 重命名为 `SKILL.md`，使 Claude Code 能够加载该 Skill。

**用法**:
```bash
/elecspeckit.skillconfig enable <skill_name>
```

**参数**:
- `skill_name` (必填): Skill 名称（如 "arxiv-search"）

**示例**:
```bash
/elecspeckit.skillconfig enable arxiv-search
```

**预期输出**:
```json
{
  "success": true,
  "message": "已启用 Skill: arxiv-search",
  "changes": {
    "config_updated": true,
    "file_renamed": true,
    "previous_state": false,
    "current_state": true
  }
}
```

**操作流程**:
1. 验证 `arxiv-search` 存在于 `skill_config.json` 中
2. 检查 `.claude/skills/arxiv-search/(DISABLED)SKILL.md` 是否存在
3. 更新 `skill_config.json` 中的 `enabled: true`（原子性更新）
4. 重命名 `(DISABLED)SKILL.md` → `SKILL.md`
5. 验证配置一致性

**错误处理**:
- 如果 Skill 不存在，返回错误码 3
- 如果文件重命名失败（权限不足或文件被占用），返回错误码 4
- 如果 Skill 已启用，操作仍然成功（幂等性）

**实现**: 调用 `.elecspecify/scripts/skillconfig_enable.py`

---

### 3. disable - 禁用 Skill

**功能**: 将指定 Skill 的 `enabled` 字段设为 `false`，并将 `SKILL.md` 重命名为 `(DISABLED)SKILL.md`，防止 Claude Code 加载该 Skill。

**用法**:
```bash
/elecspeckit.skillconfig disable <skill_name>
```

**参数**:
- `skill_name` (必填): Skill 名称

**示例**:
```bash
/elecspeckit.skillconfig disable arxiv-search
```

**预期输出**:
```json
{
  "success": true,
  "message": "已禁用 Skill: arxiv-search",
  "changes": {
    "config_updated": true,
    "file_renamed": true,
    "previous_state": true,
    "current_state": false
  }
}
```

**使用场景**:
- 临时禁用不需要的 Skills 以提高加载速度
- 禁用需要 API 但尚未配置密钥的 Skills
- 调试时排除特定 Skills 的干扰

**操作流程**:
1. 验证 Skill 存在且当前已启用
2. 更新 `skill_config.json` 中的 `enabled: false`（原子性更新）
3. 重命名 `SKILL.md` → `(DISABLED)SKILL.md`
4. 验证配置一致性

**实现**: 调用 `.elecspecify/scripts/skillconfig_disable.py`

---

### 4. update - 更新 Skill 配置

**功能**: 更新 `skill_config.json` 中指定 Skill 的 API 密钥。

**用法**:
```bash
/elecspeckit.skillconfig update <skill_name> --api-key <key>
```

**参数**:
- `skill_name` (必填): Skill 名称
- `--api-key` (必填): API 密钥值

**示例 1: 配置 Mouser API 密钥**
```bash
/elecspeckit.skillconfig update mouser-component-search --api-key "12345678-1234-1234-1234-123456789012"
```

**预期输出**:
```json
{
  "success": true,
  "message": "已更新 Skill: mouser-component-search 的 API 密钥",
  "validation_passed": true,
  "prompt": "该 Skill 当前已禁用。是否同时启用？(运行: /elecspeckit.skillconfig enable mouser-component-search)"
}
```

**示例 2: 配置 Perplexity API 密钥**
```bash
/elecspeckit.skillconfig update perplexity-search --api-key "pplx-abcdefghijklmnopqrstuvwxyz"
```

**注意事项**:
- 仅支持更新 `requires_api: true` 的 Skills（如 `mouser-component-search`、`perplexity-search`）
- 不支持更新 `description` 字段（只读字段）
- 不支持通过此命令修改 `enabled` 字段（请使用 `enable`/`disable` 命令）
- 更新后会自动调用 `skillconfig_validate.py` 验证配置有效性
- 如果验证失败，更新会回滚（原子性保证）

**错误处理**:
- 如果尝试更新不支持的字段，返回错误码 1
- 如果 Skill 不需要 API（`requires_api: false`），返回错误
- 如果验证失败（如密钥格式无效），删除临时文件并回滚

**实现**: 调用 `.elecspecify/scripts/skillconfig_update.py`

---

### 5. validate - 验证配置一致性

**功能**: 验证 `skill_config.json` 与实际 `.claude/skills/` 目录下的 SKILL.md 文件一致性，检查配置有效性。

**用法**:
```bash
/elecspeckit.skillconfig validate
```

**验证规则**:
1. **配置与文件一致性**:
   - 如果 `enabled: true`，则 `SKILL.md` 必须存在
   - 如果 `enabled: false`，则 `(DISABLED)SKILL.md` 必须存在

2. **API 配置完整性**:
   - 如果 `requires_api: true` 且 `enabled: true`，则 `api_key` 字段必须存在且非空

3. **JSON 格式有效性**:
   - 所有必填字段（`enabled`, `requires_api`, `description`）必须存在
   - 数据类型正确（`enabled` 为 boolean, `description` 为 string）

**示例 1: 验证成功**
```bash
/elecspeckit.skillconfig validate
```

**预期输出**:
```json
{
  "success": true,
  "message": "配置验证通过",
  "validation": {
    "total_skills": 24,
    "validated": 24,
    "errors": 0,
    "warnings": 0
  }
}
```

**示例 2: 验证失败**
```bash
/elecspeckit.skillconfig validate
```

**预期输出**:
```json
{
  "success": false,
  "error": {
    "code": 3,
    "message": "配置验证失败: 发现 2 个错误",
    "issues": [
      {
        "skill": "mouser-component-search",
        "severity": "error",
        "message": "Skill 已启用但缺少 API 密钥（requires_api: true）"
      },
      {
        "skill": "arxiv-search",
        "severity": "error",
        "message": "配置状态为 enabled: true 但 SKILL.md 文件不存在"
      }
    ]
  }
}
```

**使用场景**:
- 手动修改 `skill_config.json` 后验证格式正确性
- 排查 Skills 加载问题（文件缺失或配置不一致）
- 升级后确认 Skills 部署完整

**实现**: 调用 `.elecspecify/scripts/skillconfig_validate.py`

---

## 完整工作流示例

### 场景 1: 首次配置 Mouser API

```bash
# 1. 查看当前 Skills 状态
/elecspeckit.skillconfig list

# 2. 配置 Mouser API 密钥
/elecspeckit.skillconfig update mouser-component-search --api-key "YOUR_MOUSER_API_KEY"

# 3. 启用 mouser-component-search Skill
/elecspeckit.skillconfig enable mouser-component-search

# 4. 验证配置一致性
/elecspeckit.skillconfig validate

# 5. 确认 Skill 已启用
/elecspeckit.skillconfig list --format json | grep "mouser-component-search"
```

### 场景 2: 临时禁用不需要的 Skills

```bash
# 禁用学术搜索相关的 Skills
/elecspeckit.skillconfig disable arxiv-search
/elecspeckit.skillconfig disable openalex-database

# 确认禁用成功
/elecspeckit.skillconfig list
```

### 场景 3: 排查配置问题

```bash
# 运行验证命令
/elecspeckit.skillconfig validate

# 如果发现错误，查看详细信息
/elecspeckit.skillconfig list --format json

# 修复不一致的状态
/elecspeckit.skillconfig enable <有问题的skill名称>
```

---

## 技术说明

### 文件结构

```
.elecspecify/memory/skill_config.json    # Skills 配置文件
.elecspecify/scripts/
  ├── skillconfig_list.py                # list 子命令脚本
  ├── skillconfig_enable.py              # enable 子命令脚本
  ├── skillconfig_disable.py             # disable 子命令脚本
  ├── skillconfig_update.py              # update 子命令脚本
  └── skillconfig_validate.py            # validate 子命令脚本

.claude/skills/                           # Skills 目录
  ├── docs-seeker/
  │   └── SKILL.md                        # 启用状态
  ├── mouser-component-search/
  │   └── (DISABLED)SKILL.md             # 禁用状态
  └── ...
```

### 原子性更新机制

所有修改 `skill_config.json` 的操作都遵循原子性更新流程：

1. 读取原始配置到内存
2. 创建临时文件 `.elecspecify/memory/skill_config.json.tmp`
3. 写入更新后的配置到临时文件
4. 调用 `skillconfig_validate.py` 验证临时文件
5. 如果验证通过，原子重命名 `skill_config.json.tmp` → `skill_config.json`
6. 如果验证失败或文件操作失败，删除临时文件并回滚

这确保了配置更新要么完全成功，要么完全失败，绝不留下不一致状态。

### 退出码

所有脚本遵循统一的退出码契约：

- `0`: 操作成功
- `1`: 参数错误（缺少参数、格式错误）
- `2`: 文件访问错误（配置文件不存在、权限不足）
- `3`: 验证失败（配置不一致、Skill 不存在）
- `4`: 操作失败（文件重命名失败、JSON 写入失败）

### 安全性

- API 密钥存储在 `skill_config.json` 中，文件权限设为 0600（仅文件所有者可读写）
- Python 脚本在服务端执行，API 密钥不传递给 LLM 上下文
- SKILL.md 文件中不包含 API 密钥占位符或示例密钥

---

## 常见问题

**Q1: 为什么启用 Skill 后 Claude Code 没有加载？**

A: 请检查以下几点：
1. 运行 `/elecspeckit.skillconfig validate` 确认配置一致性
2. 确认 `SKILL.md` 文件存在（不是 `(DISABLED)SKILL.md`）
3. 重启 Claude Code 使配置生效

**Q2: 如何查看哪些 Skills 需要 API 密钥？**

A: 运行 `/elecspeckit.skillconfig list --format json`，查找 `requires_api: true` 的 Skills。

**Q3: 可以同时启用所有 Skills 吗？**

A: 可以，但需要 API 的 Skills（如 `mouser-component-search`）必须先配置 API 密钥，否则会在使用时报错。

**Q4: 手动编辑了 `skill_config.json`，如何确认没有错误？**

A: 运行 `/elecspeckit.skillconfig validate` 检查配置有效性。如果有错误，命令会列出具体问题。

**Q5: 禁用 Skill 后数据会丢失吗？**

A: 不会。禁用只是重命名 `SKILL.md` 为 `(DISABLED)SKILL.md`，所有文件和配置都会保留。重新启用即可恢复。

---

## 参考资料

- **契约规范**: `specs/002-claude-skills-support/contracts/skillconfig_scripts_contract.md`
- **JSON Schema**: `specs/002-claude-skills-support/contracts/skill_config_schema.json`
- **API 安全架构**: `specs/002-claude-skills-support/plan.md` L26-43
- **ElecSpeckit 规范**: `specs/002-claude-skills-support/spec.md` (FR-017 到 FR-020)
