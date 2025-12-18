# Changelog

All notable changes to ElecSpeckit CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-09

### Critical Fixes (Pre-release)

- **Windows NUL 文件删除** (build blocker): 删除了项目中的 `NUL` 文件（Windows 保留设备名），该文件导致 `python -m build` 失败并报错 `tarfile.SpecialFileError`
- **gitignore 增强**: 添加了所有 Windows 保留设备名规则（NUL、CON、PRN、AUX、COM1-9、LPT1-9）以防止这类文件再次被添加
- **移除 `-i` 简写**: 从 CLI 中完全移除 `elecspeckit -i` 简写，统一使用标准命令格式 `elecspeckit init`，确保命令结构清晰一致

### Added

#### 核心功能

- **项目初始化** (`elecspeckit init`)
  - 支持在空目录中初始化 ElecSpeckit 项目结构
  - 交互式 AI 平台选择（Claude Code 或 Qwen Code）
  - 非交互式模式 (`--platform claude/qwen`) 用于 CI/CD 自动化
  - 自动生成 `.elecspecify/`、`.claude/commands/` 或 `.qwen/commands/` 目录结构
  - Git 仓库自动初始化（可通过 `--no-git` 跳过）

- **环境检查** (`elecspeckit check`)
  - 以树形结构展示必需工具（uv）、可选工具（git、claude、qwen）和脚本环境（PowerShell/bash）的可用性
  - 支持 JSON 输出格式 (`--json`) 用于脚本集成
  - 显示工具版本号和安装路径
  - 提供缺失工具的安装建议

- **项目升级** (`elecspeckit init` 在已有项目中)
  - 自动检测已存在的平台配置，无需重新选择
  - 智能更新工作流模板（`.claude/commands/` 或 `.qwen/commands/`）
  - 更新辅助脚本（`.elecspecify/scripts/`）和文档模板（`.elecspecify/templates/`）
  - 自动生成带时间戳的备份文件（`.bak.YYYYMMDD-HHMMSS`）
  - 保护用户内容（`specs/` 目录和 `constitution.md` 不被覆盖）
  - 内容相同的文件自动跳过，不创建不必要的备份

- **宪法重置** (`elecspeckit init --reset`)
  - 将 `constitution.md` 恢复到官方模板初始状态
  - 生成带时间戳的备份文件
  - 首次初始化时静默忽略 `--reset` 标志
  - 不影响其他文件的升级逻辑

#### 工作流命令模板（15个）

为 Claude Code 和 Qwen Code 生成完整的工作流命令模板：

**项目配置命令**:
- `/elecspeckit.constitution` - 维护项目宪法（设计原则和约束）
- `/elecspeckit.kbconfig` - 配置外部知识源（标准、公司知识库、参考设计、在线知识库）

**规格与架构命令（P1 核心工作流）**:
- `/elecspeckit.specify <功能描述>` - 生成和更新特性规格（spec.md）
- `/elecspeckit.plan` - 生成架构设计（plan.md、research.md、data-model.md）

**任务与文档命令**:
- `/elecspeckit.tasks` - 生成依赖有序的任务拆分（tasks.md）
- `/elecspeckit.docs` - 生成多角色文档视图（HW/BOM/Test/FA/PM/Datasheet/KB）

**质量辅助命令（P3）**:
- `/elecspeckit.clarify` - 澄清规格模糊点，以选择题形式批量提问
- `/elecspeckit.checklist` - 生成质量检查清单
- `/elecspeckit.analyze` - 分析文档一致性（spec/plan/tasks/docs 与宪法的一致性）

#### 辅助脚本

**知识源管理脚本** (`packages/elecspeckit-cli/src/elecspeckit_init/templates/{claude,qwen}/scripts/win/python/`):
- `kbconfig_validate.py` - 验证 knowledge-sources.json 的有效性（JSON 格式、字段完整性、占位符一致性）
- `kbconfig_add.py` - 添加新知识源条目到 4 类别（standards/company_kb/reference_designs/web）
- `kbconfig_update.py` - 更新现有条目字段（替换占位符、启用/禁用条目）
- `kbconfig_list.py` - 按类别和状态展示所有知识源条目
- `kbconfig_delete.py` - 按 ID 删除知识源条目

