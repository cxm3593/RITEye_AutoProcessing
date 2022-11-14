import bpy

head = bpy.data.objects["head"]

eyelidR_upper = "eyelidR_vertices_upper.txt"
eyelidR_lower = "eyelidR_vertices_lower.txt"
eyelidR_upper_edge = "eyelidEdgeR_vertices_upper.txt"
eyelidR_lower_edge = "eyelidEdgeR_vertices_lower.txt"


vertices_list = []
with open(eyelidR_upper_edge, "r") as vertices_file:
    for v in vertices_file.readlines():
        vertex_str = v.strip()
        if(int(vertex_str) != None):
            vertices_list.append(int(vertex_str))
            
head_vertices = head.data.vertices

for v in head_vertices:
    for sv in vertices_list:
        if v.index == sv:
            v.select = True
            
