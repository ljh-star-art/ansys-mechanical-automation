# ANSYS Mechanical 官方案例简版调研

## 1. 结论

这两套官方包都属于 ANSYS Mechanical 结构仿真示例，不是 Fluent CFD。

- MAPDL 包：更偏脚本驱动，很多案例同时有几何 + 网格 + 求解输入
- Workbench 包：更偏几何驱动，适合 SpaceClaim / DesignModeler 工作流
- 绝大多数案例都属于结构力学方向：静力、接触、模态、瞬态、热/热-结构、管道/转子、断裂/生物力学

## 2. PyMechanical vs PyMAPDL

### 更适合做 Mechanical 智能体：PyMechanical

原因：
- 它更贴近 Mechanical / Workbench 的真实工作流
- 更适合做“建模 → 网格 → 求解 → 后处理”这一整链路自动化
- 更适合你以后做 agent 的统一接口

### PyMAPDL 更适合做什么

- 直接控制 MAPDL / APDL 命令和 .dat 脚本
- 适合“低层、脚本型、求解器级”自动化
- 对纯 MAPDL 案例特别适合

### 最佳组合

- 统一 agent 架构：PyMechanical 为主
- MAPDL 例子：PyMAPDL 作为底层脚本执行器
- 这样你既能覆盖 Workbench 也能覆盖原生 MAPDL

## 3. 先做哪个 SpaceClaim + Mechanical 例子

如果你现在要走 SpaceClaim + Mechanical 路线，推荐优先从：

- td-007（最接近 SpaceClaim + Mechanical 的官方示例）
  - 有 `td7_full_3D_Model.scdoc`
  - 还有 `td7_general_axisymmetric_model.agdb`
  - 几何来源和 Workbench 结构都比较完整

如果你更看重“几何 + 网格文件都存在”，则优先从：

- td-4（MAPDL 例子）
  - `ringforging.cdb`
  - `mesh1.cdb`
  - `mesh2.cdb`
  - `ringforging.dat`

这个例子其实更适合做“agent 的第一条最稳脚本路径”，因为它同时具备几何和网格文件。

> 结论：
> - 追求 SpaceClaim + Mechanical 工作流：先 td-007
> - 追求“几何 + 网格 + 求解闭环”：先 td-4

## 4. 有几何 / 没几何 / 只有网格

| 包 | 总案例数 | 几何+数据混合 | 仅几何 | 仅数据/网格 |
|---|---:|---:|---:|---:|
| MAPDL | 64 | 45 | 1 | 18 |
| Workbench | 33 | 1 | 26 | 0 |

### 结论

- MAPDL：更像脚本型 / 网格型研究案例，适合自动化脚本测试
- Workbench：更像几何建模型案例，适合真正的 Mechanical 工作流

## 5. SpaceClaim / DesignModeler 判断

- SpaceClaim：`*.scdoc`，说明是参数化几何建模
- DesignModeler：`*.agdb`，更接近 Workbench 内部几何建模

在这批案例里：
- Workbench 包多数更接近 DesignModeler/Workbench 几何驱动
- 部分案例确实使用了 SpaceClaim（例如 `*.scdoc`）

## 6. 仿真类型概览

| 类型 | 说明 |
|---|---|
| Static / Contact / Structural | 静力、接触、非线性结构 |
| Modal / Vibration | 模态、振动 |
| Dynamic / Transient | 瞬态动力学 |
| Thermal / Thermo-structural | 热分析、热-结构耦合 |
| Piping / Rotor / Elbow | 管道、转子、弯管 |
| Damage / Fracture / Composite | 损伤、断裂、复合材料 |
| Biomechanics | 生物力学、人体/器官结构 |

## 7. 最适合 agent 起步的例子

建议按顺序：

1. `td-1`（MAPDL）
2. `td-4`（MAPDL）
3. `td-007`（Workbench / SpaceClaim）
4. `td-006`（Workbench）
5. `td-008`（Workbench）

这样能覆盖：
- 直接脚本驱动
- 几何驱动
- 多模型分支
- 真正机械仿真闭环

## 8. 一句话建议

如果你的目标是做一套“围绕 Ansys Mechanical 的智能体”，最稳妥的路线是：

- 统一用 PyMechanical 做主控制层
- 在 MAPDL 例子里补 PyMAPDL
- 第一批案例先做 `td-4` + `td-007`

这样既能把脚本型 MAPDL 例子做起来，也能顺着 SpaceClaim + Workbench 方向继续扩展。