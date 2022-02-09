import bpy

# Store Eyelid vertices
print("Debug: vertex weights\n")

eyelid_upper = "eyelid_vertices.txt"
eyelid_lower = "eyelid_vertices_lower.txt"
eyelid_upper_edge = "eyelidEdge_vertices_upper.txt"
eyelid_lower_edge = "eyelidEdge_vertices_lower.txt"

head_raw = bpy.data.objects["head"]

with open(eyelid_upper, "w") as vertice_file:
    #selected_verts = [v for v in head_raw.data.vertices if v.select]
    selected_verts = []
    for v in head_raw.data.vertices:
        if v.select == True:
            selected_verts.append(v)
    for v in selected_verts:
        vertice_file.write(str(v.index) + "\n")