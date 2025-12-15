---
name: "perplexity-search"
description: "使用 Perplexity AI 进行深度网络搜索和研究"
requires_api: true
---

# perplexity-search Skill

## 概述

使用 Perplexity AI 进行深度网络搜索和研究，特别适合技术文档查找、学术资料检索、行业标准查询。

Perplexity AI 提供:
- 实时网络搜索能力
- 自动引用来源
- 学术论文和技术文档优先
- 多轮对话式深挖

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

或直接编辑 `.elecspecify/memory/skill_config.json`:

```json
{
  "skills": {
    "research": {
      "perplexity-search": {
        "enabled": true,
        "requires_api": true,
        "api_key": "pplx-YOUR-API-KEY-HERE",
        "description": "使用 Perplexity AI 进行深度网络搜索和研究"
      }
    }
  }
}
```

## 使用

### 基本用法

在 Claude Code 对话中直接调用：

```
使用 perplexity-search 查找 PCIe 5.0 标准的最新规范文档
```

### 技术文档查找

```
用 Perplexity 搜索 USB Type-C PD 3.1 协议的官方白皮书和参考设计
```

### 学术资料检索

```
通过 Perplexity 查找关于低功耗蓝牙 (BLE) Mesh 网络拓扑优化的最新研究论文
```

### 行业标准查询

```
使用 perplexity-search 找到 IPC-A-610 Class 3 焊接标准的完整描述和验收标准
```

## 功能特性

1. **实时网络搜索**: 访问最新的在线资源，不受知识截止日期限制
2. **自动引用来源**: 每个答案都附带可验证的来源链接
3. **学术优先**: 优先返回学术论文、技术白皮书、官方标准文档
4. **多轮对话**: 支持追问和深挖，逐步细化搜索结果
5. **技术专注**: 针对工程和技术领域优化的搜索结果

## ElecSpeckit 集成指南

### 在 /elecspeckit.specify 中使用

**场景**: 编写规格时查找技术标准和参考设计

```
用户: /elecspeckit.specify USB-C 充电模块

AI: [内部调用] perplexity-search:
    查询 "USB Type-C PD 3.1 reference design schematic"

    找到关键资源:
    • USB-IF 官方 PD 3.1 规范 (USB Power Delivery Specification Rev 3.1)
    • TI 的 USB-C PD 参考设计 (TIDA-010054)
    • Cypress/Infineon EZ-PD CCG7 方案

    在 spec.md 中引用:
    - 遵循 USB-IF PD 3.1 标准 (240W EPR 支持)
    - 参考 TI TIDA-010054 设计指南
    - 使用 Cypress CCG7 PD 控制器
```

### 在 /elecspeckit.plan 中使用

**场景**: 设计阶段查找技术方案和最佳实践

```
用户: /elecspeckit.plan

AI: Phase 2 架构设计 - EMI 抑制方案

    [内部调用] perplexity-search:
    查询 "PCIe 5.0 EMI mitigation best practices"

    找到关键方案:
    1. Intel PCIe 5.0 设计指南 - EMI 章节
       • 差分信号走线阻抗控制 (85Ω ±10%)
       • 参考平面完整性要求
       • 过孔 via 优化建议

    2. Keysight 应用笔记 AN-1382
       • 时钟展频 (SSC) 配置
       • 共模扼流圈选型

    在 plan.md 中生成设计决策:
    - EMI 抑制策略: 阻抗控制 + SSC + 共模滤波
    - 参考文档: [Intel PCIe 5.0 Design Guide], [Keysight AN-1382]
```

### 在 /elecspeckit.tasks 中使用

**场景**: 任务拆分时查找测试标准和验证方法

```
用户: /elecspeckit.tasks

AI: 任务拆分 - DVT 测试计划

    [内部调用] perplexity-search:
    查询 "IPC-TM-650 PCB reliability test methods"

    找到测试标准:
    • IPC-TM-650 2.6.25: Thermal Stress (Solder Float)
    • IPC-TM-650 2.6.7.1: Thermal Shock
    • IPC-TM-650 2.6.26: Highly Accelerated Stress Test (HAST)

    生成测试任务:
    - Task 7.1: 热应力测试 (按 IPC-TM-650 2.6.25, 288°C × 10s)
    - Task 7.2: 冷热冲击测试 (-40°C ↔ +85°C, 1000 cycles)
    - Task 7.3: HAST 加速老化 (130°C/85%RH, 96h)
```

