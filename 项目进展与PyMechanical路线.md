# ANSYS Mechanical 自动化项目进展

## 1. 项目目标

本项目使用 ANSYS Mechanical 2024 R2，逐步实现结构仿真的自动化，并最终形成可上传 GitHub 的项目。当前分析类型以静力分析为优先，目标流程包括：

1. 导入几何模型
2. 设置材料、边界条件和载荷
3. 自动网格划分
4. 自动求解
5. 提取总变形、等效应力等结果
6. 由外部 Python、MCP 和智能体完成任务调度

## 2. 当前算例

当前使用的是三维弯曲梁案例，项目目录为：

```text
D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation\Bending_3D_Beam
```

该案例此前已经在 Workbench/Mechanical 图形界面中成功求解，用于对比自动化结果。

## 3. 已完成内容

### 3.1 Mechanical 内部脚本

以下脚本运行在 ANSYS Mechanical 内部的 Scripting 窗口中，使用 Mechanical 的 IronPython/API：

- `Bending_3D_Beam\mesh_solve.py`
- `Bending_3D_Beam\mesh_solve2.py`
- `Bending_3D_Beam\run_static.py`

已验证的功能包括：

- 自动设置或更新网格参数；
- 生成网格；
- 执行静力求解；
- 获取 Total Deformation（总变形）；
- 获取 Equivalent Stress（等效应力）；
- 将结果写入 `beam_files\latest_results.json`。

由于 Mechanical 2024 R2 内置 IronPython 环境导入标准 `json` 模块时可能出现 `ImportError: No module named _json`，结果文件采用手动拼接 JSON 文本的方式输出，避免依赖该模块。

### 3.2 结果验证

`run_static.py` 已在 Mechanical 中运行成功，并且与原有 Workbench 算例结果一致。说明 Mechanical 内部的网格、求解和结果提取流程已经打通。

Mechanical 内部原始结果文件位置：

```text
Bending_3D_Beam\beam_files\latest_results.json
```

通过 PyMechanical 外部驱动后，项目统一结果文件写入：

```text
Bending_3D_Beam\results\latest_results.json
```

该目录是项目级输出目录，便于后续 MCP 工具和智能体读取；`beam_files` 下的文件属于 ANSYS 内部缓存和求解数据库。

### 3.3 外部 PyMechanical 测试脚本

项目根目录新增：

```text
pymechanical_smoke_test.py
```

该脚本的用途是验证外部 CPython 是否能够启动并连接 ANSYS Mechanical 2024 R2。测试内容为：

1. 启动 Mechanical；
2. 通过 PyMechanical 执行一条简单脚本；
3. 输出 Mechanical 版本；
4. 退出 Mechanical。

它不负责网格或求解，属于外部控制层的最小连通性测试。

## 4. PyMechanical 测试方法

### 4.1 安装依赖

在 PowerShell 中进入项目目录，使用普通 CPython 执行：

```powershell
cd D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
python -m pip install --upgrade pip
python -m pip install ansys-mechanical-core
```

注意：不要在 Mechanical 内部的 IronPython 窗口执行上述安装命令。

### 4.2 检查模块

```powershell
python -c "from ansys.mechanical.core import launch_mechanical; print('package ok')"
```

### 4.3 执行冒烟测试

```powershell
python .\pymechanical_smoke_test.py
```

预期输出类似：

```text
PyMechanical connection succeeded.
Mechanical evaluated 1 + 1 as: 2
```

首次启动可能需要几十秒。运行前应确认 ANSYS Mechanical 2024 R2 已安装、许可证服务正常，并且 `version=242` 与安装版本匹配。

对于未升级到 SP05 的 2024 R2，需在 `launch_mechanical` 中明确设置 `transport_mode="insecure"`。这是本机的本地连通性测试模式，不使用认证或加密；不要将该模式用于远程或不可信网络。

当前记录：项目环境曾检查到 `ansys-mechanical-core` 尚未安装，因此需要先完成安装再运行测试。

## 5. 脚本与智能体的职责划分

