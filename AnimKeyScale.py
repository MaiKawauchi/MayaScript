#--------------------------------------------------------------------------
#
# ScriptName : AnimKeyScale
# Contents   : アニメーションのキーをスケールするツール
#
#--------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys

import maya.cmds as cmds
import pymel.core as pm
from maya import OpenMayaUI

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


#--------------------------------------------------------------------------#
def AriNumber2to10(boolList):
    AnimKeyScale_UI_Frame = cmds.ls(sl=True)



#--------------------------------------------------------------------------#
def settingSave():
    AnimKeyScale_UI_Frame = cmds.ls(sl=True)
    AnimKeyScale_UI_timeRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_valRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_timeScale = cmds.ls(sl=True)
    AnimKeyScale_UI_valScale = cmds.ls(sl=True)

    cmds.floatField('timePivot', q=1, v=AriAniKeyScale_UI_timeScale[2])
    cmds.floatField('timeAbsolute', q=1, v=AriAniKeyScale_UI_timeScale[1])
    cmds.floatField('timeScale', q=1, v=AriAniKeyScale_UI_timeScale[0])
    cmds.optionVar(floatValue=['AriAniKeyScale_timePivot', timePivot])
    cmds.optionVar(floatValue=['AriAniKeyScale_timeAbsolute', timeAbsolute])
    cmds.optionVar(floatValue=['AriAniKeyScale_timeScale', timeScale])
    cmds.floatField('valPivot', q=1, v=AriAniKeyScale_UI_valScale[2])
    cmds.floatField('valAbsolute', q=1, v=AriAniKeyScale_UI_valScale[1])
    cmds.floatField('valScale', q=1, v=AriAniKeyScale_UI_valScale[0])
    cmds.optionVar(floatValue=['AriAniKeyScale_valPivot', valPivot])
    cmds.optionVar(floatValue=['AriAniKeyScale_valAbsolute', valAbsolute])
    cmds.optionVar(floatValue=['AriAniKeyScale_valScale', valScale])
    timeSelect = 1
    
    for i in range(5):
        if(cmds.radioButton(q=1, selected=AriAniKeyScale_UI_timeRadio[i])): 
            timeSelect = i
    
    cmds.optionVar(intValue=['AriAniKeyScale_timeRadio', timeSelect])
    valueSelect = 1
    
    for i in range(5): 
        if(cmds.radioButton(q=1, sl=AriAniKeyScale_UI_valRadio[i])): 
            valueSelect = i
            
    cmds.optionVar(intValue=['AriAniKeyScale_valueRadio', valueSelect])
    closeVal[3]
    cmds.frameLayout('closeVal[0]', q=1, cl=AriAniKeyScale_UI_Frame[0])
    cmds.frameLayout('closeVal[1]', q=1, cl=AriAniKeyScale_UI_Frame[1])
    closeVal10 = AriNumber2to10(closeVal)
    cmds.optionVar(intValue=['AriAniKeyScale_frameCollapse', closeVal10])

#--------------------------------------------------------------------------#
def settingLoad():
    AnimKeyScale_UI_Frame = cmds.ls(sl=True)
    AnimKeyScale_UI_timeRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_valRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_timeScale = cmds.ls(sl=True)
    AnimKeyScale_UI_valScale = cmds.ls(sl=True)


