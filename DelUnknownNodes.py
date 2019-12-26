import pymel.core as pm

def del_unknownNodes():
    nodes = pm.ls( type = ['unknown', 'unknownDag', 'unknownTransform'] )
    for unknownObj in nodes:
        print unknownObj
        pm.lockNode( unknownObj, l = False )
        
        pm.delete(nodes)
