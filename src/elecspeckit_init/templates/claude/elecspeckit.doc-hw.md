---
description: 为硬件工程师生成硬件设计视图文档
handoffs: []
---

## Command: `/elecspeckit.doc-hw`

**Goal**
基于当前硬件特性的 `spec.md`、`plan.md` 与 `tasks.md`，为硬件工程师生成专属的硬件设计视图文档 `docs/hw-view.md`，聚焦架构模块、设计任务和设计文件路径。

**Execution Steps (for the AI assistant)**
1. 在目标项目根目录工作，与用户确认当前特性的 `FEATURE_DIR = specs/00X-shortname/`，并在其中定位：
   - `FEATURE_SPEC   = FEATURE_DIR/spec.md`；
   - `IMPL_PLAN      = FEATURE_DIR/plan.md`；
   - `FEATURE_TASKS  = FEATURE_DIR/tasks.md`；
   - `FEATURE_DOCS   = FEATURE_DIR/docs/`（如不存在，则创建）。

2. 从 `plan.md` 中提取架构模块定义：
   - 读取 `plan.md` 中的架构规划章节（如"功能模块框图"、"模块间接口定义"）；
   - 识别关键功能模块（如 AC Input Filter Module, PFC Module, Isolated DC-DC Module 等）；
   - 提取每个模块的输入接口、输出接口、关键参数和约束条件。

3. 从 `tasks.md` 中提取 `[VIEW:HW]` 标记的任务：
   - 扫描 `tasks.md` 中所有任务描述；
   - 筛选包含 `[VIEW:HW]` 标记的任务；
   - 按任务ID或阶段排序，方便硬件工程师追溯。

4. 处理 `[MANUAL]` 任务的设计文件路径：
   - 对于标记为 `[MANUAL]` 的硬件设计任务（如"原理图设计"、"PCB布局设计"）；
   - 提取任务描述中的设计文件路径引用（如 `hardware/schematics/power-module.sch`）；
   - 在硬件视图文档中建立任务与设计文件的关联，方便硬件工程师快速定位。

5. 生成 `FEATURE_DIR/docs/hw-view.md`：
   - **架构模块**：列出从 `plan.md` 提取的模块定义、接口和参数；
   - **设计任务清单**：列出所有 `[VIEW:HW]` 任务，包括任务ID、描述、状态（待完成/进行中/已完成）；
   - **设计文件索引**：列出 `[MANUAL]` 任务关联的设计文件路径，建立任务到文件的映射；
   - **技术约束**：从 `spec.md` 提取硬件相关的技术约束（如电压范围、功率要求、PCB尺寸、EMC标准）；
   - **设计检查清单**：基于宪法中的"硬件设计规范"和"可靠性要求"，列出设计检查项（如降额设计、热设计、DFM检查）。

6. 向用户总结：
   - 本次生成的 `hw-view.md` 包含了哪些架构模块和设计任务；
   - 提醒硬件工程师关注的关键设计检查项；
   - 建议下一步操作（如"补充 research.md 中的拓扑选型决策"、"执行 DFM 评估"）。

**Notes**
- `/elecspeckit.doc-hw` 专注于硬件工程师视角，不涉及软件、BOM或测试相关任务；
- 硬件视图文档应与 `plan.md` 中的架构模块定义保持一致，任何不一致应通过 `/elecspeckit.plan` 回流修正；
- `[VIEW:HW]` 标记用于在 `tasks.md` 中标识硬件相关任务，确保任务拆分时正确标记；
- `[MANUAL]` 标记的任务需要人工完成，AI助手不应自动执行这些任务，但应在视图文档中突出显示并提供设计文件路径引用。

**Example: 硬件视图文档结构**

```markdown
# 硬件设计视图: 60W PD充电头

## 架构模块

### AC Input Filter Module
- **输入接口**: 85-265VAC, 47-63Hz
- **输出接口**: 滤波后AC, EMI等级 Class B
- **关键参数**: 共模电感 10mH, 差模电容 0.47µF X2
- **约束条件**: IEC 62368-1 基本绝缘, -10°C~+50°C

### PFC Module
- **输入接口**: 滤波后AC
- **输出接口**: 母线电压 380-400VDC
- **关键参数**: 效率目标 >95%, 功率因数 >0.95
- **约束条件**: THD <20%, 满足 EN 61000-3-2 Class A

## 设计任务清单

- [ ] T012 [MANUAL] [VIEW:HW] 设计AC输入滤波电路原理图 → `hardware/schematics/ac-filter.sch`
- [ ] T015 [MANUAL] [VIEW:HW] 设计PFC升压电路原理图 → `hardware/schematics/pfc-boost.sch`
- [x] T021 [AUTO] [VIEW:HW] 从参考设计提取LLC变压器参数 → `research.md`

## 设计文件索引

- `hardware/schematics/ac-filter.sch` ← T012 AC输入滤波电路
- `hardware/schematics/pfc-boost.sch` ← T015 PFC升压电路
- `hardware/pcb/power-board-layout.pcb` ← T025 PCB布局设计

## 技术约束

- 输入电压范围: 85-265VAC
- 输出功率: 65W (5V/9V/12V/15V/20V @ 3A)
- 效率目标: DoE Level VI (>94% @ 满载, >85% @ 轻载)
- 隔离耐压: 4000VAC @ 60s
- PCB尺寸: 待定（参考外壳设计）
- EMC标准: CISPR 32 Class B

## 设计检查清单

- [ ] 半导体器件降额检查 (Vds/Vdss ≥ 1.5x)
- [ ] 电容耐压降额检查 (≥ 1.25x)
- [ ] 热设计与温升测试 (变压器表面 <80°C @ 25°C环境, 满载)
- [ ] 爬电距离检查 (加强绝缘 ≥6.4mm per IEC 62368-1)
- [ ] DFM评估 (可制造性设计，见 `/elecspeckit.doc-fa`)
```
