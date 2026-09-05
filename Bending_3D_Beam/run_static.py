import os

mesh = Model.Mesh
element_size = Quantity(0.01, "m")
mesh.ElementSize = element_size
mesh.GenerateMesh()

analysis = Model.Analyses[0]
solution = analysis.Solution

total_deformation = solution.AddTotalDeformation()
equivalent_stress = solution.AddEquivalentStress()

analysis.Solution.Solve(True)
solution.EvaluateAllResults()

print("Total Deformation:", total_deformation.Maximum)
print("Equivalent Stress:", equivalent_stress.Maximum)

project_dir = ExtAPI.DataModel.Project.ProjectDirectory
result_dir = project_dir
print("Project directory:", project_dir)

result_file = os.path.join(result_dir, "latest_results.json")
with open(result_file, "w") as f:
    f.write("{\n")
    f.write('  "status": "success",\n')
    f.write('  "element_size": "' + str(element_size) + '",\n')
    f.write('  "max_total_deformation": "' + str(total_deformation.Maximum) + '",\n')
    f.write('  "max_equivalent_stress": "' + str(equivalent_stress.Maximum) + '"\n')
    f.write("}\n")

print("Results written to:", result_file)
