# ANSYS Mechanical 自动化使用方式

## 一、不使用 MCP：Codex 调用终端命令

调用关系：

```text
Codex → 终端命令 → Python 脚本 → PyMechanical → Mechanical
```

### 操作步骤

1. 确认 `pymechanical_model_test.py` 中的 `MECHANICAL_EXE` 指向本机真实的 Mechanical 启动程序：

   ```text
   D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe
   ```

2. 关闭手动打开的 Workbench/Mechanical 窗口。
3. 在 Codex 中要求执行，或者直接在终端运行：

   ```powershell
   cd D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
   python .\run_pipeline.py
   ```

4. `run_pipeline.py` 会依次执行 `pymechanical_model_test.py` 和 `analyze_results.py`。
5. 检查结果文件：

   ```text
   Bending_3D_Beam\results\latest_results.json
   ```

6. 如果只想分析已有结果，可单独执行：

   ```powershell
   python .\analyze_results.py
   ```

这种方式不需要 MCP，但 Codex 每次都需要知道脚本路径、命令和结果文件位置；如果要增加参数，通常需要修改脚本或手动拼接命令行参数。

## 二、使用 MCP：Codex 调用结构化工具

调用关系：

```text
Codex → MCP 工具 → mcp_server.py → run_pipeline.py → PyMechanical → Mechanical
```

### 操作步骤

1. 检查 MCP Server 是否已经注册：

   ```powershell
   C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp list
   ```

2. 确认输出包含：

   ```text
   ansys-mechanical ... enabled
   ```

3. 重启 Codex 会话，使 MCP 配置生效。
4. 在 Codex 中请求：

   ```text
   调用 run_static_analysis，执行一次弯曲梁静力分析。
   ```

5. 读取已有结果时请求：

   ```text
   调用 read_latest_results。
   ```

MCP 固定了工具名称、调用方式和返回结构。Codex 不需要每次拼接脚本路径，也可以根据工具返回的 `success`、`return_code`、`results`、`log` 和 `error` 判断任务状态。

## 三、两种方式的区别

| 项目 | 不使用 MCP | 使用 MCP |
|---|---|---|
| 调用方式 | Codex 执行终端命令 | Codex 调用命名工具 |
| 路径管理 | 每次需要知道脚本路径 | Server 内部统一管理 |
| 参数管理 | 需要修改脚本或拼接命令 | 可设计成工具参数 |
| 返回结果 | 解析终端文本或文件 | 结构化字段返回 |
| 适合场景 | 调试、开发、脚本验证 | 稳定调用、智能体工作流 |

## 四、`AnsysWBU.exe` 错误

Codex 调用 MCP 时出现：

```text
Cached mechanical executable not found
You are about to enter manually the path of the Ansys Mechanical executable
```

这表示 PyMechanical 找不到启动程序，不代表本次求解成功。当前机器实际存在的文件是：

```text
D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe
```

因此 `pymechanical_smoke_test.py` 和 `pymechanical_model_test.py` 已改为显式使用：

```python
MECHANICAL_EXE = Path(
    r"D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe"
)
```

更换电脑或 ANSYS 版本时，需要同步更新这个路径。

## 五、缓存结果说明

如果 MCP 返回 `success: false`，但同时返回了旧的 `results`，这些结果可能是上一次成功求解留下的缓存，不能代表本次调用成功。

当前 `mcp_server.py` 已调整为：只有本次流水线返回码为 `0` 时才返回结果，并增加 `result_is_current` 字段。判断本次是否成功时，优先检查：

```text
success == true
return_code == 0
result_is_current == true
```

## 六、可照抄的完整操作步骤

以下命令均在 PowerShell 中执行。项目使用的 Python 是 `C:\Pyth0n31210\python.exe`；如果 `python` 已指向该环境，也可以将命令中的完整 Python 路径替换为 `python`。

### 6.1 不使用 MCP

#### 方法 A：从终端启动 Codex

