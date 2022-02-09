import bpy
import sys
import argparse

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
parser = argparse.ArgumentParser()
parser.add_argument("--model_id")
args = parser.parse_args(argv)


model_name = args.model_id
blender_path = "D:/Softwares/Blender/blender.exe"

save_name = model_name
save_filepath = "//" + save_name + ".blend"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


AutoProcessingComplete = "AutoProcessingScript.py"
AutoEyelidWeight = "Eyelid_AutoWeight.py"
LinearEyelidWeight = "LinearEdgeWeightGeneration.py"
BinocularSetting = "BinocularSetting.py"

exec(open(AutoProcessingComplete).read(), {"model_name" : model_name})
exec(open(AutoEyelidWeight).read())
exec(open(LinearEyelidWeight).read())
exec(open(BinocularSetting).read())

bpy.ops.wm.save_mainfile()
