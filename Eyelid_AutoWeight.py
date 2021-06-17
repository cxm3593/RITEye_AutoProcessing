# Apply weight to eyelid automatically by script

import bpy
import math


eyelid_verts = []

head = bpy.data.objects["Head"]
head_vgroups = head.vertex_groups

Armature_obj = bpy.data.objects["Armature"]
upper_blinker = Armature_obj.data.bones["upper_blinker"]
lower_blinker = Armature_obj.data.bones["lower_blinker"]

print("####Running Eyelid_AutoWeight.py...")

# read eyelid vertices
print("Reading Vertices...")
with open("eyelid_vertices.txt", "r") as vertices_file:
    for v in vertices_file.readlines():
        vertex_str = v.strip()
        eyelid_verts.append(int(vertex_str))
        
# apply weight to vertices
upper_vg = head_vgroups.get("upper_blinker")
#upper_vg.add(eyelid_verts, 1.0, 'ADD') 
#upper_vg.remove(eyelid_verts)

### Calculate S
## variables
print("Calculating S...")

B = upper_blinker.tail
Bz = upper_blinker.tail[2]
c = 3

S_dict = {}

## helper functions:

def getVertexByIndex(index, obj):
    for v in obj.data.vertices:
        if v.index == index:
            return v
        
def CalculateS(vertex, B):
    Dx = vertex.co[0] - B[0]
    Dy = vertex.co[1] - B[1]
    Dz = vertex.co[2] - B[2]
    D = math.sqrt(Dx*Dx + Dy*Dy + Dz*Dz)
    S = D * (math.pow(abs(Dz), c))
    return S

def addGroupWeight(group, vg, weight):
    for pair in group:
        vg.add([pair[0]], weight, 'ADD') 

## helper functions end


for v_index in eyelid_verts:
    vertex = getVertexByIndex(v_index, head)
    S = CalculateS(vertex, B)
    S_dict[v_index] = S


sorted_S_dict = sorted(S_dict.items(), key= lambda x: x[1], reverse = False)

group_size = int(len(sorted_S_dict) / 4)
group1 = sorted_S_dict[:group_size]
group2 = sorted_S_dict[group_size:int(2*group_size)]
group3 = sorted_S_dict[int(2*group_size):int(3*group_size)]
group4 = sorted_S_dict[int(3*group_size):]

addGroupWeight(group1, upper_vg, 1.0)
addGroupWeight(group2, upper_vg, 0.85)
addGroupWeight(group3, upper_vg, 0.78)
addGroupWeight(group1, upper_vg, 0.6)

#upper_vg.remove(eyelid_verts) # to remove everything for debugging
