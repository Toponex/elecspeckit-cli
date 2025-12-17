---
name: mouser-component-search
description: Search Mouser Electronics for component availability, pricing, datasheets, and lead times. Use when designing hardware, sourcing components, checking inventory, comparing prices, or finding datasheets for electronic parts.
version: 1.0.0
requires_api: true
enabled: false
---

# mouser-component-search

搜索 Mouser Electronics 以获取元件可用性、定价、数据手册和交货周期信息。

## 概述

**mouser-component-search** Skill 提供了与 Mouser Electronics API 的无缝集成，使您能够：

- 通过型号、制造商或关键字搜索电子元件
- 检查实时库存可用性和库存水平
- 获取当前价格信息及批量折扣
- 直接从搜索结果访问数据手册链接
- 查看缺货或待补货物品的交货周期

此 Skill 对于硬件工程师、电子设计师以及任何需要快速验证 Mouser Electronics 元件可用性和定价的人员来说都是必不可少的工具。

## 何时使用此 Skill

在以下情况下使用 mouser-component-search Skill：

- **元件采购**：查找特定电子元件的购买渠道
- **BOM 验证**：验证物料清单中的元件是否可用
- **价格估算**：获取元件采购的成本估算
- **数据手册访问**：快速查找元件的官方数据手册
- **交货周期规划**：检查项目规划的交货时间线
- **替代元件**：当首选元件不可用时搜索类似元件

## 使用方法

此 Skill 使用 Python 脚本（`scripts/mouser_search.py`）与 Mouser Search API 进行交互。

**示例 1：搜索微控制器**
```
请在 Mouser 上搜索 STM32F103C8T6，并显示可用性和价格。
```

**示例 2：检查多个元件**
```
我需要检查以下元件在 Mouser 的库存情况：
- LM358 运算放大器
- 1N4148 二极管
- BC547 三极管

请分别搜索每一个并总结结果。
```

**示例 3：获取数据手册链接**
```
在 Mouser 上查找 STM32F407VGT6 并提供数据手册链接。
```

**示例 4：批量价格查询**
```
我需要采购 1000 颗 0805 封装的 10uF 电容，请查询 Mouser 上的批量价格。
```

**示例 5：交货周期确认**
```
我的项目需要在 3 个月内完成，请确认 ESP32-WROOM-32D 模块在 Mouser 的交货周期。
```

## 配置

### 前提条件

1. **Mouser API 账户**：您必须拥有 Mouser Electronics 账户和 API 访问权限
2. **API Key**：从 Mouser Developer Portal 获取您的 API 密钥：https://www.mouser.com/api-hub/
3. **Python 依赖项**：脚本需要 Python 3.11+ 和 `requests` 库

### API Key 设置

mouser-component-search Skill 需要 API 密钥才能访问 Mouser Search API。请按照以下步骤操作：

#### 步骤 1：获取您的 Mouser API Key

1. 访问 Mouser Developer Portal：https://www.mouser.com/api-hub/
2. 使用您的 Mouser Electronics 账户登录（如有需要请创建账户）
3. 导航至 "My Account" → "API Keys"
4. 为搜索操作生成新的 API 密钥
5. 复制您的 API 密钥（格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

#### 步骤 2：配置 Skill

使用 `/elecspeckit.skillconfig update` 命令设置您的 API 密钥：

```bash
/elecspeckit.skillconfig update mouser-component-search --api-key YOUR_API_KEY
```

将 `YOUR_API_KEY` 替换为您的实际 Mouser API 密钥。

#### 步骤 3：启用 Skill

配置 API 密钥后，启用 Skill：

```bash
/elecspeckit.skillconfig enable mouser-component-search
```

#### 步骤 4：验证配置

列出所有 Skills 以验证配置：

```bash
/elecspeckit.skillconfig list
```

您应该看到 `mouser-component-search` 的状态为 `enabled: true`。

### 配置文件

API 密钥存储在 `.elecspecify/memory/skill_config.json` 中：

```json
{
  "skills": {
    "mouser-component-search": {
      "enabled": true,
      "requires_api": true,
      "api_key": "YOUR_API_KEY",
      "description": "Mouser component availability and pricing search"
    }
  }
}
```

**安全注意事项**：`skill_config.json` 文件应具有受限权限。切勿将此文件提交到版本控制或公开共享您的 API 密钥。

