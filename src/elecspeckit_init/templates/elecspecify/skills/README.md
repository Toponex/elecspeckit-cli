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

## skill_config.json 配置字段说明

每个 Skill 在 `skill_config.json` 中的配置项包含以下字段：

### 字段详解

| 字段名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `enabled` | boolean | 是 | 表示 Skill 是否启用。默认 `true`，需要 API 的 Skill 默认 `false` |
| `requires_api` | boolean | 是 | 表示是否需要外部 API 密钥 |
| `api_key` | string | 可选 | 存储 API 密钥，仅供 Python 脚本读取，**绝不暴露给 LLM** |
| `description` | string | 是 | 简要说明 Skill 用途（中文），**只读字段，用户不应修改** |

### 配置示例

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
        "description": "使用 Perplexity AI 进行高级搜索"
      }
    }
  }
}
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
