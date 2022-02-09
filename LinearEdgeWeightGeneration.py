### LinearEdgeWeightGeneration.py
### Generate vertices weight from edge with a linear approach 
### Author: Chengyi Ma, cxm3593@g.rit.edu

import bpy
import json
import math
import sys

##-##-##-

##-##-##- Variables:
head = bpy.data.objects["head"]
parameters_json = {}
AutoScriptParameterFileName = "AutoScriptParameters.json"
UpperEyelidEdgeVertFile = "eyelidEdge_vertices_upper.txt"
UpperEyelidVertFile = "eyelid_vertices.txt"
LowerEyelidEdgeVertFile = "eyelidEdge_vertices_lower.txt"
LowerEyelidVertFile = "eyelid_vertices_lower.txt"

upper_vg = head.vertex_groups.get("upper_blinker")
lower_vg = head.vertex_groups.get("lower_blinker")



##-##-##- Functions:

def initParameters():
    with open(AutoScriptParameterFileName) as p_json:
        parameters_str = p_json.read()
    parameters_json = json.loads(parameters_str)
    return parameters_json

def readVertexFile(filename: str) -> list:
	"""Read a vertex file and return a list of string for vertices index"""
	vertices_list = []
	with open(filename, "r") as v_file:
		for v in v_file.readlines():
			v_string = v.strip()
			vertices_list.append(int(v_string))
	return vertices_list

def getVertexByIndex(index: int, obj: bpy.types.Object) -> bpy.types.MeshVertex:
	"""Get a MeshVertex Object from Blender Obj by its index"""
	for v in obj.data.vertices:
		if v.index == index:
			return v

def findPosInList(vlist: list, target: int) -> int:
	pos = 0
	for v in vlist:
		if target == v.index:
			return pos
		else:
			pos += 1

def CalculateDistance(v1, v2) -> float:
	Dx = v1.co[0] - v2.co[0]
	Dy = v1.co[1] - v2.co[1]
	Dz = v1.co[2] - v2.co[2]
	D = math.sqrt(Dx*Dx + Dy*Dy + Dz*Dz)
	return D

def GetDeltaX(v1, v2) -> float:
	Dx = v1.co[0] - v2.co[0]
	return Dx

def QuadraticWeight(deltaX, n):
	weight = 1 - (1 / math.pow(n, 2)) * math.pow(deltaX, 2) * 0.3
	return weight


def GenerateEdgeWeight(edge_verts, edge_verts_Xdict, apex_name:str):
	"""
	The method that generates weight for eyelid edge verts
	"""

	for v_str in edge_verts:
		v = getVertexByIndex(v_str, head)
		if(v!=None):
			edge_verts_Xdict[v] = v.co[0] * 10
		else:
			print("Cannot find", v_str)

	edge_verts_dict = dict(sorted(edge_verts_Xdict.items(), key=lambda item: item[1]))
	sorted_index = list(edge_verts_dict.keys())

	first_corner_vert = sorted_index[0]
	last_corner_vert = sorted_index[-1]
	eyelid_apex_index = parameters_json[apex_name]
	eyelid_apex = getVertexByIndex(eyelid_apex_index, head)

	eyelid_apex_ListPos = findPosInList(sorted_index, eyelid_apex_index)

	edge_weight_dict = {}
	left_distance = CalculateDistance(first_corner_vert, eyelid_apex)
	right_distance = CalculateDistance(last_corner_vert, eyelid_apex)

	a = GetDeltaX(sorted_index[0], eyelid_apex)
	b = GetDeltaX(sorted_index[-1], eyelid_apex)
	indexPos = 0

	for v in sorted_index:
		deltaX = GetDeltaX(v, eyelid_apex)
		if indexPos <= eyelid_apex_ListPos:
			edge_weight_dict[v] = QuadraticWeight(deltaX, a)
		else:
			edge_weight_dict[v] = QuadraticWeight(deltaX, b)
		indexPos += 1

	return [edge_weight_dict, sorted_index]

def MatchEyelidVertToEdge(EdgeMatchTable, all_verts_index, sorted_index):
	for v_index in all_verts_index:
		v = getVertexByIndex(v_index, head)
		closest_edge_vert = sorted_index[0]
		closest_edge_value = CalculateDistance(v, closest_edge_vert)
		for edge_vert in sorted_index:
			current_distance = CalculateDistance(v, edge_vert)
			if current_distance < closest_edge_value:
				closest_edge_vert = edge_vert
				closest_edge_value = current_distance
		EdgeMatchTable[closest_edge_vert].append(v)

	return EdgeMatchTable

def GenerateEyelidWeight(EdgeMatchTable, edge_weight_dict):
	eyelid_weight_table = {}

	for current_edge_vert, closest_list in EdgeMatchTable.items():
		temp_distance_table = {}
		Max_distance = CalculateDistance(closest_list[0], current_edge_vert)
		for current_eyelid_vert in closest_list:
			current_distance = CalculateDistance(current_eyelid_vert, current_edge_vert)
			temp_distance_table[current_eyelid_vert] = current_distance
			if current_distance > Max_distance:
				Max_distance = current_distance
		
		for current_vert, current_distance in temp_distance_table.items():
			if Max_distance == 0.0:
				percentage = 0.0
			else:
				percentage = current_distance / Max_distance
			closest_edge_weight = edge_weight_dict[current_edge_vert]
			current_weight = closest_edge_weight * (1 - percentage * 0.3)
			eyelid_weight_table[current_vert] = current_weight

	return eyelid_weight_table

