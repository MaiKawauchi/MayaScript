import pymel.core as pm

def texReload():
    for tex in pm.ls(type = 'file'):
        filePath = tex.fileTextureName.get()
        if not filePath:
            continue
        
        tex.fileTextureName.set( filePath )        
    print ('texture reload compleate!')

texReload()