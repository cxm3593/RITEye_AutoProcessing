import bpy

# Store Eyelid vertices
print("Debug: vertex weights\n")

head_raw = bpy.data.objects["Head"]

with open("eyelid_vertices_lower.txt", "w") as vertice_file:
    #selected_verts = [v for v in head_raw.data.vertices if v.select]
    selected_verts = []
    for v in head_raw.data.vertices:
        if v.select == True:
            selected_verts.append(v)
    for v in selected_verts:
        vertice_file.write(str(v.index) + "\n")