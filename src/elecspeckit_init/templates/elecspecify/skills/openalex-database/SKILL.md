---
name: "openalex-database"
description: "查询 OpenAlex 学术数据库获取论文、引用和研究趋势"
requires_api: false
---

# openalex-database Skill

## 概述

查询 OpenAlex 学术数据库获取学术论文、引用关系、研究者信息和研究趋势数据。

OpenAlex 是一个开放的学术知识图谱，包含:
- 超过 2.5 亿篇论文的元数据
- 引用关系和影响力分析
- 作者、机构、期刊信息
- 研究主题和领域分类
- 完全免费，无需 API 密钥

## 依赖

### Python 库

```bash
pip install pyalex requests
```

**说明**:
- `pyalex`: OpenAlex Python 客户端库
- `requests`: HTTP 请求库（备用直接 API 调用）

## 使用

### 基本用法

在 Claude Code 对话中直接调用：

```
使用 openalex-database 查找关于 GaN HEMT 功率器件的最新研究论文
```

### 按主题搜索论文

```
用 OpenAlex 搜索关于 PCIe 5.0 信号完整性的学术论文，按引用数排序
```

### 按作者查找

```
通过 openalex-database 查找 IEEE Fellows 在射频电路设计领域的代表性论文
```

### 引用关系分析

```
使用 OpenAlex 分析 DDR5 内存控制器设计相关论文的引用网络
```

## 功能特性

1. **海量学术资源**: 2.5 亿+ 论文元数据，覆盖所有学科
2. **免费开放**: 无需 API 密钥，无请求限制
3. **引用分析**: 论文引用关系、影响力指标 (citation count)
4. **多维筛选**: 按年份、期刊、作者、机构、领域过滤
5. **开放获取标识**: 识别 OA 论文和预印本
6. **研究趋势**: 按时间线分析研究热点演变

## ElecSpeckit 集成指南

### 在 /elecspeckit.specify 中使用

**场景**: 编写规格时查找学术背景和技术前沿

```
用户: /elecspeckit.specify 高速 SerDes 接口模块

AI: [内部调用] openalex-database:
    查询 "SerDes signal integrity equalization"

    找到关键论文:
    1. "Machine Learning-Based Channel Equalization for High-Speed SerDes"
       • IEEE JSSC 2023, 引用数: 47
       • 关键技术: Adaptive DFE using neural networks
       • OA 链接: https://ieeexplore.ieee.org/document/...

    2. "56 Gbps PAM-4 SerDes with Feed-Forward Equalizer"
       • ISSCC 2022, 引用数: 89
       • 关键指标: BER < 1e-15, Power 120mW/lane
       • 制造商参考: Broadcom, Marvell

    在 spec.md 中引用学术背景:
    - 均衡技术: FFE + DFE (参考 [IEEE JSSC 2023])
    - 性能指标: BER < 1e-12 @ 56Gbps (业界标准)
    - 功耗目标: < 150mW/lane (参考最新研究)
```

### 在 /elecspeckit.plan 中使用

**场景**: 架构设计时评估技术方案成熟度

```
用户: /elecspeckit.plan

AI: Phase 2 架构设计 - 电源管理方案选型

    [内部调用] openalex-database:
    查询 "GaN HEMT converter efficiency"

    研究趋势分析:
    • 论文数量: 2019-2024 年增长 3.2x
    • 引用峰值: 2022 年 (技术成熟标志)
    • 关键机构: ETH Zurich, CPES @ Virginia Tech

    顶级论文 (Top 3 by citations):
    1. "99.1% Efficiency GaN-Based Totem-Pole PFC"
       • TPEL 2021, 引用数: 312
       • 关键贡献: Zero-voltage switching + interleaving
       • 实现难度: 高 (需精确死区时间控制)

    2. "MHz-Frequency GaN DC-DC Converter with Planar Magnetics"
       • APEC 2023, 引用数: 156
       • 关键参数: 1 MHz, Power density 150 W/in³
       • 商用化: 已有参考设计 (TI, Infineon)

    在 plan.md 中标注技术成熟度:
    - GaN HEMT 方案: ✓ 成熟 (大量文献支持, 2022+ 产品化)
    - 推荐方案: Totem-pole PFC + LLC (效率 > 98%)
    - 风险评估: 低 (参考设计可用)
```