**知识源查询脚本**:
- `query_metaso.py` - 查询 Metaso 学术搜索 API（POST 请求，支持 ENV 变量解析）
- `query_volces.py` - 查询 Volces 知识库 API（POST 请求）
- `query_standards.py` - 查询本地标准文件（按 standard_number/title/abstract 搜索）
- `query_reference_design.py` - 查询本地参考设计文件（按 name/vendor/parameters 搜索）

#### 文档模板

- `spec-template.md` - 特性规格模板（用户故事、验收标准、功能需求、非功能需求、Clarifications）
- `plan-template.md` - 实施计划模板（架构设计、模块划分、接口定义）
- `tasks-template.md` - 任务拆分模板（依赖有序、角色标记 `[VIEW:XXX]`、类型标记 `[MANUAL]`/`[AUTO]`）
- `research-template.md` - Phase 0 研究模板（研究问题列表、决策记录）
- `data-model-template.md` - 数据模型模板（功能模块实体、接口参数、关系图）
- `checklist-template.md` - 质量检查清单模板
- `doc-*-template.md` - 7 个角色视图文档模板（HW/BOM/Test/FA/PM/Datasheet/KB）

#### 核心配置文件

- `constitution.md` - 项目宪法初始模板（包含项目范围、库优先、测试驱动、可观察性、中文本地化等章节）
- `knowledge-sources.json` - 外部知识源配置（预置 Metaso 和 Volces 两个 web 知识库条目，占位符为 `{{PLACEHOLDER:...}}` 格式）

#### 技术特性

- **中文优先的用户界面**: 所有 CLI 提示和错误信息以中文为主，技术术语保持英文
- **Windows UTF-8 编码支持**: 修复 Windows GBK 编码导致的 UnicodeEncodeError 崩溃问题
- **交互式平台选择**: 使用方向键导航、Enter 确认、Esc 取消的友好界面
- **多平台冲突检测**: 检测并拒绝在同一项目中同时存在 `.claude/` 和 `.qwen/` 目录（v1.x 单平台架构约束）
- **智能备份策略**: 仅对内容变化的文件创建带时间戳的备份，内容相同的文件自动跳过
- **幂等性设计**: 升级操作可以安全地重复执行，不会破坏用户自定义内容

#### 测试覆盖

- 362 个自动化测试（单元测试、集成测试、契约测试）
- 核心功能测试通过率 80-85%（264+ tests passing）
- 覆盖初始化、升级、重置、环境检查、知识源管理等所有核心场景

#### 开发工具

- **代码质量工具**: ruff（快速 Python 检查器）、black（代码格式化）
- **测试框架**: pytest
- **构建系统**: hatchling
- **依赖管理**: uv（推荐）或 pip

### Changed

- 许可证从 MIT 更改为 Apache License 2.0
- 作者信息更新为 Yongkai Li
- **改进初始化完成提示**：将"下一步操作"改为"使用说明"，提供完整的 ElecSpeckit 工作流程指南（kbconfig → constitution → specify → plan → tasks → docs），帮助新用户快速上手

### Fixed

- **CLI 入口点错误修复** (T081): 修复 `TypeError: main() missing 1 required positional argument: 'ctx'`（pyproject.toml entry_points 从 `main` 改为 `app`）
- **ChangeSummary 迭代错误修复** (T081): 修复 `'ChangeSummary' object is not iterable` 错误（访问 `.changes` 属性）
- **Windows UTF-8 编码修复** (T081): 强制 UTF-8 输出避免 GBK 编码崩溃（sys.stdout.reconfigure + subprocess encoding 参数）
- **交互式测试超时修复** (T081): 添加 `--platform` 参数支持非交互式初始化，解决测试挂起问题

### Known Issues

1. **Git 提交信息不准确**: CLI 输出显示"Git 仓库已初始化并创建初始提交"，但实际只执行了 `git init`，没有创建提交。用户需要手动执行首次提交。

2. **文档命令模板**: 实际生成的是一个通用的 `/elecspeckit.docs` 命令，而 README 描述了 7 个独立文档生成命令（`/elecspeckit.doc-hw`、`/elecspeckit.doc-bom` 等）。功能上通用命令应该可以达到类似效果，但与文档描述存在不一致。

### Documentation

- **README.md**: 全面重写，增加"为什么需要 ElecSpeckit？"、"核心概念"、"工作流命令详解"、"实际使用场景示例"等章节，详细说明每个命令的用途、典型场景、工作流和输入输出
- **LICENSE**: 添加 Apache License 2.0 完整文本（Copyright 2025 Yongkai Li）
- **quickstart.md**: 包含完整的安装、初始化、使用示例和 FAQ

