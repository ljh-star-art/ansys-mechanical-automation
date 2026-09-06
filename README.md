# ANSYS Mechanical Automation

使用 Python、PyMechanical 和 MCP 自动执行 ANSYS Mechanical 2024 R2 静力结构分析。

当前示例为三维弯曲梁（`Bending_3D_Beam`），已验证网格划分、静力求解、结果提取、结果分析和 Codex 调用流程。

## 项目结构

```text
mechanical-automation/
├─ mcp_server.py
├─ pymechanical_smoke_test.py
├─ requirements.txt
├─ Bending_3D_Beam/
│  ├─ beam.wbpj
│  ├─ run_static.py
│  ├─ pymechanical_model_test.py
│  ├─ run_pipeline.py
│  ├─ analyze_results.py
│  ├─ results/
│  └─ beam_files/             # ANSYS 生成目录，默认不提交
└─ td-007/                    # 几何模型输入
```

## 环境要求

- Windows
- ANSYS Mechanical 2024 R2
- 可用 ANSYS 许可证
- Python 3.12（当前测试环境为 `C:\Pyth0n31210\python.exe`）
- `ansys-mechanical-core`
- MCP Python SDK 2.x

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

## 虚拟环境

项目推荐在根目录使用一个统一的虚拟环境，所有算例共享同一套 PyMechanical 和 MCP 依赖。创建并激活：

```powershell
C:\Pyth0n31210\python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

如果 PowerShell 阻止激活脚本，可以不激活，直接使用虚拟环境解释器：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\Bending_3D_Beam\run_pipeline.py
```

`.venv` 已加入 `.gitignore`，不会上传到 GitHub。克隆仓库后，每台电脑都应在本地重新创建自己的 `.venv`。

安装依赖后，MCP Server 也应改用虚拟环境中的 Python 重新注册：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp remove ansys-mechanical
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp add ansys-mechanical -- "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\.venv\\Scripts\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
```

## 运行 PyMechanical 连通性测试

```powershell
python .\pymechanical_smoke_test.py
```

成功时应看到：

```text
PyMechanical connection succeeded.
Mechanical evaluated 1 + 1 as: 2
```

## 运行弯曲梁仿真

关闭手动打开的 Workbench/Mechanical，然后执行：

```powershell
python .\Bending_3D_Beam\run_pipeline.py
```

流程为：

```text
启动 Mechanical
→ 加载 SYS.mechdb
→ 执行 run_static.py
→ 生成网格
→ 静力求解
→ 保存结果
→ 分析应力阈值
```

标准结果文件为：

```text
Bending_3D_Beam\results\latest_results.json
```

单独分析已有结果：

```powershell
python .\Bending_3D_Beam\analyze_results.py
```

## ANSYS 启动程序路径

当前测试机器使用：

```text
D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe
```

如果更换机器或 ANSYS 版本，需要修改 `Bending_3D_Beam\pymechanical_model_test.py` 中的 `MECHANICAL_EXE`。

## 使用 MCP

注册 MCP Server（只需一次）：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp add ansys-mechanical -- "C:\\Pyth0n31210\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
```

检查注册状态：

```powershell
C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp list
```

重启 Codex 后，可以调用：

```text
run_static_analysis
read_latest_results
```

## 可复现性说明

`Bending_3D_Beam\pymechanical_model_test.py` 需要加载 ANSYS 生成的 `SYS.mechdb`。该文件位于 `beam_files` 目录中，通常是二进制数据库和缓存的一部分。

当前仓库默认不提交 `beam_files`，因此其他人克隆代码后可以看到脚本和文档，但不能保证直接执行弯曲梁自动化流程。要实现完全可复现，需要额外提供模型数据库，通常有两种方案：

1. 使用 Git LFS 上传必要的 `SYS.mechdb` 和相关模型文件；
2. 提供初始化步骤，让用户先在 Workbench 中打开 `beam.wbpj` 并生成对应数据库。

详细初始化步骤见 `Bending_3D_Beam\模型初始化.md`。

## 注意事项

- `run_static.py` 只能在 Mechanical 内部 Python 环境中执行；
- 普通 Python 负责启动和控制 Mechanical；
- `beam_files` 不应手动编辑；
- `results/latest_results.json` 是项目级标准结果，可提交用于示例和回归测试；
- `transport_mode="insecure"` 仅用于本机测试，不建议用于远程或不可信网络。
- 当前 `case_config.json` 已保存载荷、方向和约束字段，并传入求解上下文；实际修改 Mechanical 中已有载荷对象前，需要先确认模型树中的载荷对象名称和 API 属性。
- 当前版本的 `load_value_n`、`load_direction` 和 `constraint` 已完成输入建模、校验和日志记录，但尚未自动修改已有 Mechanical 载荷/约束对象；网格参数已实际用于求解。
