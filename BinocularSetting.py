'''
Get head model ready for Binocular rendering system

author: Chengyi Ma
'''

import bpy
import json
import math
import sys
import os

### Global Variables ###
MODEL_INDEX = 1


upper_l = bpy.data.objects["upper_L"]
lower_l = bpy.data.objects["lower_L"]
upper_r = None
lower_r = None

RITEyes_path = "E:/RITEyes/RITeyes_pipeline"
HeadInfoJsonPath = os.path.join(RITEyes_path, "static_model", "HeadModelInfo.json")

HeadInfo = None
pupillary_distance = None

### Functions ###
def ReadHeadModelInfoJson():
	global HeadInfo
	with open(HeadInfoJsonPath) as head_info_file:
		json_str = head_info_file.read()
		HeadInfo = json.loads(json_str)


def RightEyelashCreation():
	'''
	Copy left eyelash to the right side of the head model
	'''
	global upper_l, lower_l, upper_r, lower_r, pupillary_distance
	
	# first copy left_upper and left_lower eyelashes
	upper_r = upper_l.copy()
	bpy.context.collection.objects.link(upper_r)
	lower_r = lower_l.copy()
	bpy.context.collection.objects.link(lower_r)

	upper_l.name = 'upper_L'
	lower_l.name = 'lower_L'

	upper_r.name = 'upper_R'
	lower_r.name = 'lower_R'

	pupillary_distance = HeadInfo[str(MODEL_INDEX)]["pupillary distance"]
	upper_r.location[0] = -pupillary_distance * 0.01
	upper_r.scale[0] = upper_r.scale[0] * -1
	lower_r.location[0] = -pupillary_distance * 0.01
	lower_r.scale[0] = lower_r.scale[0] * -1



### Main ###
ReadHeadModelInfoJson()
# RightEyelashCreation()