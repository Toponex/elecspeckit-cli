---
description: "管理 ElecSpeckit Claude Skills 配置 - 配置 API 密钥和查看 Skills 状态"
---

# /elecspeckit.skillconfig - Skills 配置管理

管理 ElecSpecKit Claude Skills 的 API 密钥配置。

## 概述

ElecSpecKit v0.2.1 提供了 15 个专业 Skills 增强硬件设计工作流，涵盖信息检索、文档生成、数据分析、嵌入式开发、元器件采购等领域。

## 重要提示

**⚠️ 项目级配置**：Skills 配置文件位于**当前项目目录**下，而不是用户主目录：
- 正确位置：`F:\YourProject\.elecspecify\memory\skill_config.json`
- 错误位置：`C:\Users\YourName\.elecspecify\...` ❌

使用本命令时，**请确保在 ElecSpecKit 项目目录中运行**。脚本会自动向上查找包含 `.elecspecify/` 目录的项目根目录。

## 可用命令

### 1. 列出所有 Skills

```bash
python .elecspecify/scripts/win/python/skillconfig_list.py
```

**输出示例**:
```
============================================================
ElecSpecKit Skills 列表 (v0.2.1)
平台: claude
============================================================

## 信息检索类 (information_retrieval)

✅ **docs-seeker**
   搜索和定位项目文档、技术规格书、数据手册

❌ **perplexity-search** [需要 API - 未配置]
   使用 Perplexity AI 进行高级搜索

...

============================================================
图例: ✅ 已启用 | ❌ 已禁用
```

### 2. 配置 API 密钥

```bash
python .elecspecify/scripts/win/python/skillconfig_update.py <skill_name> --api-key <API_KEY>
```

**示例 - 配置 Perplexity Search**:
```bash
python .elecspecify/scripts/win/python/skillconfig_update.py perplexity-search --api-key pplx-abc123xyz...
```

**输出**:
```
✅ Skill 'perplexity-search' 配置已更新
   API 密钥已设置 (长度: 42 字符)
   配置文件: F:\YourProject\.elecspecify\memory\skill_config.json
   备份文件: skill_config.json.bak.20251216-235959
```

**示例 - 配置 Mouser Component Search**:
```bash
python .elecspecify/scripts/win/python/skillconfig_update.py mouser-component-search --api-key xxx-yyy-zzz
```

**清空 API 密钥**:
```bash
python .elecspecify/scripts/win/python/skillconfig_update.py perplexity-search --api-key ""
```

### 3. 验证配置

```bash
python .elecspecify/scripts/win/python/skillconfig_validate.py
```

**输出示例 (验证通过)**:
```json
{
  "status": "valid",
  "errors": [],
  "warnings": []
}
```

**输出示例 (有问题)**:
```json
{
  "status": "invalid",
  "errors": [
    {
      "skill": "perplexity-search",
      "error": "enabled: true 但 SKILL.md 不存在"
    }
  ],
  "warnings": [
    {
      "skill": "mouser-component-search",
      "warning": "Skill 已启用且需要 API 密钥，但未配置 API 密钥"
    }
  ]
}
```

## 需要 API 密钥的 Skills

目前有 2 个 Skills 需要配置 API 密钥才能使用：

### 1. perplexity-search - Perplexity AI 搜索

**获取 API 密钥**: https://www.perplexity.ai/settings/api

**配置步骤**:
```bash
# 1. 配置 API 密钥
python .elecspecify/scripts/win/python/skillconfig_update.py perplexity-search --api-key pplx-YOUR-KEY

# 2. 验证配置
python .elecspecify/scripts/win/python/skillconfig_validate.py
```

### 2. mouser-component-search - Mouser 元器件搜索

**获取 API 密钥**: https://www.mouser.com/api-hub/

**配置步骤**:
```bash
# 1. 配置 API 密钥
python .elecspecify/scripts/win/python/skillconfig_update.py mouser-component-search --api-key YOUR-API-KEY

# 2. 验证配置
python .elecspecify/scripts/win/python/skillconfig_validate.py
```

## 在 Claude Code 中使用

当用户要求配置 API 密钥时，Claude Code 应该：

### 方法 1: 使用 Bash 工具调用脚本（推荐）

```markdown
用户：帮我配置 perplexity-search 的 API 密钥：pplx-abc123...

AI 助手步骤：
1. 使用 Bash 工具执行：
   python .elecspecify/scripts/win/python/skillconfig_update.py perplexity-search --api-key pplx-abc123...

2. 检查输出，确认成功

3. 可选：运行验证脚本
   python .elecspecify/scripts/win/python/skillconfig_validate.py
```

### 方法 2: 手动编辑（不推荐，仅作备选）

如果脚本不可用，可以手动编辑：

1. 使用 Read 工具读取 `.elecspecify/memory/skill_config.json`
2. 使用 Edit 工具更新对应 Skill 的 `api_key` 字段
3. **重要**：不要破坏 JSON 格式

**⚠️ 警告**：手动编辑容易出错，优先使用 Python 脚本。

## skill_config.json 结构示例

```json
{
  "version": "0.2.1",
  "platform": "claude",
  "skills": {
    "information_retrieval": {
      "perplexity-search": {
        "enabled": true,
        "requires_api": true,
        "api_key": "",
        "description": "使用 Perplexity AI 进行高级搜索"
      }
    },
    "component_search": {
      "mouser-component-search": {
        "enabled": false,
        "requires_api": true,
        "api_key": "",
        "description": "Mouser 元器件库存和价格查询"
      }
    }
  }
}
```

