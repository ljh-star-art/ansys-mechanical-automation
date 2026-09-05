mesh = Model.Mesh
mesh.ElementSize = Quantity(0.01, "m")

mesh.GenerateMesh()

analysis = Model.Analyses[0]
analysis.Solution.Solve(True)
