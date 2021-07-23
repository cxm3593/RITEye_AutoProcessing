# RITEyes - Auto Processing Script

## Intro:

This is a project that automatically process unprocessed head model to get a refined model ready for RITEyes rendering pipeline.

## Content:

In current stage, there are three script files that are important to the auto processing workflow:

1. AutoProcessScript.py
2. Eyelid_AutoWeight.py
3. LinearEdgeWeightGeneration.py

## How to use:

To use the program, run these three files in the given order, or run with the AutoScript_ExternalLink.py in Blender.

PS: Put the head model files into the working directory.
[Example head file](https://drive.google.com/file/d/1MER-A9Ebu0UUv_p7dqHKYtGui0RrzcvB/view?usp=sharing) (unzip into working directory)

## Script Details For Developer:

### AutoProcessScript:

This is the starting script setting up most parts of the rendering scene. Except for anything related to the blinking animation.

This script reads the json file AutoScriptParameters.json for variables and parameters



### Eyelid_AutoWeight:

This is the script setting up Armatures, modifiers and anything related to armature animation for blinking. But the weight generation on the eyelid is outdated and overwritten by the LinearEdgeWeightGeneration

### Linear EdgeWeight Generation:

This is the script for the weight generation of each vertices on the upper and lower eyelid.