## 启用/禁用 Skills

在 v0.2.1 中，Skills 的启用/禁用通过 `enabled` 字段控制：

### 启用 Skill

```json
"mouser-component-search": {
  "enabled": true,  ← 修改为 true
  ...
}
```

### 禁用 Skill

```json
"mouser-component-search": {
  "enabled": false,  ← 修改为 false
  ...
}
```

**注意**：启用/禁用功能可以手动编辑 JSON，或等待后续版本提供专用命令。

## API 密钥安全

- **项目级存储**：API 密钥存储在项目的 `.elecspecify/memory/skill_config.json`，不是用户主目录
- **权限保护**：文件权限自动设置为 `0600`（仅所有者可读写，Windows 使用 NTFS 权限）
- **备份机制**：每次更新前自动创建带时间戳的备份（`skill_config.json.bak.YYYYMMDD-HHMMSS`）
- **原子性更新**：使用临时文件和验证机制，防止配置损坏
- **不暴露给 LLM**：Python 脚本从 JSON 读取密钥，Skill 的 `SKILL.md` 文件不包含任何 API 密钥

## 脚本功能详解

### skillconfig_list.py

**功能**：列出所有 Skills 及其配置状态

**特性**：
- 自动查找项目根目录（向上查找 `.elecspecify/` 目录）
- 按分类显示 Skills
- 显示启用状态、API 密钥配置状态
- 支持 text 和 json 两种输出格式

**退出码**：
- 0: 成功
- 1: 配置文件不存在
- 4: JSON 格式错误

### skillconfig_update.py

**功能**：安全更新 Skill 配置（主要是 API 密钥）

**特性**：
- 自动查找项目根目录
- 原子性更新机制（临时文件 → 验证 → 替换）
- 自动创建备份
- 自动调用 `skillconfig_validate.py` 验证配置
- 验证失败时自动回滚
- 设置文件权限为 0600

**退出码**：
- 0: 成功
- 1: Skill 不存在或不需要 API
- 2: 权限问题
- 3: 验证失败，已回滚
- 4: JSON 格式错误

### skillconfig_validate.py

**功能**：验证 Skills 配置一致性

**验证项**：
1. `skill_config.json` 文件格式正确
2. 配置中的每个 Skill 目录存在
3. `enabled: true` 的 Skill 有 `SKILL.md` 文件
4. 已启用且需要 API 的 Skill 是否配置了 API 密钥（警告）
5. Skills 目录中的 Skill 都在配置中（警告）

**退出码**：
- 0: 验证通过
- 1: 配置文件不存在
- 3: 验证失败
- 4: JSON 格式错误

## 15 个 Skills 清单（v0.2.1）

### 信息检索 (5)
- ✅ docs-seeker - 搜索和定位技术文档
- ✅ arxiv-search - 搜索 arXiv 学术论文
- ✅ web-research - 网络研究和信息收集
- 🔑 perplexity-search - Perplexity AI 深度搜索（需要 API）
- ✅ openalex-database - OpenAlex 学术数据库查询

### 文档生成 (3)
- ✅ architecture-diagrams - 生成架构图
- ✅ mermaid-tools - Mermaid 图表工具
- ✅ docs-write - 文档编写辅助

### 数据分析 (1)
- ✅ citation-management - 文献引用管理

### 嵌入式系统 (1)
- ✅ embedded-systems - 嵌入式系统开发

### 元器件采购 (1)
- 🔑 mouser-component-search - Mouser 元器件搜索（需要 API）

### 领域分析 (3)
- 📝 circuit-commutation-analysis - 电路换流分析（占位符）
- 📝 thermal-simulation - 热仿真（占位符）
- 📝 emc-analysis - EMC 分析（占位符）

### 元 Skill (1)
- ✅ skill-creator - Skill 创建工具

**图例**：
- ✅ 无需 API，可直接使用
- 🔑 需要配置 API 密钥
- 📝 占位符 Skill（待实现）

## 故障排除

### 问题 1: "未找到 ElecSpecKit 项目根目录"

**原因**：在错误的目录运行脚本

**解决**：
```bash
# 确保在 ElecSpecKit 项目目录中运行
cd F:\YourProject  # 包含 .elecspecify/ 目录的项目根目录
python .elecspecify/scripts/win/python/skillconfig_list.py
```

### 问题 2: "API key not configured"

**原因**：未配置 API 密钥或配置为空字符串

**解决**：使用 `skillconfig_update.py` 配置 API 密钥

### 问题 3: "Invalid API key"

**原因**：API 密钥错误或已过期

**解决**：
1. 检查 API 密钥是否正确
2. 到对应平台重新生成 API 密钥
3. 使用 `skillconfig_update.py` 更新密钥

### 问题 4: 配置被写入用户主目录

**原因**：Claude 误认为应该在用户主目录配置（错误行为）

**解决**：
1. 删除用户主目录的错误配置：`C:\Users\YourName\.elecspecify\`
2. 使用 Python 脚本配置（脚本会自动查找项目目录）
3. **不要**让 Claude 直接操作 `Path.home() / '.elecspecify'`

## 相关文档

- **Skills 使用说明**：每个 Skill 的 `SKILL.md` 文件
- **ElecSpecKit 项目宪法**：`.elecspecify/memory/constitution.md`
- **项目初始化指南**：`specs/001-elecspeckit-cli/quickstart.md`

---

**版本**：v0.2.1
**维护者**：ElecSpecKit CLI
**许可证**：Apache License 2.0
