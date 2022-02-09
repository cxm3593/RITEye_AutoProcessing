import bpy

head = bpy.data.objects["head"]

eyelid_upper = "eyelid_vertices.txt"
eyelid_lower = "eyelid_vertices_lower.txt"
eyelid_upper_edge = "eyelidEdge_vertices_upper.txt"
eyelid_lower_edge = "eyelidEdge_vertices_lower.txt"


vertices_list = []
with open(eyelid_lower, "r") as vertices_file:
    for v in vertices_file.readlines():
        vertex_str = v.strip()
        if(int(vertex_str) != None):
            vertices_list.append(int(vertex_str))
            
head_vertices = head.data.vertices

for v in head_vertices:
    for sv in vertices_list:
        if v.index == sv:
            v.select = True
            
