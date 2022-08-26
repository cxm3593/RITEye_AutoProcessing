import bpy
import json
import math
import sys
import time

##-##-##- Argument
#model_name = str(sys.argv[1])

##-##-##- Init

eye_filepath = "//Eye.blend"
lashLib_path = "//Eyelash_Lib.blend"
parameters_json = {}

head_filename = model_name # will be passed in as global variable from AutoScript_ExternalLink.py

def initParameters():
    with open("AutoScriptParameters.json") as p_json:
        parameters_str = p_json.read()
    parameters_json = json.loads(parameters_str)
    return parameters_json

def vector_subtract(a,b):
    c = [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
    return c

def vector_scale(a,s):
    c = [a[0]*s, a[1]*s, a[2]*s]
    return c

def ImportHeadModel():
    # file paths
    M12_filePath= "//Head Models\\"+head_filename+"\OBJ\Sub Division\Head.OBJ" # this does not
    M12_filePath_abs = bpy.path.abspath(M12_filePath) # this works

    # Import
    bpy.ops.import_scene.obj(filepath=M12_filePath_abs)
    head = bpy.context.selected_objects[0]
    head.name = "head"

    # shade smooth
    bpy.ops.object.shade_smooth()
    
def moveHead():
    # select the head model
    head=bpy.data.objects["head"]
    
    # model data
    verts = head.data.vertices
    head_shift = [0,0,0]
    
    upper_lid = verts[parameters_json["upper_lid"]].co
    lower_lid = verts[parameters_json["lower_lid"]].co
    inner_corner = verts[parameters_json["inner_corner"]].co
    outer_corner = verts[parameters_json["outer_corner"]].co
    
    delta_lid = vector_subtract(upper_lid, lower_lid)
    delta_corner = vector_subtract(outer_corner, inner_corner)
    
    print(delta_lid)
    print(delta_corner)

    head_shift[0] = inner_corner[0]+delta_corner[0]/2
    # y is up in these vetrex positions
    head_shift[2] = lower_lid[1]+delta_lid[1]/2 
    head_shift[1] = lower_lid[2]-math.sqrt(.012**2-(delta_lid[1]/2)**2)

    head.location[0] = head_shift[0]*-1
    head.location[1] = head_shift[1]
    head.location[2] = head_shift[2]*-1

    # appliest the transform 
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
def cleanEye():
    # 1 cm hole for the skull's orbit
    eyeball_radius = 0.01

    head=bpy.data.objects["head"]
    bpy.context.view_layer.objects.active = head

    # deselects the verticies of the head
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # selects the verticies near the origin (eyeball center)
    mesh = head.data
    for v in mesh.vertices:
        distanceSquared = v.co[0]**2 + v.co[1]**2 + v.co[2]**2
        
        if distanceSquared < eyeball_radius**2:
            v.select = True
        
    # Deletes the selected vertices 
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
def fixSkin():
    # gets the head
    head=bpy.data.objects["head"]

    # applies the skin material
    skin = bpy.data.materials["skin"]
    head.active_material = skin

    # gets the image nodes
    c1_node = skin.node_tree.nodes.get('c1')    # color map 1 
    c2_node = skin.node_tree.nodes.get('c2')    # color map 2 
    s1_node = skin.node_tree.nodes.get('s1')    # specularity map
    n_node = skin.node_tree.nodes.get('n')      # normal map

    # gets the images from the jpg folder
    jpg_path = "//Head Models\\" + head_filename + "\Textures\JPG\\"
    jpg_path = bpy.path.abspath(jpg_path)

    # colors
    color_path = jpg_path + "Colour_8k.jpg"
    color = bpy.data.images.load(filepath=color_path)

    # specularity
    spec_path = jpg_path + "Spec.jpg"
    spec = bpy.data.images.load(filepath=spec_path)

    # normals
    norm_path = jpg_path + "Normal.jpg"
    norm = bpy.data.images.load(filepath=norm_path)

    # assigns the images to the proper nodes
    c1_node.image = color
    c2_node.image = color
    s1_node.image = spec
    n_node.image = norm
    
    
def ImportBlenderFile(filepath, objNames=None):

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to): # link=False : not to modify the original model
        data_to.objects = data_from.objects
        data_to.materials = data_from.materials

    for obj in data_to.objects:
        if objNames!=None:
            if obj.name not in objNames:
                continue
            else:
                print("Obj import found: ", objNames)
        if obj is not None or bpy.types.BlendDataWorkSpaces:
          bpy.context.collection.objects.link(obj)
        
        #rename 
        if obj.name == "EyeWet.002":
            continue
        name_array = obj.name.split('.')
        newname = name_array[0]
        if newname == "Eye":                # hack fix
            newname = "Eye.Wetness"
        obj.name = newname
        if objNames != None:
            if obj.name[1] == 'L':
                obj.name = 'lower'
                if obj.name == "lower.001": # strange, have to add it or it will be named to lower.001
                    obj.name = "lower"
                print("Lower lash named: ", obj.name)
            if obj.name[1] == 'U':
                obj.name = "upper"
                #print("upper exist: ", (bpy.data.objects["upper"] == None) )
                if obj.name == "upper.001":
                    obj.name = "upper"
                print("Upper lash named: ", obj.name)
    
          
