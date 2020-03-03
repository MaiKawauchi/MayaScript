import maya.cmds as cmds

if cmds.window("PyWindow", exists = True):
    cmds.deleteUI("PyWindow")

Create_Window = cmds.window(
    "PyWindow",
    title = "pythonScript_Panel",
    width = 300,
    height = 300,
    sizeable = True,
    minimizeButton = False,
    maximizeButton = False
    )
cmds.columnLayout(adj = True)

imagepath = cmds.internalVar(upd = True) + "icons/Window_image02.jpg"

cmds.image( w=300, h=100, image = imagepath )
cmds.separator(height = 10)
cmds.text("Create And Rename Tool")
cmds.separator(h = 10)

sliderW = cmds.intSliderGrp(l = "Width", min = 1.0, max = 30.0, field = True, v = 1.0)
sliderH = cmds.intSliderGrp(l = "Hight", min = 1.0, max = 30.0, field = True, v = 1.0)
sliderD = cmds.intSliderGrp(l = "Depth", min = 1.0, max = 30.0, field = True, v = 1.0)

cmds.button(l = "Create Cube", c = "SetCube()")
cmds.separator(h = 20)

Re_name = cmds.textFieldGrp(l = "Rename", ed = True, text = "InputChangeName")
cmds.button(l = "Rename_Cube Name", c = "Rename_Set()")
cmds.showWindow(Create_Window)


def SetCube():
    setCubeWidth = cmds.intSliderGrp(sliderW, q = True, v = True)
    setCubeHidth = cmds.intSliderGrp(sliderH, q = True, v = True)
    setCubeDepth = cmds.intSliderGrp(sliderD, q = True, v = True)

    GetCube = cmds.polyCube(
        w = setCubeWidth,
        h = setCubeHidth,
        d = setCubeDepth,
        n = "SRT_Cube",
        ch = False
        )
    cmds.move(0, setCubeHidth/2.0, 0, GetCube, r = True)

def Rename_Set():
    Set_name = cmds.textFieldGrp(Re_name, q = True, text = True)
    cmds.rename(Set_name)