#--------------------------------------------------------------------------#
# plusTrue:
# valTrue : 0 = Time, 1 = Value
#--------------------------------------------------------------------------#
def AnimKeyScale_GO(plusTrue, valTrue):
    AnimKeyScale_UI_valScale = cmds.ls(sl=True)
    AnimKeyScale_UI_timeScale = cmds.ls(sl=True)
    AnimKeyScale_UI_valRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_timeRadio = cmds.ls(sl=True)

    scale = 2
    targetScale = 2
    pivVal = 0

    # 数値入力で得られた値を保持
    # Value
    if(valTrue):
        scale = cmds.floatField(q=1, v='AnimKeyScale_UI_valScale[0]')
        targetScale = cmds.floatField(q=1, v='AnimKeyScale_UI_valScale[1]')
        pivVal = cmds.floatField(q=1, v='AnimKeyScale_UI_valScale[2]')
    # Time
    else:
        scale = cmds.floatField(q=1, v='AnimKeyScale_UI_timeScale[0]')
        targetScale = cmds.floatField(q=1, v='AnimKeyScale_UI_timeScale[1]')
        pivVal = cmds.floatField(q=1, v='AnimKeyScale_UI_timeScale[2]')
    
    # / のとき
    if(plusTrue==0):
        scale = 1.0/scale
    
    # キーセットは、アニメーションカーブ上の指定したタイムレンジ内のキーグループをリスト
    cmds.keyframe('aniCurveList[]', q=1, selected=True, name=True)
    totalMax = 0
    totalMin = 0
    urveTotal = 0

    for curve in aniCurveList:
        cmds.keyframe('select_indexList[]', q=1, selected=True, indexValue=curve)
        cmds.keyframe('select_timeList[]', q=1, selected=True, timeChange=curve)
        cmds.keyframe('select_valueList', q=1, selected=True, valueChange=curve)
        cmds.keyframe('all_indexList', q=1, indexValue=curve)
        cmds.keyframe('all_timeList', q=1, timeChange=curve)
        cmds.keyframe('all_valList', q=1, valueChange=curve)
        pivMode = 0

        # ラジオボタンが選択されているとき pivMode の値を変更する
        # Vlaue
        if(valTrue):
            if(cmds.radioButton('AriAniKeyScale_UI_valRadio[0]', q=1, selected=True)): pivMode = 0
            if(cmds.radioButton('AriAniKeyScale_UI_valRadio[1]', q=1, selected=True)): pivMode = 1
            if(cmds.radioButton('AriAniKeyScale_UI_valRadio[2]', q=1, selected=True)): pivMode = 2
            if(cmds.radioButton('AriAniKeyScale_UI_valRadio[3]', q=1, selected=True)): pivMode = 3
        # Time
        else:
            if(cmds.radioButton('AriAniKeyScale_UI_timeRadio[0]', q=1, selected=True)): pivMode = 0
            if(cmds.radioButton('AriAniKeyScale_UI_timeRadio[1]', q=1, selected=True)): pivMode = 1
            if(cmds.radioButton('AriAniKeyScale_UI_timeRadio[2]', q=1, selected=True)): pivMode = 2
            if(cmds.radioButton('AriAniKeyScale_UI_timeRadio[3]', q=1, selected=True)): pivMode = 3

        max = 0
        min = 0
        total = 0
        
        for j in (size(select_indexList)):
            selIndex = select_indexList[j]
            value=[]

            # Value
            if(valTrue):
                cmds.keyframe('value', index=selIndex, q=1, valueChange=curve)
            # Time
            else:
                cmds.keyframe('value', index=selIndex, q=1, timeChange=curve)
            
            if(j==0):
                max = value[0]
                min = value[0]
            if(max < value[0]): max = value[0]
            if(min > value[0]): min = value[0]
            total += value[0]
            
        center = (max+min)/2.0

        # Absolute のとき
        if(plusTrue==2):
            scale = targetScale/(max-min)
        
        # pivMode の値によって piv の位置を決める
        piv = 0
        if(pivMode==0): piv = min
        if(pivMode==1): piv = center
        if(pivMode==2): piv = max
        if(pivMode==3): piv = pivVal 
        if(plusTrue==3 or plusTrue==4):
            if(curveTotal==0):
                totalMax = max
                totalMin = min
                
            if(totalMax < max): totalMax = max
            if(totalMax > min): totalMin = min
            curveTotal+1
            continue

        evalText = 'scaleKey '
        for j in (size(select_indexList)):
            selIndex = select_indexList[j]
            evalText = evalText + ('-index '+selIndex+' ')
            
        if(valTrue): evalText = evalText + ('-vs '+ scale +'-vp '+ piv+' '+curve)
        else: valText = evalText + ('-ts '+ scale +'-tp '+ piv+' '+curve)
        mel.eval(evalText)

    # Input Scale Pivot の Get ボタン
    if(plusTrue==3):
        totalPiv = (totalMax+totalMin)/2.0
        # Value
        if(valTrue): 
            cmds.floatField('AriAniKeyScale_UI_valScale[2]', e=True, v=totalPiv)
        # Time
        else: 
            cmds.floatField('AriAniKeyScale_UI_timeScale[2]', e=True, v=totalPiv)
    
    # Absolute Scale の Get ボタン
    if(plusTrue==4):
        size = totalMax-totalMin
        # Value
        if(valTrue): 
            cmds.floatField(' AriAniKeyScale_UI_valScale[1]', e=True, v=size)
        # Time
        else: 
            cmds.floatField('AriAniKeyScale_UI_timeScale[1]', e=True, v=size)
            
    settingSave()





