import json
import re
from pathlib import Path


RESULT_FILE = (
    Path(__file__).resolve().parent / "results" / "latest_results.json"
)
CONFIG_FILE = Path(__file__).resolve().parent / "case_config.json"


def quantity_value(value):
    match = re.match(r"\s*([-+0-9.eE]+)", str(value))
    if not match:
        raise ValueError("Unable to parse quantity: " + str(value))
    return float(match.group(1))


def main():
    if not RESULT_FILE.exists():
        raise FileNotFoundError("Result file not found: " + str(RESULT_FILE))
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config file not found: " + str(CONFIG_FILE))

    with RESULT_FILE.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    with CONFIG_FILE.open("r", encoding="utf-8") as stream:
        config = json.load(stream)

    if data.get("status") != "success":
        raise RuntimeError("Mechanical solve did not report success")

    deformation = quantity_value(data["max_total_deformation"])
    stress = quantity_value(data["max_equivalent_stress"])

    print("Result file:", RESULT_FILE)
    print("Maximum deformation (m):", deformation)
    print("Maximum equivalent stress (Pa):", stress)

    stress_limit = float(config["stress_limit_pa"])
    print("Stress limit (Pa):", stress_limit)
    if stress > stress_limit:
        print("Decision: stress limit exceeded")
        raise SystemExit(2)

    print("Decision: result is within the configured stress limit")


if __name__ == "__main__":
    main()
