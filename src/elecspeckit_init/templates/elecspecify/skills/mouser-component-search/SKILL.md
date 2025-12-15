---
name: "mouser-component-search"
description: "搜索 Mouser 电子元器件库存和价格"
requires_api: true
---

# mouser-component-search Skill

## 概述

搜索 Mouser 电子元器件库存和价格。

## 依赖

### Python 库

```bash
pip install requests
```

**说明**: 需要 `requests` 库访问 Mouser API。

### API 密钥配置

需要配置 Mouser API 密钥：

```bash
# 使用 skillconfig 命令配置
/elecspeckit.skillconfig update mouser-component-search --api-key YOUR_API_KEY
```

## 使用

### 基本用法

在 Claude Code 对话中直接调用：

```
使用 mouser-component-search 搜索 STM32F407VGT6 的库存和价格
```

### 搜索特定参数的器件

```
在 Mouser 上搜索满足以下条件的运放：
- 带宽 > 10MHz
- 电源电压: 单电源 5V
- 封装: SOIC-8
```

### 批量查询

```
使用 mouser-component-search 查询以下器件的价格和交期：
- TPS54620RHLR
- LMR14050SDDA
- TLV62130RGT
```

## 功能特性

1. **实时库存查询**: 获取 Mouser 最新库存数据
2. **价格阶梯**: 显示不同数量的单价
3. **交期信息**: 预计到货时间和库存状态
4. **参数过滤**: 根据电气参数筛选器件
5. **替代料推荐**: 查找功能相似的替代器件

## ElecSpeckit 集成指南

### 在 /elecspeckit.plan 中使用

**场景**: Phase 1 器件选型 - 查询库存和价格

```
用户: /elecspeckit.plan

AI: Phase 1 器件选型 - 主控芯片选择

    [内部调用] mouser-component-search:
    - STM32F407VGT6 (首选方案)
    - STM32F407VET6 (备选方案)

    查询结果:
    • STM32F407VGT6: 库存 5,200 片，单价 $8.50 (100+)，交期 2 周
    • STM32F407VET6: 库存 1,800 片，单价 $7.20 (100+)，交期 4 周

    推荐: 选择 STM32F407VGT6，库存充足，交期短
```

### 在 /elecspeckit.specify 中使用

**场景**: 编写 BOM 规格时验证器件可获得性

```
用户: /elecspeckit.specify 电源管理模块

AI: [内部调用] mouser-component-search:
    验证关键器件可获得性:
    - TPS54620RHLR (Buck 转换器)
    - TLV62130RGT (降压稳压器)

    库存状态: ✓ 所有器件库存充足

    在 spec.md 中标注:
    - 主要供应商: Mouser (库存验证通过)
    - 备选供应商: DigiKey, Arrow
```

### 在 /elecspeckit.tasks 中使用

**场景**: 任务拆分时估算采购成本和周期

```
用户: /elecspeckit.tasks

AI: 任务拆分 - 采购计划

    [内部调用] mouser-component-search:
    批量查询 BOM 中 50 个器件

    生成采购任务:
    - Task 1: 采购长交期器件 (交期 > 4 周)，预算 $2,500
    - Task 2: 采购常规器件 (交期 < 2 周)，预算 $1,800
    - Task 3: 备货风险器件 (库存 < 1000)，额外采购 20%
```

### 典型使用流程

1. **器件选型阶段**: 查询候选器件库存、价格、交期
2. **BOM 编制阶段**: 验证所有器件可获得性
3. **成本估算阶段**: 计算不同数量阶梯的总成本
4. **风险评估阶段**: 识别长交期和低库存器件
5. **采购计划阶段**: 制定分批采购策略

## 最佳实践

### ✅ 推荐做法

- 使用完整的制造商型号（如 "TPS54620RHLR" 而不是 "TPS54620"）
- 查询多个候选料号，避免单一来源风险
- 关注库存数量，低于 1000 片时考虑备选方案
- 记录查询时间，器件价格和库存会变化

### ❌ 避免做法

- 不要依赖单一供应商（Mouser 缺货时需要备选渠道）
- 不要忽略最小起订量（MOQ）
- 不要使用模糊的器件名称（如 "运放"、"稳压器"）
- 不要在未确认库存的情况下锁定设计方案

## 示例

### 示例 1: 查询单个器件