### Internal Changes

- 清理历史遗留文件（删除开发仓库中的 `.claude/` 目录和旧命名约定文件）
- 更新 `.gitignore` 排除 `.claude/` 和 `.qwen/` 目录
- 验证所有 41 个模板文件不包含开发仓库内部路径引用
- 代码格式化：修复 62 个 ruff 问题，格式化 24 个文件

### Development Status

- **版本**: 0.1.0（开发预览版）
- **Python 支持**: >=3.11
- **平台支持**: Windows（主要）、Linux、macOS
- **AI 平台集成**: Claude Code、Qwen Code

---

## [0.2.1] - 2025-12-17

### Added - Skills 完整实现

#### Claude Code Skills 生态系统（15个Skills）

**🎯 Type 1: 标准 Skills（11个，无需 API 密钥）**:
- `docs-seeker`: 技术文档和数据手册搜索
- `arxiv-search`: arXiv 学术论文搜索（Python 脚本集成）
- `web-research`: 网络技术调研和资源查找
- `perplexity-search`: Perplexity AI 搜索（需 API 密钥，包含友好错误提示）
- `openalex-database`: OpenAlex 学术数据库查询（Python 脚本集成）
- `architecture-diagrams`: 系统架构图生成和可视化
- `mermaid-tools`: Mermaid 图表创建和渲染
- `docs-write`: 技术文档撰写辅助
- `citation-management`: 文献引用管理（IEEE/APA/GB 格式）
- `embedded-systems`: 嵌入式系统开发最佳实践指导
- `skill-creator`: 自定义 Skill 创建指南（整合 3 个源实现）

**🔌 Type 2: API 集成 Skills（1个）**:
- `mouser-component-search`: Mouser Electronics 元器件库存和价格查询
  - 实时库存检查
  - 价格和数据手册链接
  - 交货期查询
  - 友好的 API 密钥错误处理（未配置时返回英文错误和配置指南）

**🚧 Type 3: 占位 Skills（3个，预留 v0.2.2+ 扩展）**:
- `circuit-commutation-analysis`: 电路换流分析（占位）
- `thermal-simulation`: 热仿真（占位）
- `emc-analysis`: EMC 分析（占位）

#### Skills 配置和管理

**新增 `/elecspeckit.skillconfig` 命令**：
- `/elecspeckit.skillconfig list` - 查看所有 Skills 状态和配置
- `/elecspeckit.skillconfig update <skill> --api-key <key>` - 配置 API 密钥（同步更新 skill_config.json 和 SKILL.md frontmatter，无需重启 Claude Code）
- `/elecspeckit.skillconfig enable <skill>` - 启用 Skill（重命名 (DISABLED)SKILL.md → SKILL.md）
- `/elecspeckit.skillconfig disable <skill>` - 禁用 Skill（重命名 SKILL.md → (DISABLED)SKILL.md，保留 API 密钥配置）
- `/elecspeckit.skillconfig validate` - 验证配置文件完整性

**Skills 配置 Python 脚本**（5个）：
- `skillconfig_list.py` - 按类别展示所有 Skills 状态
- `skillconfig_update.py` - 安全更新 API 密钥（原子性更新、自动备份、同步 frontmatter）
- `skillconfig_enable.py` - 启用 Skills（文件重命名 + JSON 配置更新）
- `skillconfig_disable.py` - 禁用 Skills（保留 API 密钥配置）
- `skillconfig_validate.py` - 验证配置文件格式和完整性

**项目根目录自动发现**：所有 skillconfig_*.py 脚本实现 `find_project_root()` 函数，从当前目录向上查找 `.elecspecify/` 标记，防止错误访问用户主目录。

#### 双语文档支持（中英文）

- 所有 15 个 Skills 提供完整双语文档：`SKILL.md`（英文）+ `SKILL_ZH.md`（中文）
- 技术术语保持英文一致性，用户界面和说明全中文翻译
- 每个文档 ≥ 200 行，包含 Overview、Usage、Configuration、Examples、Troubleshooting 等章节

#### API 密钥同步机制

- **双重同步**：`skillconfig_update.py` 同时更新 `skill_config.json` 和 `SKILL.md` frontmatter
- **无需重启**：API 密钥配置后 Claude Code 立即识别（YAML frontmatter 更新）
- **正则解析**：使用 `update_skill_frontmatter()` 函数安全解析和更新 YAML frontmatter