#--------------------------------------------------------------------------#
def AnimKeyScale_changeRadio():
    AnimKeyScale_UI_valScale = cmds.ls(sl=True)
    AnimKeyScale_UI_timeScale = cmds.ls(sl=True)
    AnimKeyScale_UI_valRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_timeRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_button = cmds.ls(sl=True)

    # Index が選択されたら、数値入力と Get ボタンを有効にする
    # Time
    if(cmds.radioButton(q=1, select='AnimKeyScale_UI_timeRadio[3]')):
       cmds.button('AnimKeyScale_UI_button[0]', e=1, enable=True)
       cmds.floatField('AnimKeyScale_UI_timeScale[2]', e=1, enable=True)
    else:
        cmds.button('AnimKeyScale_UI_button[0]', e=1, enable=False)
        cmds.floatField('AnimKeyScale_UI_timeScale[2]', e=1, en=False)

    # Value
    if(cmds.radioButton(q=1, select='AnimKeyScale_UI_valRadio[3]')):
        button('AnimKeyScale_UI_button[1]', e=1, en=True)
        cmds.floatField('AnimKeyScale_UI_valScale[2]', e=1, enable=True)
    else:
        cmds.button('AnimKeyScale_UI_button[1]', e=1, enable=False)
        cmds.floatField('AnimKeyScale_UI_valScale[2]', e=1, en=False)


#--------------------------------------------------------------------------#
def AnimKeyScale_setWindowSize():	
	cmds.window('AnimKeyScale', e=1, h=44)


