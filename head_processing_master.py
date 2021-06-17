import bpy

def moveHead():
    
    # manual data
    head_scale = [0.96, 0.96, 0.96]
    head_shift = [-2.7746, 9.4176, -29.008]

    # select the head model
    head=bpy.data.objects["Head"]

    # move and scale the model so the eye is in place
    for i in range(3):
        head.location[i] = head_shift[i]/100
        head.scale[i] = head_scale[i]
        
    # appliest the transform 
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def cleanEye():
    # Arbitrarily sized 1 cm hole so you can see the retina
    eyeball_radius = 0.01

    head=bpy.data.objects["Head"]

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

def fixSkin():
    # input
    headmodel_name = "F"

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

def lashesAndPlica():
    # gets the images from the jpg folder
    blender_path = "//head_components.blend"
    blender_path = bpy.path.abspath(blender_path)
    ImportBlenderFile(blender_path)


def parent():
    # gets the objects
    head = bpy.data.objects["Head"]
    lower = bpy.data.objects["lower"]
    upper = bpy.data.objects["upper"]
    plica = bpy.data.objects["Eye_Plica"]

    # sets the parent to head
    lower.parent = head
    upper.parent = head
    plica.parent = head