### 典型使用流程

1. **需求澄清阶段**: 查找行业标准、技术术语定义
2. **规格编写阶段**: 查找参考设计、官方白皮书
3. **架构设计阶段**: 查找设计指南、最佳实践、应用笔记
4. **任务拆分阶段**: 查找测试标准、验证方法
5. **问题排查阶段**: 查找故障诊断指南、调试技巧

## 最佳实践

### ✅ 推荐做法

- 使用具体的技术术语（如 "PCIe 5.0 signal integrity" 而不是 "高速信号"）
- 指定文档类型（标准、白皮书、应用笔记、学术论文）
- 包含制造商/组织名称（如 "Intel PCIe design guide"）
- 指定版本号或年份（如 "USB PD 3.1" 而不是 "USB 充电"）

### ❌ 避免做法

- 不要使用过于宽泛的查询（如 "电路设计"）
- 不要依赖单一来源（交叉验证多个来源）
- 不要忽略文档版本（旧版本标准可能已废弃）
- 不要在未验证来源可靠性的情况下直接引用

## 示例

### 示例 1: 查找技术标准

```
用户: 使用 perplexity-search 查找 JESD79-5 DDR5 SDRAM 标准的最新版本

AI: [调用 Perplexity API]

    查询结果:

    标准名称: JESD79-5B
    发布组织: JEDEC (Joint Electron Device Engineering Council)
    发布时间: 2022年11月

    主要内容:
    • DDR5 SDRAM 电气规范
      - 数据传输率: 3200-6400 MT/s
      - 工作电压: VDD = 1.1V, VDDQ = 1.1V
      - On-Die ECC (ODECC) 支持

    • 关键特性:
      - 双通道架构 (2× 32-bit subchannels)
      - 32 bank groups (8 bank groups × 4 banks)
      - Decision Feedback Equalization (DFE)

    下载链接:
    • JEDEC 官网: https://www.jedec.org/standards-documents/docs/jesd79-5b
    • 需要免费注册 JEDEC 账户

    相关参考:
    • JESD79-5A (2020年版本, 已废弃)
    • JESD82-500 (DDR5 Module 标准)
```

### 示例 2: 查找参考设计

```
用户: 用 Perplexity 搜索 STM32H7 系列的以太网 PHY 连接参考设计

AI: [调用 Perplexity API]

    查询结果:

    找到 3 个官方参考设计:

    1. STM32H743I-EVAL 评估板
       制造商: STMicroelectronics
       PHY 芯片: LAN8742A (RMII 接口)

       关键设计细节:
       • RMII 时钟: 50MHz 外部晶振 (REF_CLK)
       • 电源: 3.3V for PHY, 1.8V for I/O
       • MDC/MDIO 管理接口配置
       • 原理图参考: UM2407 User Manual, Figure 15

       下载: https://www.st.com/resource/en/user_manual/um2407.pdf

    2. STM32H750B-DK 开发板
       PHY 芯片: LAN8720A (RMII 接口)

       设计差异:
       • 使用 STM32 内部 MCO 输出 50MHz 时钟
       • 节省外部晶振成本

       原理图: UM2632, Sheet 6

    3. 社区参考 (EEVblog Forums)
       • PCB 布局注意事项: 差分对 90Ω 阻抗控制
       • EMI 对策: 磁珠 + 共模扼流圈
       • 调试经验: 上电时序很关键 (PHY 先上电)

    推荐方案:
    ✓ 使用 LAN8742A (支持 HP Auto-MDIX, 更稳定)
    ✓ 参考 STM32H743I-EVAL 原理图 (Figure 15, 16)
    ✓ 预留 MCO 时钟输出测试点
```

### 示例 3: 查找测试标准

