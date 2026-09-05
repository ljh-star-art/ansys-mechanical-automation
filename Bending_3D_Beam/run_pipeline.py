import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SOLVE_SCRIPT = PROJECT_ROOT / "pymechanical_model_test.py"
ANALYZE_SCRIPT = PROJECT_ROOT / "analyze_results.py"


def run_step(label, script):
    print("\n=== " + label + " ===")
    completed = subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main():
    run_step("PyMechanical solve", SOLVE_SCRIPT)
    run_step("Result analysis", ANALYZE_SCRIPT)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