## 响应格式

此 Skill 返回结构化的 JSON 数据：

### 成功搜索

```json
{
  "success": true,
  "results": [
    {
      "part_number": "STM32F103C8T6",
      "manufacturer": "STMicroelectronics",
      "stock": 5000,
      "price": "$2.50",
      "datasheet_url": "https://www.mouser.com/datasheet/...",
      "lead_time": "10 weeks"
    }
  ]
}
```

### 未找到结果

```json
{
  "success": true,
  "results": []
}
```

### 错误响应

```json
{
  "success": false,
  "error": "API key not configured. Please use /elecspeckit.skillconfig update mouser-component-search --api-key YOUR_KEY to configure"
}
```

## 错误处理

此 Skill 优雅地处理各种错误场景：

### 1. API Key 未配置

**错误**：`API key not configured`

**解决方案**：使用 `/elecspeckit.skillconfig update mouser-component-search --api-key YOUR_KEY` 配置您的 API 密钥

### 2. 无效的 API Key

**错误**：`Invalid API key, please check your configuration`

**解决方案**：验证您的 API 密钥是否正确。如有需要，从 Mouser Developer Portal 生成新密钥。

### 3. 超出速率限制

**错误**：`API rate limit exceeded, please try again later`

**解决方案**：Mouser API 有速率限制（每次调用 50 个请求，每分钟 30 次调用）。请等待几分钟后重试。

### 4. 网络问题

**错误**：`Unable to connect to Mouser API, please check network connection`

**解决方案**：验证您的互联网连接，并确保可以从您的网络访问 `api.mouser.com`。

### 5. 无结果

**行为**：返回 `"success": true` 和空的 `results` 数组

**含义**：搜索查询未匹配任何元件。尝试：
- 检查型号的拼写
- 使用更通用的搜索词
- 按制造商名称搜索

## API 限制和最佳实践

### 速率限制

- **每次调用 50 个请求**
- **每分钟 30 次调用**

此 Skill 自动处理速率限制错误并提供清晰的反馈。

### 最佳实践

1. **具体明确**：尽可能使用精确的型号以获得最快的结果
2. **批量搜索**：如果检查多个元件，请在一次对话中搜索它们以最小化 API 调用
3. **缓存结果**：元件可用性变化缓慢；避免重复搜索
4. **遵守限制**：不要实现可能超过速率限制的自动循环
5. **错误重试**：如遇临时错误，等待适当时间后再重试
6. **精确匹配**：使用完整的制造商型号而非简化版本
7. **数据验证**：始终验证返回的数据是否符合您的需求

## 技术细节

### 脚本位置

- **脚本**：`scripts/mouser_search.py`
- **语言**：Python 3.11+
- **依赖项**：`requests>=2.31.0`

### API 端点

- **URL**：`https://api.mouser.com/api/v1/search/keyword`
- **方法**：GET
- **认证**：API Key（Header: `X-API-Key`）
- **响应格式**：JSON

### 配置路径

- **配置文件**：`~/.elecspecify/memory/skill_config.json`
- **权限**：0600（类 Unix 系统）

### 依赖项安装

如果缺少必要的 Python 库，请使用以下命令安装：

```bash
pip install requests>=2.31.0
```

## 详细示例

### 示例 1：基本元件搜索

**用户请求**：
```
在 Mouser 上搜索 STM32F103C8T6
```

**Claude Code 响应**（使用此 Skill）：
```
我在 Mouser 上找到了 STM32F103C8T6：

- 型号：STM32F103C8T6
- 制造商：STMicroelectronics
- 库存：5,000 颗可用
- 价格：$2.50（单价）
- 数据手册：[查看 PDF](https://www.mouser.com/datasheet/...)
- 交货周期：10 周

此微控制器有充足的库存，可用性良好。
```

### 示例 2：价格比较

**用户请求**：
```
我正在比较不同来源的 LM358 运算放大器。Mouser 的价格是多少？
```

**Claude Code 响应**（使用此 Skill）：
```
正在检查 Mouser 上的 LM358 运算放大器...

Mouser 有 LM358 库存：
- 价格：$0.35 每颗
- 库存：15,000+ 颗
- 制造商：Texas Instruments
- 数据手册：[点击查看](...)

这是一个常备元件，可用性极佳。
```

### 示例 3：BOM 验证