def Importeye():
    ImportBlenderFile(eye_filepath)
          
def parent():
    # gets the objects
    head = bpy.data.objects["head"]
    lower = bpy.data.objects["lower"]
    upper = bpy.data.objects["upper"]
    plica = bpy.data.objects["Eye_Plica"]

    # sets the parent to head
    #lower.parent = head
    #upper.parent = head
    plica.parent = head
          
def lashesAndPlica():
    # gets the images from the jpg folder
    blender_path = "//head_components.blend"
    blender_path = bpy.path.abspath(blender_path)
    ImportBlenderFile(blender_path)
    parent()

def ImportLashes():
    uppername = "1" + 'U'
    lowername = "1" + 'L'

    print("Importing eyelashfile: ", [uppername])
    ImportBlenderFile(lashLib_path, objNames = [uppername, lowername])

    
def placeLashes():
    # gets the lashes
    head = bpy.data.objects["head"]
    upper = bpy.data.objects["upper"]
    lower = bpy.data.objects["lower"]
    
    # appliest the transform 
    upper.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    lower.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # wraps the lashes around the model
    upperEdges_lash = parameters_json["upperEdges_lash"]
    lowerEdges_lash = parameters_json["lowerEdges_lash"]
    upperLidVerts_lash = parameters_json["upperLidVerts_lash"]
    lowerLidVerts_lash = parameters_json["lowerLidVerts_lash"]
    
    # warps the lashes geometry 
    placeLash(lower, head, lowerLidVerts_lash, lowerEdges_lash)
    placeLash(upper, head, upperLidVerts_lash, upperEdges_lash)
    
def placeLash(lash, head, lidVerts, edges):
    # positions the lower lash
    bpy.context.view_layer.objects.active = lash
    for i in range(len(edges)):
        # deselects the other egdes
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
    
        vert = head.data.vertices[lidVerts[i]].co
        edge = lash.data.edges[edges[i]]
        edge.select = True
        
        # gets the edges's vertices
        edgeP1 = lash.data.vertices[edge.vertices[0]]
        edgeP2 = lash.data.vertices[edge.vertices[1]]
        
        midpoint = [ 
            (edgeP1.co[0] + edgeP2.co[0]) / 2, 
            (edgeP1.co[1] + edgeP2.co[1]) / 2, 
            (edgeP1.co[2] + edgeP2.co[2]) / 2
        ]
        
        # moves edge to the point
        delta = vector_subtract(vert,midpoint)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.translate(value=(delta[0], delta[1], delta[2]), orient_type='GLOBAL')
        bpy.ops.object.mode_set(mode='OBJECT')