### 在 /elecspeckit.tasks 中使用

**场景**: 任务拆分时识别技术难点和验证方法

```
用户: /elecspeckit.tasks

AI: 任务拆分 - 技术验证计划

    [内部调用] openalex-database:
    查询 "EMI测试方法 conducted emissions"

    找到标准测试方法:
    • "CISPR 22/32 Conducted Emission Measurement Techniques"
      - IEEE EMC Magazine 2020, 引用数: 78
      - 关键内容: LISN 校准方法、peak vs quasi-peak 检波

    • "Common-Mode Choke Design for Conducted EMI Suppression"
      - TPEL 2021, 引用数: 134
      - 设计方法: 阻抗匹配、饱和特性分析

    生成验证任务:
    - Task 6.1: EMI 预测仿真 (SPICE model, 参考 [TPEL 2021] 方法)
    - Task 6.2: LISN 网络设计和校准 (按 CISPR 32 标准)
    - Task 6.3: 共模扼流圈选型验证 (阻抗曲线测试)
    - Task 6.4: 认证测试 (预约 EMC 实验室, CISPR 32 Class B)

    参考文献列表:
    [TPEL 2021] "Common-Mode Choke Design..." - 阻抗设计理论
    [IEEE EMC 2020] "CISPR 22/32 Measurement..." - 测试方法
```

### 典型使用流程

1. **技术调研阶段**: 查找领域综述论文 (review papers)
2. **方案评估阶段**: 分析技术成熟度 (论文数量趋势、引用增长)
3. **设计参考阶段**: 查找具体实现论文 (电路拓扑、参数设计)
4. **验证计划阶段**: 查找测试方法和标准 (metrology, characterization)
5. **知识传承阶段**: 建立内部技术文献库

## 最佳实践

### ✅ 推荐做法

- 使用专业术语和缩写（如 "SerDes DFE" 而不是 "高速串行均衡"）
- 指定年份范围（如 "2020-2024" 关注最新研究）
- 按引用数排序（高引论文通常质量更高）
- 检查开放获取状态（OA 论文可直接下载全文）
- 查看作者机构（顶级机构通常研究质量更高）

### ❌ 避免做法

- 不要依赖单篇论文（交叉验证多篇文献）
- 不要忽略发表年份（过旧的论文可能技术已过时）
- 不要只看标题（摘要和关键词更准确）
- 不要忽略引用关系（被高引论文引用的文章也很重要）

## 示例

### 示例 1: 按主题搜索论文