```
用户: 使用 mouser-component-search 查询 TPS54620RHLR 的详细信息

AI: [调用 Mouser API]

    查询结果:

    器件: TPS54620RHLR
    制造商: Texas Instruments
    描述: 6A 同步降压转换器，VQFN-14

    库存信息:
    • Mouser 库存: 3,420 片
    • 工厂库存: 15,000+ 片

    价格阶梯:
    •   1-9:   $2.85/片
    •  10-99:  $2.35/片
    • 100-499: $1.98/片
    • 500+:    $1.75/片

    交期:
    • 现货: 3,420 片，1-2 个工作日发货
    • 补货: 预计 4-6 周

    数据手册: [链接]
```

### 示例 2: 参数搜索

```
用户: 在 Mouser 搜索满足以下条件的 LDO：
- 输出电流 > 500mA
- 输入电压范围: 3.3V - 5.5V
- 输出电压: 3.3V
- 封装: SOT-23-5

AI: [调用 Mouser API 参数搜索]

    找到 8 个匹配器件:

    1. AP2114H-3.3TRG1
       - 输出电流: 1A
       - 压差: 250mV @ 1A
       - 库存: 15,200 片
       - 单价: $0.35 (100+)
       ✓ 推荐（性价比高，库存充足）

    2. LM1117MP-3.3/NOPB
       - 输出电流: 800mA
       - 压差: 1.2V @ 800mA
       - 库存: 8,500 片
       - 单价: $0.48 (100+)

    3. MIC5504-3.3YM5-TR
       - 输出电流: 500mA
       - 压差: 165mV @ 500mA
       - 库存: 6,100 片
       - 单价: $0.52 (100+)
       ✓ 推荐（低压差）

    [显示其他 5 个器件...]
```

### 示例 3: BOM 批量查询

```
用户: 批量查询以下 BOM 器件的库存和总成本（数量 100 套）

BOM:
- STM32F407VGT6 x 1
- TPS54620RHLR x 2
- LM1117MP-3.3 x 3
- 0805 10uF 电容 x 20
- 0603 100nF 电容 x 50

AI: [批量调用 Mouser API]

    BOM 查询结果 (100 套):

    | 料号              | 单套用量 | 单价(100+) | 单套成本 | 库存状态 |
    |-------------------|---------|-----------|----------|---------|
    | STM32F407VGT6     | 1       | $8.50     | $8.50    | ✓ 5,200 |
    | TPS54620RHLR      | 2       | $1.98     | $3.96    | ✓ 3,420 |
    | LM1117MP-3.3      | 3       | $0.48     | $1.44    | ✓ 8,500 |
    | 0805 10uF/25V     | 20      | $0.08     | $1.60    | ✓ 50K+  |
    | 0603 100nF/50V    | 50      | $0.02     | $1.00    | ✓ 100K+ |

    汇总:
    • 单套成本: $16.50
    • 100 套总成本: $1,650
    • 所有器件库存充足 ✓
    • 预计交期: 1-2 周

    风险评估:
    ⚠ TPS54620RHLR 库存相对紧张 (3,420 片)
      建议: 考虑提前备货或寻找替代料
```

## 故障排除

### 问题: API 密钥无效

**解决方案**:
1. 检查 `.elecspecify/memory/skill_config.json` 中的 `api_key` 是否正确
2. 访问 Mouser 官网申请新的 API 密钥: https://www.mouser.com/api-hub/
3. 确认 API 密钥已激活（需要邮箱验证）

### 问题: 查询超时

**解决方案**:
1. 检查网络连接
2. 减少批量查询的器件数量
3. 稍后重试（可能是 Mouser API 限流）

### 问题: 找不到器件

**解决方案**:
1. 确认制造商型号完整正确
2. 尝试使用 Mouser 料号 (Mouser Part Number)
3. 检查器件是否停产或 Mouser 未代理

## 技术细节

### API 配置

skill_config.json 配置示例:

```json
{
  "mouser-component-search": {
    "enabled": true,
    "requires_api": true,
    "api_key": "your-mouser-api-key-here",
    "description": "搜索 Mouser 电子元器件库存和价格"
  }
}
```

### API 限制

- **请求频率**: 1000 次/天 (免费账户)
- **批量查询**: 建议每次不超过 50 个器件
- **响应时间**: 通常 1-3 秒

### 数据来源

- 实时库存数据来自 Mouser 数据库
- 价格更新频率: 每小时
- 数据手册链接直接指向 Mouser 网站

## 相关 Skills

- **docs-seeker**: 查找本地的器件数据手册
- **hardware-data-analysis**: 分析 BOM 成本趋势
- **citation-management**: 管理器件数据手册引用



---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
