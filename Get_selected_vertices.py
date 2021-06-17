# Store Eyelid vertices
print("Debug: vertex weights\n")

head_raw = bpy.data.objects["Head.003"]

with open("eyelid_vetices.txt", "w") as vertice_file:
    selected_verts = [v for v in head_raw.data.vertices if v.select]
    for v in selected_verts:
        vertice_file.write(str(v.index) + "\n")