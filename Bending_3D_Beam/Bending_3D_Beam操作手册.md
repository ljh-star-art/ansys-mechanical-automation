# Bending 3D Beam 自动化操作手册

## 1. 项目位置

```text
D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation\Bending_3D_Beam
```

本案例使用 ANSYS Mechanical 2024 R2，已验证三维弯曲梁静力分析流程，包括网格划分、求解、结果提取和外部自动化调用。

## 2. 关键文件

| 文件 | 作用 |
|---|---|
| `beam.wbpj` | Workbench 项目文件，仅用于手动确认基准算例 |
| `run_static.py` | Mechanical 内部脚本，执行网格、求解和结果提取 |
| `mesh_solve.py` | Mechanical 内部网格和求解脚本 |
| `mesh_solve2.py` | Mechanical 内部网格和求解脚本变体 |
| `pymechanical_model_test.py` | 外部 PyMechanical 模型加载和求解测试 |
| `run_pipeline.py` | 一键执行求解和结果分析 |
| `analyze_results.py` | 读取并判断最近一次结果 |
| `beam_files/` | ANSYS 内部数据库和缓存目录 |
| `results/latest_results.json` | 项目级标准结果文件 |

`run_static.py` 中的 `Model`、`ExtAPI` 和 `Quantity` 只能在 Mechanical 内部环境中使用，不能直接用普通 Python 执行。

## 3. 不使用 MCP

调用关系：

```text
Codex → 终端命令 → Python 脚本 → PyMechanical → Mechanical
```

### 3.1 启动 Codex

在 PowerShell 中执行：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd
```

如果 PowerShell 允许执行脚本，也可以执行：

```powershell
codex
```

`codex.cmd` 是 Windows 下 Codex CLI 的启动入口。使用它可以绕过当前 PowerShell 对 `codex.ps1` 的执行限制。

### 3.2 让 Codex 执行完整仿真

在 Codex 会话中输入：

```text
请在终端执行 C:\\Pyth0n31210\\python.exe .\\Bending_3D_Beam\\run_pipeline.py，并报告求解状态和关键结果。
```

对应的实际命令为：

```powershell
cd D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
C:\Pyth0n31210\python.exe .\Bending_3D_Beam\run_pipeline.py
```

### 3.3 读取结果

结果文件为：

```text
Bending_3D_Beam\results\latest_results.json
```

如需单独分析已有结果，在 Codex 中输入：

```text
请在终端执行 C:\\Pyth0n31210\\python.exe .\\Bending_3D_Beam\\analyze_results.py，并报告最大变形、最大应力和阈值判断。
```

## 4. 使用 MCP

调用关系：

```text
Codex → MCP 工具 → mcp_server.py → run_pipeline.py → PyMechanical → Mechanical
```

### 4.1 注册 MCP Server

只需注册一次：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp add ansys-mechanical -- "C:\\Pyth0n31210\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
```

检查注册状态：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp list
```

必须看到：

```text
ansys-mechanical ... enabled
```

### 4.2 调用 MCP 工具

完全退出并重新启动 Codex：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd
```

在新会话中输入：

```text
列出所有可用的 MCP 工具。
```

确认存在：

```text
run_static_analysis
read_latest_results
```

执行完整仿真：

```text
调用 run_static_analysis，执行一次弯曲梁静力分析，并报告求解状态、最大总变形和最大等效应力。
```

读取已有结果：

```text
调用 read_latest_results，读取最近一次弯曲梁静力分析结果。
```

有效结果应满足：

```text
success: true
return_code: 0
result_is_current: true
```

## 5. PyMechanical 启动程序

本机 ANSYS Mechanical 2024 R2 的启动程序为：

```text
D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe
```

该路径已写入 `pymechanical_model_test.py`。如果更换电脑或 ANSYS 版本，需要更新 `MECHANICAL_EXE`。

2024 R2 低于 SP05 时使用本机测试模式：

```python
transport_mode="insecure"
```

这是本机 gRPC 连通性测试配置，不建议用于远程或不可信网络。

## 6. 两种方式对比

| 项目 | 不使用 MCP | 使用 MCP |
|---|---|---|
| 调用方式 | Codex 执行终端命令 | Codex 调用命名工具 |
| 脚本路径 | 每次需要明确 | 由 Server 管理 |
| 结果返回 | 读取终端和 JSON 文件 | 结构化字段返回 |
| 调试便利性 | 高 | 中 |
| 智能体扩展性 | 需要自行拼接命令 | 便于增加参数和决策逻辑 |

## 7. 目录建议

案例专属文件放在本目录；根目录只保留通用入口：

```text
mechanical-automation/
├─ mcp_server.py
├─ pymechanical_smoke_test.py
├─ requirements.txt
└─ Bending_3D_Beam/
   ├─ beam.wbpj
   ├─ run_static.py
   ├─ mesh_solve.py
   ├─ mesh_solve2.py
   ├─ pymechanical_model_test.py
   ├─ run_pipeline.py
   ├─ analyze_results.py
   ├─ Bending_3D_Beam操作手册.md
   ├─ beam_files/
   └─ results/
```
