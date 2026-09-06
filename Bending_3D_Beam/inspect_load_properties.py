"""Inspect the existing pressure object in Mechanical.

Run this script in Mechanical's Automation > Scripting window.  It deliberately
writes ASCII text because some Mechanical/IronPython consoles fail when they
receive Unicode object names.
"""

# Use forward slashes here.  A raw Python string cannot end with a single
# backslash, which would cause Mechanical's IronPython parser to report
# ``EOL while scanning single-quoted string``.
OUTPUT_FILE = (
    "D:/vibe_coding/Ansys/Ansys_Mechancal/mechanical-automation/"
    "Bending_3D_Beam/results/pressure_properties.txt"
)


def safe_text(value):
    try:
        text = repr(value)
    except Exception as error:
        text = "<repr failed: %s>" % (error,)
    text = text.replace("\\x00", "<NUL>")
    return "".join(ch if ord(ch) < 128 else "?" for ch in text)


def write_line(stream, message):
    line = safe_text(message)
    stream.write(line + "\n")
    try:
        ExtAPI.Log.WriteMessage(line)
    except Exception:
        pass


with open(OUTPUT_FILE, "w") as stream:
    write_line(stream, "Pressure property inspection started")
    analysis = Model.Analyses[0]
    pressure = None
    for child in analysis.Children:
        try:
            category = str(child.DataModelObjectCategory)
        except Exception:
            category = ""
        if "Pressure" in category:
            pressure = child
            break

    if pressure is None:
        write_line(stream, "No Pressure object found")
    else:
        write_line(stream, "Pressure object name: " + safe_text(pressure.Name))
        write_line(stream, "Pressure object type: " + safe_text(pressure.GetType().FullName))

        # These are the properties most commonly used to change a pressure
        # through the Mechanical ACT API.  Reading them is safe and tells us
        # which form this particular model exposes in 2024 R2.
        # These properties are known to exist for the object found in this
        # model.  Do not access GeometryLocation/CoordinateSystem here: they
        # are not members of the 2024 R2 Pressure object and some Mechanical
        # scripting hosts propagate that AttributeError out of the loop.
        candidates = [
            "Magnitude",
            "Location",
            "LoadedArea",
            "DefineBy",
            "Direction",
            "Suppressed",
            "DataModelObjectCategory",
        ]
        for property_name in candidates:
            try:
                value = getattr(pressure, property_name)
                write_line(stream, property_name + " = " + safe_text(value))
            except Exception as error:
                write_line(
                    stream,
                    property_name + " = <unavailable: " + safe_text(error) + ">",
                )

        # Magnitude is a Field.  Listing its public members helps identify the
        # exact 2024 R2 assignment API without changing the model.
        try:
            magnitude = pressure.Magnitude
            write_line(stream, "Magnitude public attributes:")
            for name in sorted(name for name in dir(magnitude) if not name.startswith("_")):
                write_line(stream, "  " + name)
            try:
                inputs = magnitude.Inputs
                write_line(stream, "Magnitude.Inputs count: " + str(len(inputs)))
                for index in range(len(inputs)):
                    write_line(stream, "Magnitude.Inputs[%d]: %s" % (index, safe_text(inputs[index])))
            except Exception as error:
                write_line(stream, "Magnitude.Inputs unavailable: " + safe_text(error))

            # Do not enumerate or read arbitrary members of Output here.  In
            # Mechanical 2024 R2, Output is a Variable and some apparently
            # harmless members (for example Values) raise from inside the
            # .NET wrapper.  The repr of Magnitude above already reports the
            # current value without touching those members.
            try:
                output = magnitude.Output
                write_line(stream, "Magnitude.Output type: " + safe_text(output.GetType().FullName))
            except Exception as error:
                write_line(stream, "Magnitude.Output type unavailable: " + safe_text(error))
        except Exception as error:
            write_line(stream, "Magnitude inspection failed: " + safe_text(error))

        write_line(stream, "Public attributes:")
        try:
            names = sorted(name for name in dir(pressure) if not name.startswith("_"))
            for name in names:
                write_line(stream, "  " + name)
        except Exception as error:
            write_line(stream, "dir() failed: " + safe_text(error))

    write_line(stream, "Pressure property inspection completed")

try:
    ExtAPI.Log.WriteMessage("Pressure diagnostic file: " + OUTPUT_FILE)
except Exception:
    pass

