---
description: "管理 ElecSpeckit Claude Skills 配置 - 列出、启用、禁用、更新和验证 Skills"
---

# /elecspeckit.skillconfig - Skills 配置管理

管理 ElecSpeckit Claude Skills 的启用状态、API 密钥配置和一致性验证。

## 概述

ElecSpeckit 提供了 24 个专业 Skills 增强硬件设计工作流,涵盖信息检索、文档生成、数据分析、嵌入式开发、元器件采购等领域。

`/elecspeckit.skillconfig` 命令提供以下子命令来管理这些 Skills:

- **list**: 列出所有 Skills 及其配置状态
- **enable**: 启用指定的 Skill
- **disable**: 禁用指定的 Skill
- **update**: 更新 Skill 配置 (如 API 密钥)
- **validate**: 验证配置文件与 Skills 文件一致性

## 使用场景

### 场景 1: 查看所有可用的 Skills

当你想了解有哪些 Skills 可用,以及它们的启用状态时:

```
用户: /elecspeckit.skillconfig list

AI: [执行] python .claude/scripts/win/python/skillconfig_list.py

输出:
============================================================
ElecSpeckit Skills 列表 (v0.2.0)
平台: claude
============================================================

## 信息检索类 (information_retrieval)

✅ **docs-seeker**
   搜索和定位项目文档、技术规格书、数据手册

❌ **perplexity-search** [需要 API]
   使用 Perplexity AI 进行深度网络搜索和研究

...

============================================================
图例: ✅ 已启用 | ❌ 已禁用 | [需要 API] 需要配置 API 密钥
```

### 场景 2: 启用一个禁用的 Skill

当你想使用某个被禁用的 Skill 时:

```
用户: /elecspeckit.skillconfig enable docs-seeker

AI: [执行] python .claude/scripts/win/python/skillconfig_enable.py docs-seeker

输出:
✅ Skill 'docs-seeker' 已启用
```

**副作用**:
- `skill_config.json` 中 `enabled: true`
- `(DISABLED)SKILL.md` 重命名为 `SKILL.md`
- Claude Code 现在可以加载和调用此 Skill

### 场景 3: 禁用一个启用的 Skill

当你想临时停用某个 Skill 时:

```
用户: /elecspeckit.skillconfig disable docs-seeker

AI: [执行] python .claude/scripts/win/python/skillconfig_disable.py docs-seeker

输出:
❌ Skill 'docs-seeker' 已禁用
```

**副作用**:
- `skill_config.json` 中 `enabled: false`
- `SKILL.md` 重命名为 `(DISABLED)SKILL.md`
- Claude Code 不再加载此 Skill
- **API 密钥保留**: 如果之前配置过 API 密钥,会被保留,下次启用时无需重新配置

### 场景 4: 配置需要 API 密钥的 Skill

某些 Skills (如 `perplexity-search`, `mouser-component-search`) 需要外部 API 密钥才能工作。配置流程:

```
用户: /elecspeckit.skillconfig update perplexity-search --api-key pplx-abc123xyz...

AI: [执行] python .claude/scripts/win/python/skillconfig_update.py perplexity-search --api-key pplx-abc123xyz...

输出:
✅ Skill 'perplexity-search' 配置已更新
   API 密钥已设置

然后启用 Skill:

用户: /elecspeckit.skillconfig enable perplexity-search

AI: [执行] python .claude/scripts/win/python/skillconfig_enable.py perplexity-search

输出:
✅ Skill 'perplexity-search' 已启用
```

**安全机制**:
- API 密钥存储在 `.elecspecify/memory/skill_config.json`
- 文件权限自动设置为 `0600` (仅所有者可读写)
- Python 脚本从 JSON 读取密钥,**绝不暴露给 LLM**
- Skill 的 `SKILL.md` 文件**不包含**任何 API 密钥

### 场景 5: 验证配置一致性

当你怀疑配置文件与实际 Skills 文件不一致时 (例如手动修改了文件后):

```
用户: /elecspeckit.skillconfig validate

AI: [执行] python .claude/scripts/win/python/skillconfig_validate.py

输出 (验证通过):
{
  "status": "valid",
  "errors": [],
  "warnings": []
}

输出 (验证失败):
{
  "status": "invalid",
  "errors": [
    {
      "skill": "docs-seeker",
      "error": "enabled: true 但文件名为 (DISABLED)SKILL.md"
    }
  ],
  "warnings": [
    {
      "skill": "my-custom-skill",
      "warning": "Skills 目录中存在但未在配置中"
    }
  ]
}
```

**修复不一致**: 根据错误信息,使用 enable/disable 命令修复配置