#--------------------------------------------------------------------------#
def AnimKeyScale():
    AnimKeyScale_UI_Frame = cmds.ls(sl=True)
    AnimKeyScale_UI_timeRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_valRadio = cmds.ls(sl=True)
    AnimKeyScale_UI_timeScale = cmds.ls(sl=True)
    AnimKeyScale_UI_valScale = cmds.ls(sl=True)
    AnimKeyScale_UI_button = cmds.ls(sl=True)

    if (cmds.window('AnimKeyScale', ex=True)==True):
        cmds.deleteUI('AnimKeyScale', window=True)
        cmds.deleteUI('AnimKeyScale', window=True)
    
    #--------------------------------------------------------------------------#
    cmds.window('AnimKeyScale', tlb=1, title='AnimKeyScale', w=200, h=120 )
    cmds.columnLayout( adj=True )

    #------------------------------- Time -------------------------------------#
    # Time Collapse
    AnimKeyScale_UI_Frame1 = cmds.frameLayout( label='Time', cll=True, cl=False, cc='AnimKeyScale_setWindowSize()' )
    cmds.columnLayout( adj=True )

    # Scale Pvot
    cmds.radioCollection()
    cmds.rowLayout( nc=4 )
    radioCollection1 = cmds.radioCollection()
    cmds.radioButton('AnimKeyScale_UI_timeRadio[0]', label=u'Min', onc='AnimKeyScale_changeRadio()')
    cmds.radioButton('AnimKeyScale_UI_timeRadio[1]', label=u'Center', onc='AnimKeyScale_changeRadio()', sl=True)
    cmds.radioButton('AnimKeyScale_UI_timeRadio[2]', label=u'Max', onc='AnimKeyScale_changeRadio()')
    cmds.setParent( '..' )

    # Input Scale Pivot
    cmds.rowLayout( nc=4 )
    cmds.radioButton('AnimKeyScale_UI_timeRadio[3]', label=u'Input', onc='AnimKeyScale_changeRadio()')
    cmds.floatField('AnimKeyScale_UI_timeScale[2]', value=0)
    cmds.button('AnimKeyScale_UI_button[0]',  w=30, label='Get', command='AnimKeyScale_GO(3,0);')
    cmds.setParent( '..' )

    # Absolute Scale
    cmds.rowLayout( nc=3, adj=1 )
    cmds.floatField('AnimKeyScale_UI_timeScale[1]', value=100)
    cmds.button(w=30, label='Get', command='AnimKeyScale_GO(4,0);')
    cmds.button(w=60, label='Absolute', command='AnimKeyScale_GO(2,0);')
    cmds.setParent( '..' )

    # Run
    cmds.rowLayout( nc=4, adj=1 )
    cmds.floatField('AnimKeyScale_UI_timeScale[0]', value=1.5)
    cmds.button(w=20, label='/', command='AnimKeyScale_GO(0,0);')
    cmds.iconTextButton(w=70, bgc=[0.5, 0.4, 0.4], image1='constrainDragX.png', command='AnimKeyScale_GO(1,0);')

    # Up Parent
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )



    #-------------------------------- Value -----------------------------------#
    # Value Collapse
    AnimKeyScale_UI_Frame2 = cmds.frameLayout( l='Value', cll=True, cl=False, cc='AnimKeyScale_setWindowSize()' )
    cmds.columnLayout( adj=True )
    
    # Scale Pvot
    cmds.radioCollection()
    cmds.rowLayout( nc=4 )
    radioCollection2 = cmds.radioCollection()
    cmds.radioButton('AnimKeyScale_UI_valRadio[0]', label=u'Min', onc='AnimKeyScale_changeRadio()')
    cmds.radioButton('AnimKeyScale_UI_valRadio[1]', label=u'Center', onc='AnimKeyScale_changeRadio()', sl=True)
    cmds.radioButton('AnimKeyScale_UI_valRadio[2]', label=u'Max', onc='AnimKeyScale_changeRadio()')
    cmds.setParent( '..' )

    # Input Scale Pivot
    cmds.rowLayout( nc=4 )
    cmds.radioButton('AnimKeyScale_UI_valRadio[3]', label=u'Input', onc='AnimKeyScale_changeRadio()')
    cmds.floatField('AnimKeyScale_UI_valScale[2]', value=0)
    cmds.button('AnimKeyScale_UI_button[1]',  w=30, label='Get', command='AnimKeyScale_GO(3,1);')
    cmds.setParent( '..' )

    # Absolute Scale
    cmds.rowLayout( nc=3, adj=1 )
    cmds.floatField('AnimKeyScale_UI_valScale[1]', value=1)
    cmds.button(w=30, label='Get', command='AnimKeyScale_GO(4,1);')
    cmds.button(w=60, label='Absolute', command='AnimKeyScale_GO(2,1);')
    cmds.setParent( '..' )

    # Run
    cmds.rowLayout( nc=4, adj=1 )
    cmds.floatField('AnimKeyScale_UI_valScale[0]', value=1.5)
    cmds.button(w=20, label='/', command='AnimKeyScale_GO(0,1);')
    cmds.iconTextButton(w=70, bgc=[0.4, 0.5, 0.4], image1='constrainDragY.png', command='AnimKeyScale_GO(1,1);')

    # Up Parent
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )

    #--------------------------------------------------------------------------#
    cmds.showWindow()
    cmds.refresh()


AnimKeyScale()