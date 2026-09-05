"""Minimal PyMechanical connectivity test for ANSYS Mechanical 2024 R2."""

from pathlib import Path

from ansys.mechanical.core import launch_mechanical


MECHANICAL_EXE = Path(r"D:\Program Files\ANSYS Inc\v242\aisol\bin\winx64\AnsysWBU.exe")


def main():
    mechanical = launch_mechanical(
        exec_file=str(MECHANICAL_EXE),
        batch=True,
        cleanup_on_exit=True,
        transport_mode="insecure",
    )
    try:
        result = mechanical.run_python_script("1 + 1")
        print("PyMechanical connection succeeded.")
        print("Mechanical evaluated 1 + 1 as:", result)
    finally:
        mechanical.exit()


if __name__ == "__main__":
    main()
