import json
import re
from pathlib import Path
from case_spec import CaseSpec


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
    case_spec = CaseSpec.from_file(CONFIG_FILE)

    if data.get("status") != "success":
        raise RuntimeError("Mechanical solve did not report success")

    deformation = quantity_value(data["max_total_deformation"])
    stress = quantity_value(data["max_equivalent_stress"])

    print("Result file:", RESULT_FILE)
    print("Maximum deformation (m):", deformation)
    print("Maximum equivalent stress (Pa):", stress)
    print("Pressure (Pa):", case_spec.pressure_value_pa)
    print("Load direction:", case_spec.load_direction)
    print("Constraint:", case_spec.constraint)

    stress_limit = case_spec.stress_limit_pa
    print("Stress limit (Pa):", stress_limit)
    if stress > stress_limit:
        print("Decision: stress limit exceeded")
        raise SystemExit(2)

    print("Decision: result is within the configured stress limit")


if __name__ == "__main__":
    main()