```
用户: 通过 Perplexity 查找 MIL-STD-810H 振动测试的具体要求

AI: [调用 Perplexity API]

    查询结果:

    标准全称: MIL-STD-810H (Environmental Engineering Considerations and Laboratory Tests)
    发布时间: 2019年1月

    振动测试章节: Method 514.8

    测试类型:

    1. General Vibration (通用振动)
       • 频率范围: 1 Hz - 2000 Hz
       • 测试曲线: Figure 514.8C-1 (Ground Vehicle curve)
       • 持续时间: 3小时/轴 (X, Y, Z 三轴)
       • 量级: 0.04 g²/Hz (5-500 Hz plateau)

    2. Random Vibration (随机振动)
       • 适用于: 车载、航空电子设备
       • PSD 谱密度: 见 Table 514.8C-III
       • Grms: 6.1 Grms (典型车载环境)

    3. Loose Cargo Transportation (松散货物运输)
       • 针对运输包装验证
       • PSD: Figure 514.8C-8
       • 持续时间: 3小时 (单轴垂直)

    测试设备要求:
    • 电动振动台 (推荐: 20 kN 以上推力)
    • 三轴固定夹具
    • 实时监控加速度传感器

    相关标准对比:
    • RTCA DO-160G (民航): 类似但更严格
    • IEC 60068-2-64 (工业): 更注重长期可靠性

    参考文档下载:
    • MIL-STD-810H 完整版 (800+ 页): DTIC 网站
    • 简化解读: NASA Technical Reports Server
```

## 故障排除

### 问题: API 密钥无效

**解决方案**:
1. 检查 `.elecspecify/memory/skill_config.json` 中的 `api_key` 格式
2. 访问 Perplexity 官网申请新密钥: https://www.perplexity.ai/settings/api
3. 确认账户有足够的 API 配额（免费账户有请求限制）

### 问题: 搜索结果不相关

**解决方案**:
1. 使用更具体的技术术语和型号
2. 添加文档类型关键词（datasheet, application note, standard）
3. 指定制造商或组织名称（Intel, IEEE, JEDEC）
4. 包含版本号或年份

### 问题: 无法访问付费资源

**解决方案**:
1. Perplexity 可能返回付费论文/标准的摘要
2. 使用机构图书馆账户访问完整文档
3. 查找预印本版本（arXiv, ResearchGate）
4. 联系文档发布组织申请免费访问

## 技术细节

### API 配置

skill_config.json 配置示例:

```json
{
  "perplexity-search": {
    "enabled": true,
    "requires_api": true,
    "api_key": "pplx-YOUR-API-KEY-HERE",
    "description": "使用 Perplexity AI 进行深度网络搜索和研究",
    "api_endpoint": "https://api.perplexity.ai/chat/completions",
    "model": "sonar-medium-online"
  }
}
```

### API 限制

- **请求频率**: 取决于 Perplexity 账户类型
  - 免费账户: 5 请求/小时
  - Pro 账户: 300 请求/天
  - Enterprise: 自定义配额
- **响应时间**: 通常 3-10 秒（含实时搜索）
- **上下文长度**: 最多 4K tokens

### 数据来源

- 实时网络索引（不受知识截止日期限制）
- 学术数据库优先（Google Scholar, PubMed, arXiv）
- 官方技术文档（制造商网站、标准组织）
- 自动引用来源 URL

## 与其他 Skills 的协同

### perplexity-search + docs-seeker

```
场景: 先用 Perplexity 找到文档名称，再用 docs-seeker 在本地查找

1. perplexity-search: "STM32H7 RMII Ethernet reference design"
   → 找到文档: UM2407 User Manual

2. docs-seeker: 在本地 docs/ 目录搜索 "UM2407"
   → 找到本地副本或提示下载链接
```

### perplexity-search + openalex-database

```
场景: Perplexity 找到研究主题，openalex-database 查找相关学术论文

1. perplexity-search: "DDR5 signal integrity challenges"
   → 找到关键研究主题和术语

2. openalex-database: 用精确术语查找学术论文
   → 检索 OpenAlex 数据库，获取论文列表和引用关系
```

### perplexity-search + web-research

```
场景: Perplexity 提供概览，web-research 深挖特定网站

1. perplexity-search: "PCIe 5.0 design guidelines"
   → 找到 Intel、PCI-SIG 等来源

2. web-research: 爬取 Intel 官网的完整设计指南
   → 提取详细的设计规则和计算公式
```

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
