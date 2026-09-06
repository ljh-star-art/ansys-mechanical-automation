"""Verify Pressure.Magnitude assignment in Mechanical 2024 R2.

Run in Mechanical Automation > Scripting with SYS.mechdb loaded.  The test
writes the existing value (30000 Pa) back to the pressure object, so it does
not intentionally change the model's physical load.
"""

OUTPUT_FILE = (
    "D:/vibe_coding/Ansys/Ansys_Mechancal/mechanical-automation/"
    "Bending_3D_Beam/results/pressure_assignment_test.txt"
)


def write_line(stream, message):
    text = repr(message).replace("\\x00", "<NUL>")
    text = "".join(ch if ord(ch) < 128 else "?" for ch in text)
    stream.write(text + "\n")
    try:
        ExtAPI.Log.WriteMessage(text)
    except Exception:
        pass


with open(OUTPUT_FILE, "w") as stream:
    write_line(stream, "Pressure assignment test started")
    analysis = Model.Analyses[0]
    pressure = None
    for child in analysis.Children:
        try:
            if "Pressure" in str(child.DataModelObjectCategory):
                pressure = child
                break
        except Exception:
            pass

    if pressure is None:
        write_line(stream, "No Pressure object found")
    else:
        write_line(stream, "Before: " + repr(pressure.Magnitude))
        try:
            pressure.Magnitude = Quantity("30000 [Pa]")
            write_line(stream, "Assignment method: pressure.Magnitude = Quantity(...) succeeded")
        except Exception as first_error:
            write_line(stream, "Direct assignment failed: " + repr(first_error))
            try:
                pressure.Magnitude.Output.DiscreteValues = [Quantity("30000 [Pa]")]
                write_line(stream, "Assignment method: Magnitude.Output.DiscreteValues succeeded")
            except Exception as second_error:
                write_line(stream, "DiscreteValues assignment failed: " + repr(second_error))

        try:
            write_line(stream, "After: " + repr(pressure.Magnitude))
        except Exception as error:
            write_line(stream, "Readback failed: " + repr(error))

    write_line(stream, "Pressure assignment test completed")