## 子命令详细说明

### list - 列出所有 Skills

**用法**:
```bash
python .claude/scripts/win/python/skillconfig_list.py [--format {text|json}]
```

**选项**:
- `--format text`: 文本格式输出 (默认,按分类显示,带状态图标)
- `--format json`: JSON 格式输出 (完整配置数据)

**输出示例** (text 格式):
```
============================================================
ElecSpeckit Skills 列表 (v0.2.0)
============================================================

## 信息检索类 (information_retrieval)

✅ **docs-seeker**
   搜索和定位项目文档、技术规格书、数据手册

❌ **perplexity-search** [需要 API]
   使用 Perplexity AI 进行深度网络搜索和研究
```

### enable - 启用 Skill

**用法**:
```bash
python .claude/scripts/win/python/skillconfig_enable.py <skill_name>
```

**功能**:
1. 更新 `skill_config.json` 中 `enabled: true`
2. 重命名 `(DISABLED)SKILL.md` → `SKILL.md`
3. Claude Code 开始加载此 Skill

**退出码**:
- `0`: 成功
- `1`: Skill 不存在
- `2`: 文件重命名失败 (权限问题或文件被占用)

**示例**:
```bash
python .claude/scripts/win/python/skillconfig_enable.py docs-seeker
```

### disable - 禁用 Skill

**用法**:
```bash
python .claude/scripts/win/python/skillconfig_disable.py <skill_name>
```

**功能**:
1. 更新 `skill_config.json` 中 `enabled: false`
2. 重命名 `SKILL.md` → `(DISABLED)SKILL.md`
3. **保留 API 密钥配置**
4. Claude Code 停止加载此 Skill

**退出码**:
- `0`: 成功
- `1`: Skill 不存在
- `2`: 文件重命名失败

**示例**:
```bash
python .claude/scripts/win/python/skillconfig_disable.py perplexity-search
```

### update - 更新配置 (API 密钥)

**用法**:
```bash
python .claude/scripts/win/python/skillconfig_update.py <skill_name> --api-key <API_KEY>
```

**功能**:
1. 更新 `skill_config.json` 中的 `api_key` 字段
2. 使用**原子性更新**机制 (临时文件 → 验证 → 替换)
3. 自动调用 `skillconfig_validate.py` 验证配置
4. **验证失败时自动回滚**

**原子性更新流程**:
```
1. 创建临时文件 skill_config.tmp.json
2. 写入更新后的配置到临时文件
3. 调用 skillconfig_validate.py 验证临时文件
4. 如果验证通过:
   - 替换原文件
   - 保留文件权限 (0600)
5. 如果验证失败:
   - 删除临时文件
   - 原配置文件保持不变
   - 返回退出码 3
```

**退出码**:
- `0`: 成功
- `1`: Skill 不存在或不需要 API
- `2`: 权限问题
- `3`: 验证失败,已回滚
- `4`: JSON 格式错误

**示例**:
```bash
# 设置 API 密钥
python .claude/scripts/win/python/skillconfig_update.py perplexity-search --api-key pplx-abc123xyz...

# 清空 API 密钥
python .claude/scripts/win/python/skillconfig_update.py perplexity-search --api-key ""
```

### validate - 验证配置一致性

**用法**:
```bash
python .claude/scripts/win/python/skillconfig_validate.py
```

**验证内容**:
1. `skill_config.json` 文件格式正确
2. 配置中的每个 Skill 目录存在
3. `enabled: true` 的 Skill 有 `SKILL.md` 文件
4. `enabled: false` 的 Skill 有 `(DISABLED)SKILL.md` 文件
5. Skills 目录中的 Skill 都在配置中 (警告)

**输出格式** (JSON):
```json
{
  "status": "valid" | "invalid",
  "errors": [
    {"skill": "skill-name", "error": "错误描述"}
  ],
  "warnings": [
    {"skill": "skill-name", "warning": "警告描述"}
  ]
}
```

**退出码**:
- `0`: 验证通过 (status: "valid")
- `1`: 配置文件不存在
- `3`: 验证失败 (status: "invalid")
- `4`: JSON 格式错误

**示例**:
```bash
python .claude/scripts/win/python/skillconfig_validate.py
```

## 完整工作流示例

### 工作流 1: 启用需要 API 的 Skill

```bash
# 1. 查看 Skill 状态
python .claude/scripts/win/python/skillconfig_list.py

# 2. 配置 API 密钥
python .claude/scripts/win/python/skillconfig_update.py perplexity-search \
  --api-key pplx-your-key-here

# 3. 启用 Skill
python .claude/scripts/win/python/skillconfig_enable.py perplexity-search

# 4. 验证配置
python .claude/scripts/win/python/skillconfig_validate.py
```

