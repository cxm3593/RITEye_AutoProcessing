# Apply weight to eyelid automatically by script

import bpy
import math

print("####Running Eyelid_AutoWeight.py...")
## Initialize some variables
head = bpy.data.objects["Head"]
head_vgroups = head.vertex_groups

upper_eyelash = bpy.data.objects["upper"]
lower_eyelash = bpy.data.objects["lower"]

## Create Armature and set up bones
new_armature = bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
Armature_obj = bpy.data.objects["Armature"]
Armature_obj.show_in_front = True
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
edit_bones = Armature_obj.data.edit_bones
edit_bones.remove(edit_bones["Bone"]) # delete the default one


head_move = edit_bones.new('head_move')
head_move.head = (0.0, 1.0, 0.0)
head_move.tail = (0.0, 0.0, 0.0)

upper_blinker = edit_bones.new('upper_blinker')
upper_blinker.head = (0.0, 0.0, 0.0)
upper_blinker.tail = (0.0, -1.33367, 0.45673)
upper_blinker.parent = head_move
lower_blinker = edit_bones.new('lower_blinker')
lower_blinker.head = (0.0, 0.0, 0.0)
lower_blinker.tail = (0.0, -1.21273, -0.68972)
lower_blinker.parent = head_move

## Parenting Objects to Armature
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.ops.object.select_all(action='DESELECT') #deselect all objects
head.select = True
upper_eyelash.select = True
lower_eyelash.select = True
Armature_obj.select = True
bpy.context.view_layer.objects.active = Armature_obj
bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)


## Calculate vertex weight
eyelid_upper_verts = []
eyelid_lower_verts = []


# read upper_eyelid vertices
print("Reading Vertices...")
with open("eyelid_vertices.txt", "r") as vertices_file:
    for v in vertices_file.readlines():
        vertex_str = v.strip()
        eyelid_upper_verts.append(int(vertex_str))

with open("eyelid_vertices_lower.txt", "r") as lower_vertices_file:
	for v in lower_vertices_file.readlines():
		vertex_str = v.strip()
		eyelid_lower_verts.append(int(vertex_str))
        
# apply weight to vertices
upper_vg = head_vgroups.get("upper_blinker")
lower_vg = head_vgroups.get("lower_blinker")
head_vg = head_vgroups.get("head_move")


### Calculate S
## variables
print("Calculating S...")

BU = upper_blinker.tail
#print("B_Tail: ",BU[0], ",",BU[1], ",",BU[2])
BL = lower_blinker.tail
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

def generateVertexWeight(eyelid_verts, eyelid_apex, vertex_group, head, isUpper):

	D_dict = {}
	for v_index in eyelid_verts:
		vertex = getVertexByIndex(v_index, head)
		Dx = vertex.co[0] - eyelid_apex.co[0]
		Dy = vertex.co[1] - eyelid_apex.co[1]
		Dz = vertex.co[2] - eyelid_apex.co[2]
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
		Dz = vertex.co[1] - eyelid_apex.co[1]
		if isUpper == True:
			if Dz < 0:
				Dz = 0
		else:
			if Dz >0:
				Dz = 0
		Dz_dict[v_index] = Dz

	z_minmax = findMinMax(list(Dz_dict.values()))
	z_Min = z_minmax[0]
	z_Max = z_minmax[1]
	z_Range = z_Max - z_Min

	for p in D_dict.items():
		D_diff = p[1] - Min
		percentage = D_diff / Range
		z_percentage = Dz_dict[p[0]] / z_Range
		weight = 1 - (percentage * 0.6) - (z_percentage * 0.3)
		#print("Index: ", p[0], " Position ", p," Percentage: ", percentage, ", weight: ", weight)
		vertex_group.add([p[0]], weight, 'REPLACE')

	return True

## helper functions end


### Auto weight Method 2
Eyelid_upper_apex_index = 1125 # the index of apex vertex
Eyelid_upper_apex_vertex = getVertexByIndex(Eyelid_upper_apex_index, head)
Eyelid_lower_apex_index = 1160
Eyelid_lower_apex_vertex = getVertexByIndex(Eyelid_lower_apex_index, head)

D_dict = {}

## Generating for upper eyelid
generateVertexWeight(eyelid_upper_verts, Eyelid_upper_apex_vertex, upper_vg, head, True)


## Code block, works fine but not reusable
# for v_index in eyelid_upper_verts:
#     vertex = getVertexByIndex(v_index, head)
#     Dx = vertex.co[0] - Eyelid_upper_apex_vertex.co[0]
#     Dy = vertex.co[1] - Eyelid_upper_apex_vertex.co[1]
#     Dz = vertex.co[2] - Eyelid_upper_apex_vertex.co[2]
#     D = math.sqrt((Dx*Dx) + (Dy*Dy) + (Dz*Dz))
#     print(v_index, ": ",Dx,", ",Dy,", ",Dz)
#     D_dict[vertex.index] = D

# minmax = findMinMax(list(D_dict.values()))
# Min = minmax[0]
# Max = minmax[1]
# print("Min: ",Min, ", Max: ", Max)
# Range = Max - Min

# # Calculate z difference
# Dz_dict = {}
# for v_index in eyelid_upper_verts:
#     vertex = getVertexByIndex(v_index, head)
#     Dz = vertex.co[1] - Eyelid_upper_apex_vertex.co[1]
#     if Dz < 0:
#         Dz = 0
#     Dz_dict[v_index] = Dz
    
# z_minmax = findMinMax(list(Dz_dict.values()))
# z_Min = z_minmax[0]
# z_Max = z_minmax[1]
# z_Range = z_Max - z_Min

# for p in D_dict.items():
#     D_diff = p[1] - Min
#     percentage = D_diff / Range
#     z_percentage = Dz_dict[p[0]] / z_Range
#     weight = 1 - (percentage * 0.6) - (z_percentage * 0.3)
#     #print("Index: ", p[0], " Position ", p," Percentage: ", percentage, ", weight: ", weight)
#     upper_vg.add([p[0]], weight, 'REPLACE')

## Generating for lower eyelid
generateVertexWeight(eyelid_lower_verts, Eyelid_lower_apex_vertex, lower_vg, head, False)


### Add modifiers
## Adding armature for upper eyelid
bpy.context.view_layer.objects.active = head
mod_to_remove = head.modifiers["Armature"]
head.modifiers.remove(mod_to_remove)
Armature_mod_upper = head.modifiers.new("Armature_upper", 'ARMATURE')
Armature_mod_upper.object = Armature_obj
Armature_mod_upper.vertex_group = "upper_blinker"

Armature_mod_lower = head.modifiers.new("Armature_lower", 'ARMATURE')
Armature_mod_lower.object = Armature_obj
Armature_mod_lower.vertex_group = "lower_blinker"

## modifier adjustment for eyelash
bpy.context.view_layer.objects.active = upper_eyelash
bpy.ops.object.modifier_move_to_index(modifier="Armature", index=2)



## For Optional Debug Purpose
#removeAllweight()
