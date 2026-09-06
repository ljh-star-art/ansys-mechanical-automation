from pathlib import Path
import shutil
import json

from ansys.mechanical.core import launch_mechanical


PROJECT_ROOT = Path(__file__).resolve().parent
MECHANICAL_EXE = Path(r"D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe")
MECHDB = PROJECT_ROOT / "beam_files" / "dp0" / "global" / "MECH" / "SYS.mechdb"
STATIC_SCRIPT = PROJECT_ROOT / "run_static.py"
CONFIG_FILE = PROJECT_ROOT / "case_config.json"
SOURCE_RESULT = PROJECT_ROOT / "beam_files" / "dp0" / "global" / "MECH" / "SYS_Mech_Files" / "latest_results.json"
RESULT_DIR = PROJECT_ROOT / "results"
RESULT_FILE = RESULT_DIR / "latest_results.json"


def main():
    if not MECHDB.exists():
        raise FileNotFoundError("Mechanical database not found: " + str(MECHDB))
    if not STATIC_SCRIPT.exists():
        raise FileNotFoundError("Static script not found: " + str(STATIC_SCRIPT))
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config file not found: " + str(CONFIG_FILE))

    with CONFIG_FILE.open("r", encoding="utf-8") as stream:
        config = json.load(stream)
    element_size_m = float(config["element_size_m"])

    mechanical = launch_mechanical(
        exec_file=str(MECHANICAL_EXE),
        batch=True,
        transport_mode="insecure",
        cleanup_on_exit=True,
    )
    try:
        load_script = (
            "ExtAPI.DataModel.Project.Open(r'"
            + str(MECHDB).replace("\\", "/")
            + "')"
        )
        print("Loading:", MECHDB)
        print(mechanical.run_python_script(load_script))
        mechanical.run_python_script("element_size_m = " + repr(element_size_m))
        print("Running:", STATIC_SCRIPT)
        result = mechanical.run_python_script_from_file(str(STATIC_SCRIPT))
        print(result)
        if not SOURCE_RESULT.exists():
            raise FileNotFoundError("Mechanical result not found: " + str(SOURCE_RESULT))
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_RESULT, RESULT_FILE)
        print("Standard result written to:", RESULT_FILE)
        print("PyMechanical model test completed.")
    finally:
        mechanical.exit()


if __name__ == "__main__":
    main()