1. 打开 PowerShell。
2. 使用 `codex.cmd` 启动 Codex：

   ```powershell
   C:\Users\luo\AppData\Roaming\npm\codex.cmd
   ```

   `codex.cmd` 是 Windows 下 Codex CLI 的启动入口。若 PowerShell 允许执行脚本，也可以使用：

   ```powershell
   codex
   ```

3. 进入项目目录：

   ```text
   D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
   ```

4. 在 Codex 中输入：

   ```text
   请在终端执行 C:\\Pyth0n31210\\python.exe .\\Bending_3D_Beam\\run_pipeline.py，并报告求解状态和关键结果。
   ```

5. Codex 会执行以下实际命令：

   ```powershell
   cd D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
   C:\Pyth0n31210\python.exe .\Bending_3D_Beam\run_pipeline.py
   ```

6. 求解完成后，Codex 应检查：

   ```text
   Bending_3D_Beam\results\latest_results.json
   ```

7. 若只读取并分析最近一次结果，在 Codex 中输入：

   ```text
   请在终端执行 C:\\Pyth0n31210\\python.exe .\\Bending_3D_Beam\\analyze_results.py，并报告最大变形、最大应力和阈值判断。
   ```

#### 方法 B：不启动交互式 Codex

也可以先在 PowerShell 中执行：

```powershell
cd D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation
C:\Users\luo\AppData\Roaming\npm\codex.cmd "请在终端执行 C:\\Pyth0n31210\\python.exe .\\Bending_3D_Beam\\run_pipeline.py，并报告求解状态和关键结果。"
```

### 6.2 使用 MCP

1. 打开 PowerShell。
2. 启动 Codex：

   ```powershell
   C:\Users\luo\AppData\Roaming\npm\codex.cmd
   ```

3. 如果尚未注册 MCP Server，先执行一次：

   ```powershell
   C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp add ansys-mechanical -- "C:\\Pyth0n31210\\python.exe" "D:\\vibe_coding\\Ansys\\Ansys_Mechancal\\mechanical-automation\\mcp_server.py"
   ```

4. 检查注册状态：

   ```powershell
   C:\Users\luo\AppData\Roaming\npm\codex.cmd mcp list
   ```

   必须看到 `ansys-mechanical` 且状态为 `enabled`。

5. 完全退出当前 Codex 会话，再重新启动一次，使 MCP 配置加载。
6. 在新 Codex 会话中输入：

   ```text
   列出所有可用的 MCP 工具。
   ```

7. 确认工具列表中包含：

   ```text
   run_static_analysis
   read_latest_results
   ```

8. 执行完整求解：

   ```text
   调用 run_static_analysis，执行一次弯曲梁静力分析，并报告求解状态、最大总变形和最大等效应力。
   ```

9. 读取已有结果：

   ```text
   调用 read_latest_results，读取最近一次弯曲梁静力分析结果。
   ```

10. 判断 MCP 返回值时检查：

   ```text
   success: true
   return_code: 0
   result_is_current: true
   ```

MCP Server 会自动调用 `Bending_3D_Beam\run_pipeline.py`，不需要用户手动运行 `mcp_server.py`，也不需要手动打开 Workbench 或 Mechanical。

## 七、目录组织

推荐采用“案例文件归案例目录，通用接口留根目录”的结构：

```text
mechanical-automation/
├─ mcp_server.py
├─ pymechanical_smoke_test.py
├─ requirements.txt
├─ Bending_3D_Beam/
│  ├─ beam.wbpj
│  ├─ run_static.py
│  ├─ mesh_solve.py
│  ├─ mesh_solve2.py
│  ├─ pymechanical_model_test.py
│  ├─ run_pipeline.py
│  ├─ analyze_results.py
│  ├─ beam_files/
│  └─ results/
└─ td-007/
```

这样组织的原因是：`Bending_3D_Beam` 内的脚本和结果只属于该案例；根目录的 `mcp_server.py` 是通用入口，未来可以根据案例名称选择不同子目录。当前已将 `pymechanical_model_test.py`、`run_pipeline.py` 和 `analyze_results.py` 移入 `Bending_3D_Beam`，并同步修正了路径引用。
