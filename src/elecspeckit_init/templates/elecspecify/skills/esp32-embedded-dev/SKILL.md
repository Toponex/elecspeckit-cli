---
name: "esp32-embedded-dev"
description: "ESP32 开发和调试支持"
requires_api: false
---

# esp32-embedded-dev Skill

## 概述

ESP32 开发和调试支持。

## 依赖

### 系统工具

需要安装 ESP-IDF 工具链：

```bash
# 安装 ESP-IDF
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/

# 常用工具
- esptool: ESP32 烧录工具
- idf.py: ESP-IDF 构建系统
- menuconfig: 配置工具
```

### Python 库

```bash
pip install esptool
```

**说明**: 需要 ESP-IDF 开发环境和相关工具链。

## 使用

### 基本用法

```
使用 esp32-embedded-dev 帮助配置 ESP32 的 I2C 外设
```



## ElecSpeckit 集成指南

### 在 ElecSpeckit 工作流中使用

**场景**: 嵌入式系统类相关任务

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