当前已经完成的是“仿真执行脚本层”，还不是完整智能体。建议采用以下分层架构：

```text
用户需求
   ↓
Codex/智能体：解析任务、选择参数、检查结果、决定下一步
   ↓
MCP 工具层：提供启动、执行脚本、读取结果等标准工具
   ↓
PyMechanical：从外部 Python 连接和控制 Mechanical
   ↓
Mechanical 内部脚本：网格、求解、后处理
   ↓
latest_results.json：结构化结果
```

其中，Mechanical 内部脚本负责确定性的工程操作；智能体负责理解自然语言、生成或修改参数、调用工具、判断求解是否成功以及决定是否需要重新计算。

## 6. 当前尚未完成内容

- 安装并验证 `ansys-mechanical-core`；
- 确认 PyMechanical 能启动 2024 R2；
- 编写外部驱动脚本，打开项目并调用 `run_static.py`；
- 将结果读取、错误处理和日志整理成可复用模块；
- 增加结果分析脚本，对最大变形和应力进行阈值判定；
- 增加统一入口脚本，串联求解和结果分析；
- 封装 MCP Server/Tools；
- 增加智能体对网格尺寸、载荷和结果阈值的决策逻辑；
- 增加 README、依赖文件、示例和 GitHub 发布说明。

## 7. 下一步执行顺序

1. 安装 `ansys-mechanical-core`；
2. 运行 `pymechanical_smoke_test.py`；
3. 记录启动成功或完整错误信息；
4. 编写外部驱动脚本，调用现有 `run_static.py`；
5. 从 `latest_results.json` 读取结果并打印摘要；
6. 使用 `analyze_results.py` 进行结果阈值判定；
7. 使用 `run_pipeline.py` 串联完整流程；
8. 使用 `mcp_server.py` 暴露静力分析和结果读取工具；
9. 配置 MCP 客户端并进行工具调用测试；
10. 增加智能体对参数和结果的决策逻辑。

## 9. MCP 初步实现

项目根目录新增 `mcp_server.py`。它使用 MCP Python SDK 的 stdio 模式，提供：

- `run_static_analysis`：执行 `run_pipeline.py`，返回求解日志和结构化结果；
- `read_latest_results`：读取 `Bending_3D_Beam\\results\\latest_results.json`。

安装依赖（当前 Server 使用 MCP 2.x API）：

```powershell
python -m pip install -r requirements.txt
```

启动 MCP Server：

```powershell
python .\\mcp_server.py
```

Server 启动后等待 MCP 客户端通过 stdio 发送工具调用。直接运行时不会自动求解，只有调用 `run_static_analysis` 工具才会启动 Mechanical。

在 Codex CLI 中注册该 Server（PowerShell）：

```powershell
codex mcp add ansys-mechanical -- "C:\\Pyth0n31210\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
codex mcp list
```

如果 PowerShell 阻止 `codex.ps1`，使用 `codex.cmd` 替代 `codex`。注册后重启 Codex 会话，在新会话中即可调用 `run_static_analysis` 和 `read_latest_results`。

## 10. 实际操作记录

### 10.1 PyMechanical 冒烟测试

首先运行：

```powershell
python .\\pymechanical_smoke_test.py
```

初始测试使用安全 gRPC 传输时，2024 R2 返回了“不支持 secure transport”的错误。随后在 `launch_mechanical` 中增加：

```python
transport_mode="insecure"
```

再次运行后成功输出：

```text
PyMechanical connection succeeded.
Mechanical evaluated 1 + 1 as: 2
```

这证明外部 CPython 可以启动 Mechanical 并建立 PyMechanical 连接。TLS 警告是因为本机使用非加密 gRPC，属于预期提示。

### 10.2 基准模型确认

双击 `Bending_3D_Beam\\beam.wbpj`，在 Workbench 中双击 `Model` 进入 Mechanical。确认模型树中的 `Mesh`、`Static Structural` 和 `Solution` 均存在且显示绿色勾。

这一步只用于确认原始 Workbench 算例、边界条件、网格和已有结果正常，不用于测试 PyMechanical，也不要求手动再次求解。