def ApplyWeightsToVerts(eyelid_weight_table, vertex_group):
	for tuple in eyelid_weight_table.items():
		vertex_group.add([tuple[0].index], tuple[1], 'REPLACE')
		

##-##-##- Program Begins Here:
print("Running Linear Edge Weight Script...")

parameters_json = initParameters()
upper_edge_verts = readVertexFile(UpperEyelidEdgeVertFile)
lower_edge_verts = readVertexFile(LowerEyelidEdgeVertFile)

upper_edge_verts_Xdict = {}
lower_edge_verts_Xdict = {}

##-##- First, calculate weight for vertices on the edge
GEW_result_upper = GenerateEdgeWeight(upper_edge_verts, upper_edge_verts_Xdict, apex_name="upper_lid")
upper_edge_weight_dict = GEW_result_upper[0]
sorted_index_upper = GEW_result_upper[1]

GEW_result_lower = GenerateEdgeWeight(lower_edge_verts, lower_edge_verts_Xdict, apex_name="lower_lid")
lower_edge_weight_dict = GEW_result_lower[0]
sorted_index_lower = GEW_result_lower[1]


##-##- Second calculate weight for each vertex based on the distance to the closest vertex.
all_upper_verts_index = readVertexFile(UpperEyelidVertFile)
EdgeMatchTable_upper = {}
##- Initialize Match Table
for v in sorted_index_upper:
	EdgeMatchTable_upper[v] = []

all_lower_verts_index = readVertexFile(LowerEyelidVertFile)
EdgeMatchTable_lower = {}
for v in sorted_index_lower:
	EdgeMatchTable_lower[v] = []

##- Put verts on eyelid to the list which matches the closest edge vert
EdgeMatchTable_upper = MatchEyelidVertToEdge(EdgeMatchTable_upper, all_upper_verts_index, sorted_index_upper)
EdgeMatchTable_lower = MatchEyelidVertToEdge(EdgeMatchTable_lower, all_lower_verts_index, sorted_index_lower)

# For debug
# for tuple in EdgeMatchTable_upper.items():
# 	print(tuple[0].index, ":", [e.index for e in tuple[1]])

for tuple in EdgeMatchTable_lower.items():
	print(tuple[0].index, ":", [e.index for e in tuple[1]])

##- For each closest list, find the max range and ration of distance to the max for each vertex
# upper_eyelid_weight_table = {}
upper_eyelid_weight_table = GenerateEyelidWeight(EdgeMatchTable_upper, upper_edge_weight_dict)
lower_eyelid_weight_table = GenerateEyelidWeight(EdgeMatchTable_lower, lower_edge_weight_dict)



##-##- Apply weights to vertices
ApplyWeightsToVerts(upper_eyelid_weight_table, upper_vg)
ApplyWeightsToVerts(lower_eyelid_weight_table, lower_vg)

##-##-##- Add modifiers
# ShrinkWrap_upper_Eye = head.modifiers.new("ShrinkWrap_upper", 'SHRINKWRAP')
# ShrinkWrap_upper_Eye.wrap_mode = 'OUTSIDE'
# ShrinkWrap_upper_Eye.target = bpy.data.objects["Eye.Wetness"]
# ShrinkWrap_upper_Eye.offset = 0.03
# ShrinkWrap_upper_Eye.vertex_group = "upper_blinker"
# ShrinkWrap_upper_Cornea = head.modifiers.new("ShrinkWrap_upper_Cornea", 'SHRINKWRAP')
# ShrinkWrap_upper_Cornea.wrap_mode = 'OUTSIDE'
# ShrinkWrap_upper_Cornea.target = bpy.data.objects["63"]
# ShrinkWrap_upper_Cornea.offset = 0.03
# ShrinkWrap_upper_Cornea.vertex_group = "upper_blinker"

# ShrinkWrap_lower_Cornea = head.modifiers.new("ShrinkWrap_upper_Cornea", 'SHRINKWRAP')
# ShrinkWrap_lower_Cornea.wrap_mode = 'OUTSIDE'
# ShrinkWrap_lower_Cornea.target = bpy.data.objects["63"]
# ShrinkWrap_lower_Cornea.offset = 0.03
# ShrinkWrap_lower_Cornea.vertex_group = "lower_blinker"

##-##- Fix some bug

##- Set Rotation mode
bpy.data.objects["Armature"].pose.bones["upper_blinker"].rotation_mode = 'XYZ'
bpy.data.objects["Armature"].pose.bones["lower_blinker"].rotation_mode = 'XYZ'

bpy.data.objects["upper"].modifiers["Armature"].object = bpy.data.objects["Armature"]
bpy.data.objects["lower"].modifiers["Armature"].object = bpy.data.objects["Armature"]

##- Scale Fix
#bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
# bpy.ops.transform.resize(value=(10, 10, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.data.objects["Armature"].scale = bpy.data.objects["Armature"].scale * 100
bpy.data.objects["Camera"].scale = bpy.data.objects["Camera"].scale * 100
bpy.data.objects["Empty"].scale = bpy.data.objects["Empty"].scale * 100
bpy.data.objects["Eye.Wetness"].scale = bpy.data.objects["Eye.Wetness"].scale * 100
bpy.data.objects["Sunglasses"].scale = bpy.data.objects["Sunglasses"].scale * 100

##- Set default render machine
bpy.context.scene.render.engine = 'CYCLES'

##- Set Unit fix
bpy.context.scene.unit_settings.scale_length = 0.01
bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'



## for debug
for tuple in upper_eyelid_weight_table.items():
	print(tuple)
	