### 工作流 2: 临时禁用 Skill

```bash
# 1. 禁用 Skill (保留 API 密钥)
python .claude/scripts/win/python/skillconfig_disable.py perplexity-search

# 2. 稍后重新启用 (无需重新配置 API 密钥)
python .claude/scripts/win/python/skillconfig_enable.py perplexity-search
```

## 文件和目录结构

```
.claude/
├── skills/                          # Skills 目录
│   ├── docs-seeker/
│   │   └── SKILL.md                 # 启用状态
│   ├── perplexity-search/
│   │   └── (DISABLED)SKILL.md       # 禁用状态
│   └── ...
└── scripts/win/python/              # 管理脚本
    ├── skillconfig_list.py
    ├── skillconfig_enable.py
    ├── skillconfig_disable.py
    ├── skillconfig_update.py
    └── skillconfig_validate.py

.elecspecify/
└── memory/
    └── skill_config.json            # Skills 配置文件 (权限 0600)
```

## skill_config.json 结构

```json
{
  "version": "0.2.0",
  "platform": "claude",
  "skills": {
    "information_retrieval": {
      "docs-seeker": {
        "enabled": true,
        "requires_api": false,
        "description": "搜索和定位项目文档、技术规格书、数据手册"
      },
      "perplexity-search": {
        "enabled": false,
        "requires_api": true,
        "api_key": "",
        "description": "使用 Perplexity AI 进行深度网络搜索和研究"
      }
    }
  }
}
```

## 注意事项

### API 密钥安全

- **绝不在 SKILL.md 中包含 API 密钥**
- API 密钥仅存储在 `skill_config.json` (权限 0600)
- Python 脚本从 JSON 读取密钥,在服务端完成 API 调用
- 返回结构化数据给 LLM,**密钥永不暴露**

### 幂等性

所有命令都是幂等的:
- 重复启用已启用的 Skill: 输出 "已启用 (幂等操作)",退出码 0
- 重复禁用已禁用的 Skill: 输出 "已禁用 (幂等操作)",退出码 0
- 重复配置相同的 API 密钥: 正常更新,退出码 0

### 错误处理

所有脚本提供清晰的错误信息和合理的退出码:
- **退出码 0**: 成功
- **退出码 1**: 文件不存在或 Skill 不存在
- **退出码 2**: 权限问题
- **退出码 3**: 验证失败 (仅 update 命令,已回滚)
- **退出码 4**: JSON 格式错误
- **退出码 5**: 其他未知错误

### 文件锁定

如果文件被占用 (如被编辑器打开),脚本会返回明确错误:
```
错误: 无法重命名文件 (文件被占用或权限不足): SKILL.md → (DISABLED)SKILL.md
```

解决方法: 关闭占用文件的程序,然后重试

## 相关文档

- **Skills 库说明**: `.claude/skills/README.md`
- **skill_config.json 字段详解**: `.claude/skills/README.md` 中的 "skill_config.json 配置字段说明" 部分
- **ElecSpeckit 项目宪法**: `.elecspecify/constitution.md`
- **Skills 集成指南**: 每个 Skill 的 `SKILL.md` 文件中的 "ElecSpeckit 集成指南" 部分

## 故障排除

### 问题 1: "配置文件不存在"

**原因**: 项目未初始化或初始化不完整

**解决**:
```bash
# 重新初始化项目
elecspeckit init
```

### 问题 2: "Skill 目录不存在"

**原因**: Skills 未正确部署

**解决**:
```bash
# 重新初始化部署 Skills
elecspeckit init --upgrade
```

### 问题 3: "验证失败: enabled: true 但文件名为 (DISABLED)SKILL.md"

**原因**: 配置与文件名不一致 (可能手动修改了文件)

**解决**:
```bash
# 方法 1: 使用 disable 再 enable 修复
python .claude/scripts/win/python/skillconfig_disable.py <skill-name>
python .claude/scripts/win/python/skillconfig_enable.py <skill-name>

# 方法 2: 手动重命名文件
mv .claude/skills/<skill-name>/(DISABLED)SKILL.md .claude/skills/<skill-name>/SKILL.md
```

### 问题 4: "API 密钥已过期或无效"

**原因**: 外部 API 密钥过期

**解决**:
```bash
# 重新配置 API 密钥
python .claude/scripts/win/python/skillconfig_update.py <skill-name> --api-key <new-key>
```

---

**版本**: v0.2.0
**维护者**: ElecSpeckit CLI
**许可证**: Apache License 2.0