**用户请求**：
```
我正在完成我的 BOM。能否检查这些元件在 Mouser 上是否可用？
- STM32F407VGT6
- AMS1117-3.3
- 0805 10uF 电容
```

**Claude Code 响应**（使用此 Skill）：
```
我将检查 Mouser 上的每个元件：

1. STM32F407VGT6（微控制器）：
   - 库存：2,500 颗
   - 价格：$8.50
   - 状态：可用

2. AMS1117-3.3（电压调节器）：
   - 库存：8,000 颗
   - 价格：$0.45
   - 状态：可用

3. 0805 10uF 电容：
   - 多个选项可用
   - 价格范围：$0.10 - $0.25
   - 状态：可用

所有元件目前在 Mouser 上都有库存。
```

### 示例 4：交货周期规划

**用户请求**：
```
我的项目时间表很紧。请检查以下元件的交货周期：
- STM32H743VIT6
- TPS54620RGYR
- LAN8720A-CP
```

**Claude Code 响应**（使用此 Skill）：
```
以下是各元件的交货周期信息：

1. STM32H743VIT6（高性能微控制器）：
   - 库存：150 颗
   - 交货周期：16 周（如缺货）
   - 建议：库存有限，建议立即订购

2. TPS54620RGYR（降压转换器）：
   - 库存：5,000+ 颗
   - 交货周期：即时发货
   - 建议：库存充足

3. LAN8720A-CP（以太网 PHY）：
   - 库存：缺货
   - 交货周期：20 周
   - 建议：考虑替代型号 LAN8720AI

建议优先确保 STM32H743VIT6 和 LAN8720A 的供应，或寻找替代方案。
```

### 示例 5：批量定价查询

**用户请求**：
```
我需要 5000 颗 BC547 三极管。请查询批量价格。
```

**Claude Code 响应**（使用此 Skill）：
```
BC547 三极管的批量定价信息：

- 1-99 颗：$0.12/颗
- 100-999 颗：$0.08/颗
- 1000-4999 颗：$0.05/颗
- 5000+ 颗：$0.03/颗

您需要的 5000 颗，总价格约为 $150.00
库存：50,000+ 颗可用
制造商：ON Semiconductor

建议：库存充足，可满足您的需求。
```

## 常见问题解答（FAQ）

### Q1：此 Skill 是否支持其他分销商？

**A**：此 Skill 专门用于 Mouser Electronics。如需搜索其他分销商，请考虑使用 **web-research** Skill 或访问各分销商的网站。

### Q2：API 密钥是否有有效期？

**A**：Mouser API 密钥通常不会过期，但可能因安全原因被撤销。如果您的密钥无效，请在 Mouser Developer Portal 重新生成。

### Q3：搜索结果的数据多久更新一次？

**A**：Mouser API 提供实时数据，包括库存水平、价格和交货周期。数据准确性取决于 Mouser 的更新频率。

### Q4：能否搜索替代或兼容元件？

**A**：此 Skill 基于关键字搜索。您可以使用更通用的搜索词找到类似元件，但具体的替代建议需要工程判断。

### Q5：是否支持国际运费和税费计算？

**A**：此 Skill 仅提供元件价格。运费和税费需要在 Mouser 网站上结账时计算。

### Q6：如何处理停产元件？

**A**：如果元件已停产，搜索可能返回空结果或显示 "Obsolete" 状态。建议使用 **web-research** Skill 查找替代元件。

### Q7：是否可以保存搜索历史？

**A**：此 Skill 不保存搜索历史。每次搜索都是独立的 API 调用。如需保存 BOM 信息，请在您的项目文档中记录。

### Q8：API 调用是否收费？

**A**：Mouser 提供免费的 API 访问，但有速率限制。超出限制可能需要联系 Mouser 获取企业级访问。

## 故障排除

### 问题：Skill 无响应

**检查**：
1. Skill 是否已启用？运行 `/elecspeckit.skillconfig list`
2. API 密钥是否已配置？检查 `.elecspecify/memory/skill_config.json`
3. Python 3.11+ 是否已安装？运行 `python --version`
4. `requests` 库是否已安装？运行 `pip list | grep requests`

### 问题："Invalid API Key" 错误

