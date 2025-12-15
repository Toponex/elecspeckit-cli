---
name: "perplexity-search"
description: "使用 Perplexity AI 进行高级搜索"
requires_api: true
---

# perplexity-search Skill

## 概述

使用 Perplexity AI 进行高级搜索。

## 依赖

### Python 库

```bash
pip install requests
```

**说明**: 需要 `requests` 库访问 Perplexity API。

### API 密钥配置

需要配置 Perplexity API 密钥：

```bash
# 使用 skillconfig 命令配置
/elecspeckit.skillconfig update perplexity-search --api-key YOUR_API_KEY
```

## 使用

### 基本用法

```
使用 perplexity-search 搜索最新的 GaN 功率器件技术
```



## ElecSpeckit 集成指南

### 在 ElecSpeckit 工作流中使用

**场景**: 信息检索类相关任务

适用于以下 ElecSpeckit 命令:
-  - 架构设计阶段
-  - 规格编写阶段  
-  - 任务拆解阶段

## 示例

### 示例 1



---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
