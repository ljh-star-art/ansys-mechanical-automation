import os

try:
    pressure_value_pa
except NameError:
    pressure_value_pa = 30000.0
try:
    load_direction
except NameError:
    load_direction = "negative_y"
try:
    constraint_name
except NameError:
    constraint_name = "fixed_left_end"

mesh = Model.Mesh
try:
    element_size_m
except NameError:
    element_size_m = 0.01
element_size = Quantity(element_size_m, "m")
mesh.ElementSize = element_size
mesh.GenerateMesh()

analysis = Model.Analyses[0]

# Reuse the pressure object and its existing geometry selection.  This changes
# only the magnitude; it does not guess or replace the loaded face.
pressure = None
for child in analysis.Children:
    try:
        if "Pressure" in str(child.DataModelObjectCategory):
            pressure = child
            break
    except Exception:
        pass
if pressure is None:
    raise RuntimeError("No Pressure object found in the analysis tree")
pressure.Magnitude = Quantity(str(pressure_value_pa) + " [Pa]")
print("Pressure applied (Pa):", pressure_value_pa)

solution = analysis.Solution

total_deformation = solution.AddTotalDeformation()
equivalent_stress = solution.AddEquivalentStress()

analysis.Solution.Solve(True)
solution.EvaluateAllResults()

print("Total Deformation:", total_deformation.Maximum)
print("Equivalent Stress:", equivalent_stress.Maximum)
print("Requested pressure (Pa):", pressure_value_pa)
print("Requested load direction:", load_direction)
print("Requested constraint:", constraint_name)

project_dir = ExtAPI.DataModel.Project.ProjectDirectory
result_dir = project_dir
print("Project directory:", project_dir)

result_file = os.path.join(result_dir, "latest_results.json")
with open(result_file, "w") as f:
    f.write("{\n")
    f.write('  "status": "success",\n')
    f.write('  "element_size": "' + str(element_size) + '",\n')
    f.write('  "pressure_value_pa": "' + str(pressure_value_pa) + '",\n')
    f.write('  "load_direction": "' + str(load_direction) + '",\n')
    f.write('  "constraint": "' + str(constraint_name) + '",\n')
    f.write('  "max_total_deformation": "' + str(total_deformation.Maximum) + '",\n')
    f.write('  "max_equivalent_stress": "' + str(equivalent_stress.Maximum) + '"\n')
    f.write("}\n")

print("Results written to:", result_file)
