import subprocess
import shutil
import sys
import os

All_mode = False
if(len(sys.argv) == 1):
	All_mode = True

if (All_mode == True):
	for i in range(1, 25):
		process_modelName = str(i)

		blender_path = "D:/Softwares/Blender/blender.exe"

		empty_file_path = "./empty.blend"
		dest_file_path = "./"+process_modelName+".blend"
		#dest_file_path = os.path.join(os.getcwd(), "version9.1", process_modelName+".blend")

		print("Copying to", dest_file_path)
		shutil.copy(empty_file_path, dest_file_path)


		subprocess.call([blender_path, '-b', process_modelName+'.blend', '-P', 'AutoScript_ExternalLink.py', '--',
						"--model_id", process_modelName])
else:
	process_modelName = str(sys.argv[1])

	blender_path = "D:/Softwares/Blender/blender.exe"

	empty_file_path = "./empty.blend"
	dest_file_path = "./"+process_modelName+".blend"

	shutil.copy(empty_file_path, dest_file_path)


	subprocess.call([blender_path, '-b', process_modelName+'.blend', '-P', 'AutoScript_ExternalLink.py', '--',
					"--model_id", process_modelName])