import pymel.core as pm

sel = pm.selected()

sel[-1].setPivots(sel[0].getPivots(worldSpace = True)[0],absolute = True, worldSpace = True)
