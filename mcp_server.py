import json
import subprocess
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer


PROJECT_ROOT = Path(__file__).resolve().parent
CASE_ROOT = PROJECT_ROOT / "Bending_3D_Beam"
PIPELINE_SCRIPT = CASE_ROOT / "run_pipeline.py"
RESULT_FILE = PROJECT_ROOT / "Bending_3D_Beam" / "results" / "latest_results.json"

server = MCPServer(name="ansys-mechanical-automation")


def load_results():
    if not RESULT_FILE.exists():
        raise FileNotFoundError("Result file not found: " + str(RESULT_FILE))
    with RESULT_FILE.open("r", encoding="utf-8") as stream:
        return json.load(stream)


@server.tool()
def run_static_analysis() -> dict:
    """Run the validated PyMechanical static-analysis pipeline."""
    completed = subprocess.run(
        [sys.executable, str(PIPELINE_SCRIPT)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    results = load_results() if completed.returncode == 0 and RESULT_FILE.exists() else {}
    return {
        "success": completed.returncode == 0,
        "return_code": completed.returncode,
        "results": results,
        "result_is_current": completed.returncode == 0,
        "log": completed.stdout[-4000:],
        "error": completed.stderr[-4000:],
    }


@server.tool()
def read_latest_results() -> dict:
    """Read the latest standardized Mechanical result file."""
    return load_results()


if __name__ == "__main__":
    server.run("stdio")
