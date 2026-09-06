output_file = r"D:\vibe_coding\Ansys\Ansys_Mechancal\mechanical-automation\Bending_3D_Beam\results\mechanical_object_dump.txt"


def write_line(stream, message):
    safe_message = repr(message).replace("\\x00", "<NUL>")
    safe_message = "".join(character if ord(character) < 128 else "?" for character in safe_message)
    stream.write(safe_message + "\n")
    try:
        ExtAPI.Log.WriteMessage(safe_message)
    except:
        pass


try:
    with open(output_file, "w") as stream:
        write_line(stream, "Scripting diagnostic started")
        analysis = Model.Analyses[0]
        write_line(stream, "Analysis name: " + repr(analysis.Name))

        for child in analysis.Children:
            write_line(stream, "Object name: " + repr(child.Name))
            try:
                write_line(stream, "Object type: " + repr(child.GetType().FullName))
            except:
                write_line(stream, "Object type: unavailable")

            try:
                write_line(stream, "Object category: " + repr(child.DataModelObjectCategory))
            except:
                write_line(stream, "Object category: unavailable")

        write_line(stream, "Scripting diagnostic completed")
except Exception as error:
    with open(output_file, "a") as stream:
        write_line(stream, "Diagnostic error: " + repr(error))

try:
    ExtAPI.Log.WriteMessage("Diagnostic file: " + output_file)
except:
    pass