```
用户: 使用 openalex-database 查找关于 SiC MOSFET 栅极驱动的论文

AI: [调用 OpenAlex API]

    查询: "SiC MOSFET gate driver design"
    筛选: 2019-2024, 按引用数排序

    查询结果 (Top 5):

    1. "Active Gate Driver for SiC MOSFETs with dv/dt and di/dt Control"
       • 期刊: IEEE TPEL (电力电子顶刊)
       • 年份: 2021
       • 作者: J. Zhang, et al. @ Virginia Tech
       • 引用数: 267
       • 关键技术:
         - 可调 dv/dt 控制 (减少 EMI)
         - 米勒平台电压优化
         - 短路保护 < 200ns
       • OA 状态: ✓ 绿色 OA (预印本可下载)
       • DOI: 10.1109/TPEL.2021.1234567
       • PDF: https://repository.vt.edu/...

    2. "Monolithic Gate Driver IC for 1.2 kV SiC MOSFET"
       • 期刊: ISSCC (集成电路顶会)
       • 年份: 2023
       • 引用数: 89
       • 关键指标:
         - 隔离电压: 5 kVrms
         - 驱动能力: 10A peak
         - 死区时间: 可调 20-200ns
       • 商用化: PowerIntegrations 参考设计

    3. "Gate Charge Analysis and Optimization for SiC Power Devices"
       • 期刊: IEEE TIA (工业应用)
       • 年份: 2020
       • 引用数: 178
       • 贡献: 栅极电荷计算模型、损耗分析方法

    4. "Integrated Auxiliary Power Supply for Isolated Gate Drivers"
       • 期刊: APEC (应用电力电子会议)
       • 年份: 2022
       • 引用数: 56
       • 关键技术: 变压器设计、启动电路

    5. "Turn-off Overvoltage Suppression in SiC MOSFET Bridges"
       • 期刊: ECCE (能源转换会议)
       • 年份: 2023
       • 引用数: 34
       • 应用场景: 电机驱动、逆变器

    统计分析:
    • 总相关论文: 1,247 篇 (2019-2024)
    • 年均增长: +23% (技术热点)
    • 主要机构: Virginia Tech (89 篇), ETH Zurich (67 篇), CPES (54 篇)
    • 主要期刊: IEEE TPEL (312 篇), APEC (189 篇), ECCE (156 篇)

    推荐行动:
    ✓ 重点阅读 [TPEL 2021] 和 [ISSCC 2023] 论文
    ✓ 下载 Virginia Tech 的开放预印本
    ✓ 参考 PowerIntegrations 的商用 IC 方案
```

### 示例 2: 引用关系分析

```
用户: 分析 "GaN power amplifier for 5G" 领域的关键论文和引用网络

AI: [调用 OpenAlex API - 引用关系查询]

    种子论文 (Seed Paper):
    "28 GHz GaN PA with 45% PAE for 5G Base Stations"
    • IEEE MTT 2022, 引用数: 312
    • DOI: 10.1109/TMTT.2022.1234567

    引用网络分析:

    ┌─────────────────────────────────────┐
    │ 被该论文引用的关键文献 (References) │
    └─────────────────────────────────────┘

    [1] "Doherty PA Linearization for 5G" (IEEE JSSC 2019)
        引用数: 567 → 📌 基础理论论文
        关键贡献: Doherty 架构数字预失真

    [2] "Thermal Management in GaN MMICs" (IEDM 2020)
        引用数: 423 → 📌 工程实现关键
        关键技术: 热阻分析、散热设计

    [3] "28 GHz GaN HEMT Process" (CSICS 2018)
        引用数: 289
        工艺参数: 0.15 μm gate, ft = 120 GHz

    ┌────────────────────────────────┐
    │ 引用该论文的后续研究 (Citing) │
    └────────────────────────────────┘

    [A] "39 GHz Wideband GaN PA for mmWave 5G" (RFIC 2023)
        引用数: 78 → 📌 技术延伸方向
        改进: 带宽扩展到 4 GHz

    [B] "Integrated GaN PA Module with Antenna" (APSURSI 2024)
        引用数: 23 → 📌 系统集成趋势
        创新: AiP (Antenna-in-Package) 技术

    [C] "AI-Assisted PA Bias Optimization" (IEEE Access 2024)
        引用数: 12 → 📌 新兴研究方向
        方法: 强化学习动态偏置

    引用网络可视化:

    [JSSC 2019] ──┐
    [IEDM 2020] ──┼──> [核心论文 MTT 2022] ──┬──> [RFIC 2023] (带宽扩展)
    [CSICS 2018] ─┘                          ├──> [APSURSI 2024] (集成封装)
                                             └──> [IEEE Access 2024] (AI 优化)

    研究趋势洞察:
    • 基础理论: Doherty 架构已成熟 (2019-)
    • 当前热点: 毫米波频段扩展 (28 → 39 GHz)
    • 未来方向: 1) 系统级集成 (AiP), 2) AI 辅助设计
    • 产业化: Qorvo, Wolfspeed 有相关产品

    推荐阅读路径:
    1. 先读 [JSSC 2019] 了解 Doherty 理论基础
    2. 再读 [核心论文 MTT 2022] 掌握 28 GHz 实现
    3. 最后读 [RFIC 2023] 和 [APSURSI 2024] 了解前沿趋势
```

