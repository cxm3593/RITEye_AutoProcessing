import bpy
import json
import math

eye_filepath = "//Eye.blend"
parameters_json = {}

def initParameters():
    with open("AutoScriptParameters.json") as p_json:
        parameters_str = p_json.read()
    parameters_json = json.loads(parameters_str)
    return parameters_json

def vector_subtract(a,b):
    c = [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
    return c

def ImportHeadModel():
    # file paths
    M12_filePath= "//Head Models\M\OBJ\Sub Division\Head.OBJ" # this does not
    M12_filePath_abs = bpy.path.abspath(M12_filePath) # this works

    # Import
    bpy.ops.import_scene.obj(filepath=M12_filePath_abs)
    head = bpy.context.selected_objects[0]
    head.name = "Head"

    # shade smooth
    bpy.ops.object.shade_smooth()
    
def moveHead():
    # select the head model
    head=bpy.data.objects["Head"]
    
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

    head=bpy.data.objects["Head"]
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
    # input
    headmodel_name = "M"

    # gets the head
    head=bpy.data.objects["Head"]

    # applies the skin material
    skin = bpy.data.materials["skin"]
    head.active_material = skin

    # gets the image nodes
    c1_node = skin.node_tree.nodes.get('c1')    # color map 1 
    c2_node = skin.node_tree.nodes.get('c2')    # color map 2 
    s1_node = skin.node_tree.nodes.get('s1')    # specularity map
    n_node = skin.node_tree.nodes.get('n')      # normal map

    # gets the images from the jpg folder
    jpg_path = "//Head Models\\" + headmodel_name + "\Textures\JPG\\"
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
    
    
def ImportBlenderFile(filepath):
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to): # link=False : not to modify the original model
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None or bpy.types.BlendDataWorkSpaces:
          bpy.context.collection.objects.link(obj)
        
        #rename 
        name_array = obj.name.split('.')
        newname = name_array[0]
        if newname == "Eye":                # hack fix
            newname = "Eye.Wetness"
        obj.name = newname
          
def Importeye():
    ImportBlenderFile(eye_filepath)
          
def parent():
    # gets the objects
    head = bpy.data.objects["Head"]
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
    
def placeLashes():
    # gets the lashes
    head = bpy.data.objects["Head"]
    upper = bpy.data.objects["upper"]
    lower = bpy.data.objects["lower"]
    
    # appliest the transform 
    upper.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    lower.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # wraps the lashes around the model
    upperEdges = parameters_json["upperEdges"]
    lowerEdges = parameters_json["lowerEdges"]
    upperLidVerts = parameters_json["upperLidVerts"]
    lowerLidVerts = parameters_json["lowerLidVerts"]
    
    # warps the lashes geometry 
    placeLash(lower, head, lowerLidVerts, lowerEdges)
    placeLash(upper, head, upperLidVerts, upperEdges)
    
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

    
def AddWarp():
    head = bpy.data.objects["Head"]
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

# Init
parameters_json = initParameters()

# Entry
ImportHeadModel()
moveHead()
cleanEye()
fixSkin()
Importeye()
lashesAndPlica()
placeLashes()
AddWarp()