def SetLashes():
    lash_parameters_dict = parameters_json["eyelash_parameters"]
    model_lash_dict = lash_parameters_dict[head_filename]

    thickness = model_lash_dict["thickness"]
    amount = model_lash_dict["amount"]
    clump = model_lash_dict["clump"]
    clump_shape = model_lash_dict["clump_shape"]
    length = model_lash_dict["length"]

    lower = bpy.data.objects["lower"]
    upper = bpy.data.objects["upper"]
    upper_settings = upper.particle_systems["new_lashes"].settings
    lower_settings = lower.particle_systems["new_lashes"].settings

    # settings
    # setting amount
    upper_settings.rendered_child_count = amount[0]
    lower_settings.rendered_child_count = amount[1]
    upper_settings.child_nbr = amount[0]
    lower_settings.child_nbr = amount[1]
    # setting thickness
    upper_settings.root_radius = thickness[0]
    lower_settings.root_radius = thickness[1]
    # setting clump
    upper_settings.clump_factor = clump[0]
    lower_settings.clump_factor = clump[1]
    upper_settings.clump_shape = clump_shape
    lower_settings.clump_shape = clump_shape
    # setting length
    upper_settings.child_length = length[0]
    lower_settings.child_length = length[1]
    # setting random
    upper.particle_systems["new_lashes"].child_seed = int(head_filename)
    lower.particle_systems["new_lashes"].child_seed = int(head_filename)

    # static settings:
    upper_settings.use_clump_noise = True
    lower_settings.use_clump_noise = True
    upper_settings.clump_noise_size = 0.5
    lower_settings.clump_noise_size = 0.5





def placePlica():
    disp = parameters_json["plicaDisp"]
    
    head = bpy.data.objects["head"]
    plica = bpy.data.objects["Eye_Plica"]
    
    # recenters and applies
    plica.location = disp
    plica.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    guideP1 = head.data.vertices[559].co
    guideP2 = head.data.vertices[546].co
    guideAvg = [ (guideP1[0]+guideP2[0])/2, (guideP1[1]+guideP2[1])/2, (guideP1[2]+guideP2[2])/2 ]
    plica.location = guideAvg

    dist = math.sqrt(plica.location[0]**2+plica.location[1]**2+plica.location[2]**2)
    plica.location = vector_scale(plica.location, parameters_json["plicaDist"] / dist)

    
def AddWarp():
    head = bpy.data.objects["head"]
    upper = bpy.data.objects["upper"]
    lower = bpy.data.objects["lower"]
    head.modifiers.new("Warp_Modifier", 'WARP')
    
    pupil_empty = bpy.data.objects["pupil-empty"]
    cornea_empty = bpy.data.objects["cornea-empty"]
    
    head_mod = head.modifiers["Warp_Modifier"]
    upper_mod = upper.modifiers["Warp"]
    lower_mod = lower.modifiers["Warp"]
    warp_mods = [ head_mod, upper_mod, lower_mod ]
    
    for WARP_mod in warp_mods:
        WARP_mod.object_from = pupil_empty
        WARP_mod.object_to = cornea_empty
        WARP_mod.strength = 0.40
        WARP_mod.falloff_radius = 0.009
        WARP_mod.falloff_type = "CURVE"

def SettingSceneMisc():
	bpy.context.scene.render.resolution_x = 640
	bpy.context.scene.render.resolution_y = 480
	bpy.context.scene.camera = bpy.data.objects["Camera"]

def SettingDOF():
	camera = bpy.data.objects["Camera"]
	camera.data.dof.use_dof = True
	camera.data.dof.focus_object = bpy.data.objects["Eye.Wetness"]
	camera.data.dof.aperture_fstop = 0.5
	camera.data.dof.aperture_blades = 8





# Init
parameters_json = initParameters()

# Entry
ImportHeadModel()
Importeye()
moveHead()
cleanEye()
fixSkin()
lashesAndPlica()
placeLashes()
SetLashes()
placePlica()
AddWarp()
SettingSceneMisc()
SettingDOF()