### 示例 3: 按作者和机构查找

```
用户: 查找 ETH Zurich 在宽禁带半导体领域的代表性研究

AI: [调用 OpenAlex API - 机构和作者查询]

    机构: ETH Zurich (ROR: 05a28rw58)
    研究领域: Wide Bandgap Semiconductors (SiC, GaN)
    时间范围: 2019-2024

    查询结果:

    ═══════════════════════════════════
    ■ 领军学者 (Top Authors by Impact)
    ═══════════════════════════════════

    1. Prof. Johann W. Kolar
       • H-index: 89 (OpenAlex)
       • 论文数: 127 篇 (该领域)
       • 总引用: 12,347
       • 研究方向: 电力电子、高频变换器
       • 主页: https://pbl.ee.ethz.ch/

    2. Prof. Christian Franck
       • H-index: 56
       • 论文数: 78 篇
       • 研究方向: 高压电力电子、GaN 器件
       • 关键贡献: 超快速断路器技术

    ═════════════════════════════════
    ■ 代表性论文 (Top 5 by Citations)
    ═════════════════════════════════

    [1] "Ultra-High Power Density GaN-Based Inverter"
        • IEEE TPEL 2020, 引用数: 487
        • 作者: J.W. Kolar, et al.
        • 关键指标: 功率密度 13.2 kW/dm³ (世界纪录)
        • 技术亮点:
          - 三维集成封装
          - 液冷散热系统
          - 600 kHz 开关频率

    [2] "SiC-Based Solid-State Circuit Breaker for MVDC Grids"
        • ECCE 2021, 引用数: 312
        • 作者: C. Franck, et al.
        • 应用: 中压直流电网保护
        • 断开时间: < 1 μs

    [3] "GaN-on-Si Power Transistor with Field Plate"
        • IEDM 2022, 引用数: 267
        • 联合作者: IBM Research
        • 工艺创新: 应力工程、钝化层优化
        • 器件性能: RON = 1.2 mΩ·cm²

    [4] "Three-Phase GaN Inverter with Integrated EMI Filter"
        • APEC 2023, 引用数: 156
        • 创新: 平面磁集成、共模滤波
        • EMI 性能: 满足 CISPR 22 Class B (裕量 15 dB)

    [5] "Gate Driver IC for Cascode GaN HEMTs"
        • ISSCC 2024, 引用数: 89
        • 特点: 自适应死区时间、短路保护
        • 商用化: 与 Infineon 合作开发

    ═════════════════════════════════
    ■ 研究热点演变 (Topic Trends)
    ═════════════════════════════════

    2019-2020: SiC 基础器件特性
    2021-2022: GaN 高频应用 (1-3 MHz)
    2023-2024: 系统级集成、EMI 优化

    ═════════════════════════════════
    ■ 产学合作 (Industry Collaboration)
    ═════════════════════════════════

    • ABB: 中压直流断路器
    • Infineon: GaN 驱动 IC
    • Hitachi: 铁路牵引变流器

    推荐行动:
    ✓ 关注 J.W. Kolar 研究组的最新论文 (每年 APEC/ECCE 必有)
    ✓ 下载 [TPEL 2020] 论文学习高功率密度设计方法
    ✓ 参考 ETH 的开源仿真工具: GeckoCIRCUITS
```

### 示例 4: 研究趋势分析

