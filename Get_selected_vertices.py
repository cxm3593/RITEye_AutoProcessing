import bpy

# Store Eyelid vertices
print("Debug: vertex weights\n")

eyelidR_upper = "eyelidR_vertices_upper.txt"
eyelidR_lower = "eyelidR_vertices_lower.txt"
eyelidR_upper_edge = "eyelidEdgeR_vertices_upper.txt"
eyelidR_lower_edge = "eyelidEdgeR_vertices_lower.txt"

head_raw = bpy.data.objects["head"]

with open(eyelidR_upper_edge, "w") as vertice_file:
    #selected_verts = [v for v in head_raw.data.vertices if v.select]
    selected_verts = []
    for v in head_raw.data.vertices:
        if v.select == True:
            selected_verts.append(v)
    for v in selected_verts:
        vertice_file.write(str(v.index) + "\n")