#### 模板和命令更新

- `spec-template.md` 和 `plan-template.md` 添加 Skills 使用提示（替代已删除的 query_*.py 脚本）
- `research-template.md` 更新为 Skills 风格（自然语言请求替代脚本调用）
- 删除 8 个已废弃的 query_*.py 脚本（metaso、volces、standards、reference_design）
- 移除 `/elecspeckit.constitution` 命令中的 knowledge-source 检查逻辑

### Changed - 版本管理改进

#### 版本号一致性修复

**问题**：pip install 显示 `elecspeckit_cli-0.1.0` 但 `elecspeckit --version` 显示 `0.2.1`

**修复**：
- `pyproject.toml`: `version = "0.1.0"` → `"0.2.1"`（单一真相来源）
- `__init__.py`: 硬编码版本 → 动态导入 `version("elecspeckit-cli")`
- 安装后验证：pip 输出和运行时版本号完全一致

**宪法更新 v2.3.0**：
- 新增"版本号一致性要求"章节
- 定义版本号管理规范（pyproject.toml 为唯一真相来源）
- 建立版本更新流程（修改 pyproject.toml → 重新安装 → 验证一致性）

### Removed - Skills 清理

删除不再支持的 8 个 Skills：
- `docx` - 文档处理移至 Anthropic 官方 Skills
- `pdf` - 同上
- `xlsx` - 同上
- `pptx` - 同上
- `hardware-data-analysis` - 范围外功能
- `hardware-protocols` - 范围外功能
- `esp32-embedded-dev` - 合并到 embedded-systems
- `embedded-best-practices` - 合并到 embedded-systems

删除 8 个已废弃的查询脚本：
- `query_metaso.py` - 替换为 Skills
- `query_volces.py` - 替换为 Skills
- `query_standards.py` - 替换为 Skills
- `query_reference_design.py` - 替换为 Skills

### Fixed

#### 核心修复（用户反馈）

**问题 1: 缺少 /elecspeckit.skillconfig 命令**
- **原因**: `elecspeckit.skillconfig` 未包含在 `COMMAND_BASENAMES` 列表中
- **修复**:
  - 将命令添加到 `template_manager.py` 的 `COMMAND_BASENAMES`
  - 简化命令模板为 Read + Edit 工具模式（AI 直接编辑 JSON）
  - 添加详细配置步骤和安全指南
  - 列出所有 15 个 Skills 及其分类
- **验证**: `elecspeckit init` 后 `.claude/commands/elecspeckit.skillconfig.md` 正确部署
- **文件**: `template_manager.py`, `templates/claude/elecspeckit.skillconfig.md`

**问题 2: /elecspeckit.constitution 中过时的 knowledge-source 判断**
- **验证结果**: 已在之前更新中解决，`elecspeckit.constitution.md` 不包含任何 knowledge-source 相关内容
- **无需修复**

**问题 3: Spec/Plan 模板缺少 Skills 使用指南**
- **修复**:
  - `spec-template.md`: 添加 Skills 使用提示注释（信息检索、文档生成、领域分析类 Skills）
  - `plan-template.md`: 添加更详细的 Skills 分类指南（研究与分析、元器件选型、架构设计、领域分析）
  - 提示在 research.md 中记录 Skills 使用过程
- **Skills 清单**: docs-seeker, arxiv-search, web-research, openalex-database, architecture-diagrams, mermaid-tools, docs-write, mouser-component-search, embedded-systems, circuit-commutation-analysis, thermal-simulation, emc-analysis
- **文件**: `spec-template.md`, `plan-template.md`

**问题 4: 空的 powershell 目录不应该被创建**
- **原因**: `_create_elecspecify_structure()` 硬编码创建 `scripts/powershell/` 目录
- **修复**:
  - 删除硬编码目录创建逻辑
  - 让 `copy_directory_tree()` 根据实际模板内容自动创建目录结构
- **验证**: `find .elecspecify/scripts -type d` 不再包含 powershell 目录
- **文件**: `template_manager.py`

#### 额外修复（Skills 部署）

**Skills 清单不一致**
- **原因**: `REQUIRED_SKILLS` 列表包含 23 个 Skills（v0.2.0 旧清单），但 Phase 4 US2 已删除 8 个
- **修复**: 更新为 15 个 Skills，删除 docx, pdf, xlsx, pptx, hardware-data-analysis, hardware-protocols, esp32-embedded-dev, embedded-best-practices
- **文件**: `template_manager.py` (L325-357)

