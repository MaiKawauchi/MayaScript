import pymel.core as pm

def select_similar_type():
    obj = pm.selected()[0]
    if isinstance(obj, pm.nodetypes.Transform):
        obj = obj.getShape()
        
        result = pm.ls( type = obj.type() )
        pm.select( result )
        
        return result
