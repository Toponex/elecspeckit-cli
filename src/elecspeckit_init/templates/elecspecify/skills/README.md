# ElecSpeckit Claude Skills 库

本目录包含 ElecSpeckit 项目的所有 Claude Skills 实现。Skills 是增强 Claude Code 功能的专业工具，专为硬件/电子项目设计。

## Skills 分类

### 1. 信息检索类 (Information Retrieval) - 5个

- **docs-seeker**: 搜索和定位项目文档、技术规格书、数据手册
- **arxiv-search**: 搜索学术论文和研究文献
- **web-research**: 执行结构化网络研究任务
- **perplexity-search**: 使用 Perplexity AI 进行高级搜索（需要 API）
- **openalex-database**: 查询 OpenAlex 学术数据库

### 2. 文档生成与可视化类 (Document Generation) - 7个

- **docx**: 生成 Microsoft Word 文档
- **pdf**: 生成 PDF 文档
- **xlsx**: 生成和编辑 Excel 电子表格
- **pptx**: 生成 PowerPoint 演示文稿
- **architecture-diagrams**: 生成系统架构图和技术图表
- **mermaid-tools**: 创建 Mermaid 流程图和序列图
- **docs-write**: 编写和格式化技术文档

### 3. 数据分析类 (Data Analysis) - 2个

- **hardware-data-analysis**: 分析硬件测试数据和性能指标
- **citation-management**: 管理文献引用和参考文献

### 4. 嵌入式系统类 (Embedded Systems) - 4个

- **embedded-systems**: 嵌入式系统开发指导和最佳实践
- **hardware-protocols**: 硬件通信协议支持 (I2C, SPI, UART, CAN等)
- **esp32-embedded-dev**: ESP32 开发和调试支持
- **embedded-best-practices**: 嵌入式开发最佳实践和设计模式

### 5. 元器件采购类 (Component Search) - 1个

- **mouser-component-search**: 搜索 Mouser 电子元器件库存和价格（需要 API）

### 6. 领域分析类 (Domain Analysis) - 3个

- **circuit-commutation-analysis**: 电路拓扑和换流分析（占位实现）
- **thermal-simulation**: 热仿真和散热设计（占位实现）
- **emc-analysis**: 电磁兼容性分析和设计指导（占位实现）

### 7. 元 Skill (Meta) - 1个

- **skill-creator**: 创建和管理自定义 Claude Skills

## skill_config.json 配置字段说明 (详细)

Skills 的配置信息存储在 `.elecspecify/memory/skill_config.json` 文件中。该文件控制 Skills 的启用状态、API 密钥等配置。

### 配置文件整体结构

```json
{
  "version": "0.2.0",
  "platform": "claude",
  "skills": {
    "<category>": {
      "<skill-name>": {
        "enabled": boolean,
        "requires_api": boolean,
        "api_key": "string (可选)",
        "description": "string (中文)"
      }
    }
  }
}
```

### 字段详细说明

#### `enabled` (布尔值,必需)

- **含义**: 表示该 Skill 是否启用
- **数据类型**: `boolean` (`true` 或 `false`)
- **默认值**:
  - 不需要 API 的 Skills: `true`
  - 需要 API 密钥的 Skills: `false` (用户配置密钥后可手动启用)
- **作用**: Claude Code 只加载 `enabled: true` 的 Skills。禁用的 Skill 对应的 SKILL.md 文件会被重命名为 `(DISABLED)SKILL.md`
- **修改方式**:
  - 使用命令: `/elecspeckit.skillconfig enable <skill-name>` 或 `/elecspeckit.skillconfig disable <skill-name>`
  - 不推荐手动编辑 JSON 文件
- **示例**:
  ```json
  "enabled": true   // Skill 已启用，Claude Code 可调用
  "enabled": false  // Skill 已禁用，Claude Code 跳过
  ```

#### `requires_api` (布尔值,必需)

- **含义**: 表示该 Skill 是否需要外部 API 密钥才能正常工作
- **数据类型**: `boolean` (`true` 或 `false`)
- **作用**:
  - 初始化时,`requires_api: true` 的 Skills 默认 `enabled: false`
  - 在 `/elecspeckit.skillconfig list` 输出中提示用户配置 API 密钥
  - 决定是否显示 `api_key` 字段
- **字段来源**: 从 SKILL.md 的 YAML front matter `requires_api` 字段自动提取
- **用户操作**: **只读字段,用户不应修改**
- **示例**:
  ```json
  "requires_api": false  // 无需 API，直接使用
  "requires_api": true   // 需要配置 API 密钥后才能使用
  ```

#### `api_key` (字符串,可选)

- **含义**: 存储外部 API 的访问密钥,**仅供 Python 脚本读取,绝不暴露给 LLM**
- **数据类型**: `string`
- **默认值**: 空字符串 `""` (未配置时)
- **作用**:
  - Python 脚本从此字段读取密钥
  - 脚本在服务端完成 API 调用,返回结构化数据给 LLM
  - LLM 永远不会看到原始 API 密钥
- **安全机制**:
  - `skill_config.json` 文件权限自动设置为 `0600` (Linux/macOS) 或等效权限 (Windows)
  - 仅文件所有者可读写
  - **绝不在 SKILL.md 或 LLM 提示中包含或引用**
- **修改方式**:
  - 使用命令: `/elecspeckit.skillconfig update <skill-name> --api-key YOUR_KEY`
  - 不推荐手动编辑 JSON 文件 (可能破坏文件权限)