### 10.3 PyMechanical 模型求解

关闭手动打开的 Workbench/Mechanical 后，运行：

```powershell
python .\\pymechanical_model_test.py
```

脚本启动 Mechanical，加载：

```text
Bending_3D_Beam\\beam_files\\dp0\\global\\MECH\\SYS.mechdb
```

然后调用 `run_static.py`，自动完成网格生成、静力求解和结果提取。

由于通过数据库加载后 `ExtAPI.DataModel.Project.ProjectDirectory` 指向 ANSYS 内部目录，原始结果实际写入：

```text
Bending_3D_Beam\\beam_files\\dp0\\global\\MECH\\SYS_Mech_Files\\latest_results.json
```

### 10.4 统一项目结果目录

`pymechanical_model_test.py` 随后将原始结果复制到项目级目录：

```text
Bending_3D_Beam\\results\\latest_results.json
```

该目录用于后续 MCP 工具和智能体读取，不依赖 ANSYS 内部缓存目录。

### 10.5 结果分析

运行：

```powershell
python .\\analyze_results.py
```

脚本读取标准结果文件，解析最大总变形和最大等效应力，并按照配置的应力阈值进行判断。当前一次验证结果为：

```text
Maximum deformation (m): 5.5702551009067274e-05
Maximum equivalent stress (Pa): 2388484.473988054
Decision: result is within the configured stress limit
```

### 10.6 一键流水线

运行：

```powershell
python .\\run_pipeline.py
```

该脚本依次执行 `pymechanical_model_test.py` 和 `analyze_results.py`，实现启动 Mechanical、加载模型、网格、求解、结果保存和结果判定的一键执行。

### 10.7 MCP Server 安装与兼容处理

项目使用 `mcp_server.py` 提供 `run_static_analysis` 和 `read_latest_results` 两个工具。最初代码使用 MCP 1.x 的 `FastMCP` API，但本机安装的是 MCP 2.x，因此出现：

```text
No module named 'mcp.server.fastmcp'
```

随后将 Server 改为 MCP 2.x API：使用 `MCPServer`、`@server.tool()` 和 `server.run("stdio")`。`requirements.txt` 固定为：

```text
mcp>=2,<3
```

并通过以下命令验证模块可导入：

```powershell
python -c "import mcp_server; print('MCP server import ok')"
```

### 10.8 注册到 Codex

由于 PowerShell 阻止 `codex.ps1`，使用 `codex.cmd` 注册：

```powershell
C:\\Users\\luo\\AppData\\Roaming\\npm\\codex.cmd mcp add ansys-mechanical -- "C:\\Pyth0n31210\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
```

检查配置：

```powershell
C:\\Users\\luo\\AppData\\Roaming\\npm\\codex.cmd mcp list
```

最终显示：

```text
ansys-mechanical ... enabled
```

这表示 MCP Server 已成功注册为 Codex 的全局 stdio Server。`Auth: Unsupported` 对本地 stdio Server 是正常现象，因为它不使用远程认证。

## 11. 当前完成状态

目前已经完成：

- Mechanical 内部网格、静力求解和结果提取；
- PyMechanical 外部启动和连接；
- PyMechanical 加载模型并执行求解；
- 统一结果目录和结果分析；
- 一键流水线；
- MCP Server 工具封装；
- MCP Server 注册到 Codex。

后续可在新的 Codex 会话中调用 `run_static_analysis` 和 `read_latest_results`，再继续增加可调网格尺寸、载荷参数、结果阈值和智能体决策逻辑。

## 8. 重要注意事项

- Mechanical 内部脚本和外部 PyMechanical 脚本运行在不同 Python 环境中；
- Mechanical 内部环境可能不支持完整 CPython 标准库；
- 外部脚本中的路径应使用当前项目目录，避免引用旧的 `Bending_3D_Beam` 路径；
- 运行自动化前应保留一个可手动打开并求解的基准算例；
- 每次自动求解都应保存日志和结果文件，便于与基准结果对比。