```
用户: 分析 "电动汽车无线充电" 领域的研究趋势和技术演进

AI: [调用 OpenAlex API - 趋势分析]

    主题: "Wireless Power Transfer for Electric Vehicles"
    分析时间: 2015-2024 (10 年)

    ═════════════════════════════════════
    ■ 论文数量趋势 (Publication Trend)
    ═════════════════════════════════════

    Year │ Papers │ Growth │ Top Conference/Journal
    ─────┼────────┼────────┼────────────────────────
    2015 │   312  │   -    │ IEEE TPEL, ECCE
    2016 │   389  │ +24.7% │ APEC, EPE
    2017 │   467  │ +20.1% │ IEEE TVT, TIE
    2018 │   598  │ +28.1% │ IEEE TPEL (专题)
    2019 │   723  │ +20.9% │ ITEC, EVS
    2020 │   834  │ +15.4% │ ECCE, APEC
    2021 │   912  │  +9.4% │ IEEE TIE, TPEL
    2022 │  1045  │ +14.6% │ IEEE JESTPE (新刊)
    2023 │  1123  │  +7.5% │ eTransportation
    2024 │   634  │   ~    │ (截至 6月, 预计 1200+)

    📈 总体趋势:
    • 2015-2019: 快速增长期 (+20%/year) - 技术突破阶段
    • 2020-2024: 成熟发展期 (+10%/year) - 产业化阶段

    ═══════════════════════════════════════
    ■ 研究热点演变 (Topic Evolution)
    ═══════════════════════════════════════

    2015-2017: 基础技术
    ├─ 关键词: "coil design", "efficiency optimization"
    ├─ 标志论文: [TPEL 2016] "DD Coil Topology" (引用 892)
    └─ 里程碑: SAE J2954 标准发布 (2017)

    2018-2020: 系统集成
    ├─ 关键词: "misalignment tolerance", "foreign object detection"
    ├─ 标志论文: [IEEE VT 2019] "Real-Time FOD" (引用 567)
    └─ 里程碑: 功率等级提升到 11 kW (量产车)

    2021-2023: 高级功能
    ├─ 关键词: "dynamic charging", "bidirectional V2G"
    ├─ 标志论文: [eTransp 2022] "Dynamic WPT on Highway" (引用 312)
    └─ 里程碑: 欧洲试点道路动态充电项目

    2024-现在: 智能化
    ├─ 关键词: "AI-based control", "grid integration"
    ├─ 新兴方向: 强化学习优化、区块链能源交易
    └─ 产业趋势: V2G双向充电、光储充一体化

    ═══════════════════════════════════════
    ■ 关键技术指标演进 (Performance Metrics)
    ═══════════════════════════════════════

    指标           │  2015   │  2020   │  2024   │ 增长
    ───────────────┼─────────┼─────────┼─────────┼──────
    传输效率       │  85%    │  92%    │  95%    │ +12%
    功率等级       │  3.7 kW │  11 kW  │  22 kW  │ +495%
    气隙距离       │  100mm  │  150mm  │  200mm  │ +100%
    横向偏移容差   │  ±50mm  │  ±100mm │  ±150mm │ +200%
    FOD 检测精度   │   -     │  10mm   │  5mm    │  -
    成本 ($/kW)    │  $500   │  $300   │  $180   │  -64%

    ═══════════════════════════════════════
    ■ 产业化进展 (Commercialization)
    ═══════════════════════════════════════

    汽车厂商:
    • Genesis GV60 (2022): 全球首款量产 WPT 车型
    • BMW iX5 (2023): 11 kW 感应充电
    • BYD Han (2024): 国产 15 kW 无线充电

    充电设施:
    • WiTricity: 授权给 20+ 车厂
    • Qualcomm Halo: 被 WiTricity 收购
    • 国电南瑞: 中国市场领导者

    标准制定:
    • SAE J2954 (2020 Rev.): 11 kW, Z-class
    • ISO 19363 (2021): 磁场暴露安全
    • GB/T 38775 (2020): 中国国标 11 kW

    ═══════════════════════════════════════
    ■ 未来研究方向 (Future Directions)
    ═══════════════════════════════════════

    [高优先级]
    1. 动态充电 (Dynamic WPT)
       • 论文增长: +120% (2022-2024)
       • 技术挑战: 多线圈切换、实时功率控制
       • 试点项目: 德国 eRoadArlanda, 韩国 OLEV

    2. 超高功率充电 (>22 kW)
       • 需求驱动: 商用车、重卡
       • 技术瓶颈: 散热、EMI、安全
       • 论文增长: +85%

    3. V2G 双向充电
       • 应用场景: 电网调峰、应急供电
       • 论文增长: +67%
       • 产业标准: IEEE 2030.1.1 (起草中)

    [新兴方向]
    4. AI 优化控制
       • 强化学习自适应匹配
       • 神经网络异物检测

    5. 区块链能源管理
       • 去中心化充电交易
       • 智能合约自动结算

    推荐行动:
    ✓ 重点关注 "dynamic charging" 和 "V2G" 研究
    ✓ 跟踪 IEEE JESTPE 和 eTransportation 期刊
    ✓ 参考 SAE J2954 和 GB/T 38775 标准
    ✓ 研究 WiTricity 和国电南瑞的专利布局
```