- **何时出现**: 仅当 `requires_api: true` 时此字段才存在
- **示例**:
  ```json
  "api_key": ""                           // 未配置
  "api_key": "pplx-abc123xyz..."          // 已配置 Perplexity API 密钥
  "api_key": "12345678-abcd-ef90-..."     // 已配置 Mouser API 密钥
  ```

#### `description` (字符串,必需,只读)

- **含义**: Skill 的简要功能说明,使用中文
- **数据类型**: `string`
- **字段来源**: 从 SKILL.md 的 YAML front matter `description` 字段自动提取
- **作用**:
  - 帮助用户快速理解 Skill 用途
  - 在 `/elecspeckit.skillconfig list` 输出中显示
  - 作为 Skills 目录的"目录"信息
- **用户操作**: **只读字段,用户不应手动修改**。如需修改,应编辑对应的 SKILL.md 文件
- **格式规范**:
  - 使用中文
  - 简洁明了 (建议 10-30 字)
  - 技术术语可保留英文 (如 "Perplexity AI", "Mouser API")
- **示例**:
  ```json
  "description": "搜索和定位项目文档、技术规格书、数据手册"
  "description": "使用 Perplexity AI 进行深度网络搜索和研究"
  "description": "Mouser 电子元器件搜索和参数查询"
  ```

### 完整配置示例

#### 示例 1: 无需 API 的 Skill (默认启用)

```json
{
  "skills": {
    "information_retrieval": {
      "docs-seeker": {
        "enabled": true,
        "requires_api": false,
        "description": "搜索和定位项目文档、技术规格书、数据手册"
      }
    }
  }
}
```

**说明**:
- `enabled: true` → Skill 已启用,Claude Code 可直接调用
- `requires_api: false` → 无需 API 密钥
- 无 `api_key` 字段 (因为不需要)

#### 示例 2: 需要 API 的 Skill (未配置密钥)

```json
{
  "skills": {
    "information_retrieval": {
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

**说明**:
- `enabled: false` → Skill 默认禁用 (因为缺少 API 密钥)
- `requires_api: true` → 需要配置 API 密钥
- `api_key: ""` → 尚未配置
- 用户需要先配置密钥,再启用 Skill

#### 示例 3: 需要 API 的 Skill (已配置密钥并启用)

```json
{
  "skills": {
    "information_retrieval": {
      "perplexity-search": {
        "enabled": true,
        "requires_api": true,
        "api_key": "pplx-abc123xyz...",
        "description": "使用 Perplexity AI 进行深度网络搜索和研究"
      }
    }
  }
}
```

**说明**:
- `enabled: true` → Skill 已启用
- `api_key: "pplx-..."` → API 密钥已配置
- 现在 Skill 可以正常工作

### 配置操作工作流

#### 工作流 1: 启用无需 API 的 Skill

```bash
# 查看状态
/elecspeckit.skillconfig list

# 如果 Skill 已禁用,直接启用
/elecspeckit.skillconfig enable docs-seeker
```

#### 工作流 2: 启用需要 API 的 Skill

```bash
# 1. 查看状态 (通常显示 enabled: false, api_key: "")
/elecspeckit.skillconfig list

# 2. 配置 API 密钥
/elecspeckit.skillconfig update perplexity-search --api-key pplx-your-key-here

# 3. 启用 Skill
/elecspeckit.skillconfig enable perplexity-search

# 4. 验证配置
/elecspeckit.skillconfig validate
```

#### 工作流 3: 禁用 Skill

```bash
# 禁用 Skill (保留配置)
/elecspeckit.skillconfig disable perplexity-search

# 此时 enabled: false, 但 api_key 仍保留
# 下次启用时无需重新配置密钥
```

### 使用指引

1. **启用/禁用 Skill**: 使用 `/elecspeckit.skillconfig enable/disable <skill-name>` 命令
2. **配置 API 密钥**: 使用 `/elecspeckit.skillconfig update <skill-name> --api-key YOUR_KEY` 命令
3. **查看所有 Skills**: 使用 `/elecspeckit.skillconfig list` 命令
4. **验证配置**: 使用 `/elecspeckit.skillconfig validate` 命令

## Skill 目录结构

每个 Skill 目录包含：

```
<skill-name>/
├── SKILL.md              # Skill 说明文档（YAML front matter + Markdown）
├── <script>.py           # Python 脚本实现（如有）
└── references/           # 参考资料目录（可选）
    └── <reference-files>
```

### SKILL.md 格式

```markdown
---
name: "Skill 名称"
description: "Skill 简要说明"
requires_api: false
---

## 概述

Skill 的详细介绍...

## 依赖

- Python 库依赖
- 系统工具依赖
- API 密钥配置

## 使用

如何使用此 Skill...

## ElecSpeckit 集成指南

在 ElecSpeckit 工作流中的使用场景...
```

## 安全注意事项

- **API 密钥保护**: `skill_config.json` 文件权限设置为 `0600`（仅文件所有者可读写）
- **密钥隔离**: Python 脚本从 `skill_config.json` 读取 API 密钥，绝不暴露给 LLM
- **备份策略**: 升级时自动备份旧的 Skills 目录到 `.elecspecify/backup/skills.bak.YYYYMMDD-HHMMSS/`

## 开发自定义 Skill

使用 `skill-creator` Skill 创建自定义硬件专用 Skills：

```
在 Claude Code 中调用 skill-creator，按照引导创建新 Skill
```

---

**版本**: v0.2.0
**生成时间**: ElecSpeckit CLI 自动生成
**许可证**: Apache License 2.0
