import bpy

head_obj = bpy.data.objects["Head"]

head_vgroups = head_obj.vertex_groups
head_vertices = head_obj.data.vertices

# Experiment Code
print("Debug: Vertex Experiment")

# Print out the vertices's weight and what vertex groups it belongs to
for v in head_vertices:
    if len(v.groups) == 0:
        continue
    else:
        print(v.index, ": ")
        for i in v.groups:
            print(i.group, ": ", i.weight)
        
print("Debug: Vertex group experiment")
for vg in head_vgroups:
    print(vg.index, ": ", vg.name)