## 故障排除

### 问题: API 请求失败

**解决方案**:
1. 检查网络连接（OpenAlex API: https://api.openalex.org）
2. 验证 pyalex 库版本（需要 >= 0.10）
3. OpenAlex 无需 API 密钥，但建议添加 User-Agent 邮箱：
   ```python
   import pyalex
   pyalex.config.email = "your.email@example.com"
   ```

### 问题: 搜索结果不准确

**解决方案**:
1. 使用更精确的技术术语和缩写
2. 添加年份范围过滤（`from_publication_date="2020-01-01"`）
3. 指定研究领域 (`concepts.id:`)
4. 检查拼写（OpenAlex 支持模糊匹配但准确度下降）

### 问题: 无法访问全文

**解决方案**:
1. 检查 OA 状态（OpenAlex 标注开放获取类型）
2. 查找预印本版本（arXiv, HAL, ResearchGate）
3. 使用机构图书馆数据库访问
4. 联系作者请求副本（email 通常在论文中）

## 技术细节

### API 使用示例

```python
import pyalex
from pyalex import Works

# 配置邮箱（礼貌的 API 使用）
pyalex.config.email = "your.email@example.com"

# 按主题搜索论文
works = Works().search("GaN HEMT power amplifier").get()

# 按年份和引用数过滤
recent_influential = (
    Works()
    .search("SerDes equalization")
    .filter(publication_year=">2020")
    .sort(cited_by_count="desc")
    .get(per_page=10)
)

# 按作者查找
author_works = Works().filter(author={"id": "A1234567890"}).get()

# 按机构查找
eth_papers = (
    Works()
    .filter(institutions={"ror": "05a28rw58"})  # ETH Zurich ROR ID
    .filter(concepts={"id": "C12345"})  # Power Electronics
    .get()
)

# 获取引用关系
citing_papers = Works().filter(cites="W1234567890").get()
```

### API 限制

- **请求频率**: 10 万次/天（免费，无需注册）
- **加 polite 模式**: 添加邮箱后提升到 100 次/秒
- **响应时间**: 通常 < 1 秒
- **数据更新**: 每周更新一次

### 数据覆盖

- **论文数量**: 250M+ (截至 2024)
- **时间跨度**: 1900 年至今
- **引用关系**: 1.8B+ 引用链接
- **开放获取**: 标注 OA 状态和链接

## 与其他 Skills 的协同

### openalex-database + perplexity-search

```
场景: OpenAlex 提供学术背景，Perplexity 查找应用案例

1. openalex-database: 查找 "GaN HEMT" 学术论文
   → 获取理论基础和技术参数

2. perplexity-search: "GaN HEMT power amplifier products"
   → 找到商用产品和数据手册
```

### openalex-database + arxiv-search

```
场景: OpenAlex 找到论文元数据，arXiv 获取预印本全文

1. openalex-database: 搜索 "machine learning circuit design"
   → 找到相关论文列表和 DOI

2. arxiv-search: 用论文标题在 arXiv 查找
   → 下载免费预印本 PDF
```

### openalex-database + docs-seeker

```
场景: 学术论文提供理论，本地文档提供实现

1. openalex-database: "DDR5 signal integrity analysis"
   → 学术方法和分析工具

2. docs-seeker: 在本地查找 "DDR5 datasheet"
   → 具体器件参数和设计指南
```

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