**解决方案**：
1. 在 https://www.mouser.com/api-hub/ 验证您的 API 密钥
2. 检查 API 密钥配置中的拼写错误
3. 如果当前密钥已过期或被撤销，生成新的 API 密钥
4. 使用 `/elecspeckit.skillconfig update mouser-component-search --api-key NEW_KEY` 重新配置

### 问题：有效型号返回空结果

**可能原因**：
1. 型号在 Mouser 不可用（尝试其他分销商）
2. 型号已停产或过时
3. 型号拼写错误（检查制造商网站）
4. 型号为特定分销商专有（不通过 Mouser 销售）

**解决方案**：
- 尝试更广泛的搜索词
- 按制造商名称搜索
- 直接检查 Mouser 网站以验证可用性

### 问题：搜索速度慢

**可能原因**：
1. 网络连接慢
2. Mouser API 服务器响应慢
3. 搜索词过于宽泛，返回大量结果

**解决方案**：
- 使用更具体的搜索词或完整型号
- 检查您的网络连接
- 在非高峰时段重试

### 问题：数据手册链接无效

**可能原因**：
1. 制造商更新了数据手册 URL
2. 数据手册已从 Mouser 服务器移除
3. 临时的 CDN 问题

**解决方案**：
- 使用 **docs-seeker** Skill 从其他来源查找数据手册
- 直接访问制造商网站
- 稍后重试

## 应用场景

### 场景 1：原型开发

在原型开发阶段，快速验证关键元件的可用性和价格：

```
我正在开发一个基于 ESP32 的物联网设备。请检查以下元件：
- ESP32-WROOM-32D
- CP2102 USB-to-UART 桥接器
- AMS1117-3.3V 稳压器
- 0805 100nF 去耦电容（至少 20 颗）
```

### 场景 2：成本优化

比较不同制造商的类似元件以优化 BOM 成本：

```
我需要一个通用运算放大器。请比较以下选项的价格和可用性：
- LM358
- TL072
- MCP6002
批量：1000 颗
```

### 场景 3：紧急采购

快速确认紧急项目所需元件的即时可用性：

```
紧急！我需要在 3 天内收到以下元件：
- Arduino Nano（至少 10 个）
- HC-05 蓝牙模块（至少 5 个）
请确认 Mouser 的库存和最快的发货选项。
```

### 场景 4：供应链风险管理

评估关键元件的供应链风险：

```
我的产品使用 STM32F103C8T6。请检查：
1. 当前库存水平
2. 交货周期
3. 是否有 "Active" 生产状态
4. 过去 3 个月的可用性趋势（如果 API 支持）
```

## 集成工作流程

### 与其他 Skills 的配合

1. **docs-seeker + mouser-component-search**：
   - 首先使用 mouser-component-search 找到元件
   - 然后使用 docs-seeker 获取完整的技术规格和应用笔记

2. **web-research + mouser-component-search**：
   - 使用 web-research 研究设计方案
   - 使用 mouser-component-search 验证推荐元件的可用性

3. **embedded-systems + mouser-component-search**：
   - 使用 embedded-systems 获取设计指导
   - 使用 mouser-component-search 确认建议元件的采购信息

### 在 ElecSpeckit 工作流中的位置

```
设计阶段 → 元件选择 → [mouser-component-search] → BOM 生成 → 采购
                ↓
            数据手册审查（docs-seeker）
```

## 版本历史

- **v1.0.0**（2025-12-16）：初始发布
  - Mouser Search API 集成
  - 实时库存检查
  - 价格和数据手册检索
  - API 密钥问题的错误处理
  - 速率限制处理

## 相关 Skills

- **docs-seeker**：从多个来源查找元件数据手册
- **web-research**：研究元件规格和替代方案
- **embedded-systems**：获取嵌入式设计的元件选择指导

## 支持

### 特定于此 Skill 的问题

- 查看 ElecSpeckit 文档：https://github.com/your-org/elecspeckit-cli
- 报告 bug：https://github.com/your-org/elecspeckit-cli/issues

### Mouser API 问题

- Mouser Developer Portal：https://www.mouser.com/api-hub/
- Mouser 支持：https://www.mouser.com/contact-us/

## 许可证

此 Skill 遵循 ElecSpeckit CLI 许可证。请参阅主存储库的 LICENSE 文件。

---

**最后更新**：2025-12-16
**Skill 类型**：Type 2（API 集成）
**状态**：生产就绪