**UTF-8 编码错误**
- **原因**: `copy_directory_tree()` 对所有文件使用 `read_text(encoding="utf-8")`，某些 Skills 包含非 UTF-8 文件（图片、二进制文件）
- **修复**: 改用 `shutil.copy2()` 进行二进制文件复制，支持文本和二进制文件，保留文件元数据
- **文件**: `fs_utils.py` (L167)

**版本号不一致**
- **修复**: `__init__.py` 版本号从 0.1.0 更新到 0.2.1

#### 其他安全修复

- **安全问题**：防止 Claude Code 访问用户主目录（`C:\Users\<user>\.elecspecify\`）而非项目目录
- **API 重启问题**：修复 API 密钥配置后需要重启 Claude Code 才能生效的问题
- **配置一致性**：修复 mouser-component-search 默认状态不一致问题（enabled: false → true）

### Testing

- 手动测试通过率：100%（参考 `specs/003-skills-implementation-v021/TEST_CHECKLIST.md`）
- 所有 15 个 Skills 在 Claude Code 中验证通过
- 所有 4 个包含 Python 脚本的 Skills（arxiv-search、perplexity-search、openalex-database、mouser-component-search）脚本可执行性测试通过
- 所有 2 个需要 API 密钥的 Skills（perplexity-search、mouser-component-search）错误处理测试通过

### Documentation

- 添加 `TEST_CHECKLIST.md` - 15 个 Skills 的详细测试清单
- 添加 `QUICK_TEST_GUIDE.md` - 5 分钟快速验证指南
- 更新 `.specify/memory/constitution.md` → v2.3.0（版本管理规范）

### Breaking Changes

**无重大破坏性变更** - v0.2.1 向后兼容 v0.1.0 项目结构

**注意事项**：
- 删除的 8 个 Skills（docx、pdf 等）不再可用，请使用 Anthropic 官方 Skills 或 embedded-systems Skill
- 删除的 query_*.py 脚本已被 Skills 替代，请使用自然语言请求相应 Skills

### Known Issues

1. **Type 3 占位 Skills**：circuit-commutation-analysis、thermal-simulation、emc-analysis 仅为占位实现，功能未实现，计划在 v0.2.2+ 实现
2. **Skills 完整性**：v0.2.1 专注于 Claude Code 平台，Qwen Code Skills 支持有限
3. **API 密钥加密**：当前版本 API 密钥存储在 skill_config.json 中未加密（权限 0600），v0.3.0 将实现跨平台加密存储（Windows DPAPI, Linux Keyring, macOS Keychain）
4. **异常场景覆盖**：以下边缘情况尚未完全覆盖：
   - 磁盘空间不足时的 Skills 部署失败处理
   - Python 依赖缺失时的友好错误提示
   - Mouser API 返回大量结果（100+ 元器件）时的分页处理
   - 非 ASCII 字符文件路径的完整处理（Windows GBK 环境）
5. **跨平台限制**：
   - Windows GBK 编码环境下中文显示已部分测试，可能存在特殊场景乱码
   - Linux/macOS 文件权限设置已实现但未在所有发行版测试
6. **性能基准缺失**：v0.2.1 定义了性能目标（60s SSD, 120s HDD），但缺少 v0.2.0 基准对比数据

### Internal Changes

- 实现 (DISABLED)SKILL.md 文件重命名机制（真正控制 Claude Code 加载）
- skill_config.json 的 enabled 字段改为元数据（实际控制靠文件重命名）
- 原子性配置更新机制（临时文件 → 验证 → 替换 + 自动备份）

---

## [Unreleased]

### Planned

- Type 3 Skills 完整实现（circuit-commutation-analysis、thermal-simulation、emc-analysis）
- Qwen Code Skills 生态系统支持
- 性能优化（Skills 部署并行化）
- 更多硬件领域专用 Skills
- Skills 单元测试和集成测试自动化
- **Skills 图形化管理界面**（Web UI 或 TUI）- 可视化配置 API 密钥、启用/禁用 Skills、查看 Skills 状态

---

[0.2.1]: https://github.com/Toponex/elecspeckit-cli/releases/tag/v0.2.1
[0.1.0]: https://github.com/Toponex/elecspeckit-cli/releases/tag/v0.1.0
