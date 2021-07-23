AutoProcessingComplete = "AutoProcessingScript.py"
AutoEyelidWeight = "Eyelid_AutoWeight.py"
LinearEyelidWeight = "LinearEdgeWeightGeneration.py"

exec(open(AutoProcessingComplete).read())
exec(open(AutoEyelidWeight).read())
exec(open(LinearEyelidWeight).read())
