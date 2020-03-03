import pymel.core as pm

sel = pm.selected()[0]
bbox = sel.getBoundingBox( space = 'world' )
pvt = sel.getPivots( worldSpace = True )[0]

sel.setPivots( [pvt.x, bbox.min().y, pvt.z], absolute = True, worldSpace = True )