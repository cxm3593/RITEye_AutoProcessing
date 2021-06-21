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
lower_vg = head_vgroups.get("lower_blinker")
head_vg = head_vgroups.get("head_move")
#upper_vg.add(eyelid_verts, 1.0, 'ADD') 
#upper_vg.remove(eyelid_verts)

### Calculate S
## variables
print("Calculating S...")

B = upper_blinker.tail
print("B_Tail: ",B[0], ",",B[1], ",",B[2])
c = 0.5

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
    S = D #/ (math.pow(abs(Dz), c))
    return S

def addGroupWeight(group, vg, weight):
    for pair in group:
        vg.add([pair[0]], weight, 'ADD') 
        
def findMinMax(list):
    min = list[0]
    max = list[0]
    for v in list:
        if v > max:
            max = v
        if v < min:
            min = v
    return [min, max]

def removeAllweight():
    upper_vg.remove([v.index for v in head.data.vertices]) # to remove everything for debugging
    lower_vg.remove([v.index for v in head.data.vertices])
    head_vg.remove([v.index for v in head.data.vertices])

## helper functions end

## Method 1
#for v_index in eyelid_verts:
#    vertex = getVertexByIndex(v_index, head)
#    S = CalculateS(vertex, B)
#    S_dict[v_index] = S


#sorted_S_dict = sorted(S_dict.items(), key= lambda x: x[1], reverse = True)

## for debug
#for s in sorted_S_dict:
#    print(s[0],": ",s[1])

#group_size = int(len(sorted_S_dict) / 4)
#group1 = sorted_S_dict[:group_size]
#group2 = sorted_S_dict[group_size:int(2*group_size)]
#group3 = sorted_S_dict[int(2*group_size):int(3*group_size)]
#group4 = sorted_S_dict[int(3*group_size):]

#addGroupWeight(group1, upper_vg, 1.0)
#addGroupWeight(group2, upper_vg, 0.85)
#addGroupWeight(group3, upper_vg, 0.78)
#addGroupWeight(group1, upper_vg, 0.6)
## Method 1 Ends

## Method 2
Eyelid_apex_index = 1125 # the index of apex vertex
Eyelid_apex_vertex = getVertexByIndex(Eyelid_apex_index, head)


D_dict = {}


# Calculate distance
for v_index in eyelid_verts:
    vertex = getVertexByIndex(v_index, head)
    Dx = vertex.co[0] - Eyelid_apex_vertex.co[0]
    Dy = vertex.co[1] - Eyelid_apex_vertex.co[1]
    Dz = vertex.co[2] - Eyelid_apex_vertex.co[2]
    D = math.sqrt((Dx*Dx) + (Dy*Dy) + (Dz*Dz))
    print(v_index, ": ",Dx,", ",Dy,", ",Dz)
    D_dict[vertex.index] = D

minmax = findMinMax(list(D_dict.values()))
Min = minmax[0]
Max = minmax[1]
print("Min: ",Min, ", Max: ", Max)
Range = Max - Min

# Calculate z difference
Dz_dict = {}
for v_index in eyelid_verts:
    vertex = getVertexByIndex(v_index, head)
    Dz = vertex.co[1] - Eyelid_apex_vertex.co[1]
    if Dz < 0:
        Dz = 0
    Dz_dict[v_index] = Dz
    
z_minmax = findMinMax(list(Dz_dict.values()))
z_Min = z_minmax[0]
z_Max = z_minmax[1]
z_Range = z_Max - z_Min
#

for p in D_dict.items():
    D_diff = p[1] - Min
    percentage = D_diff / Range
    z_percentage = Dz_dict[p[0]] / z_Range
    weight = 1 - (percentage * 0.6) - (z_percentage * 0.3)
    print("Index: ", p[0], " Position ", p," Percentage: ", percentage, ", weight: ", weight)
    upper_vg.add([p[0]], weight, 'REPLACE')
    
    
#for v_index in eyelid_verts:
#    vertex = getVertexByIndex(v_index, head)
#    for i in vertex.groups:
#        print(v_index, ": ", i.weight)

#removeAllweight()
