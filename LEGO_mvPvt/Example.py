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

try:
    import shiboken
except:
    import shiboken2 as shiboken

ptr = OpenMayaUI.MQtUtil.mainWindow()
parent = shiboken.wrapInstance(long(ptr), QWidget)

#-----------------------------------------------------#
class maskUI(QMainWindow):
    def __init__(self):
        super(maskUI, self).__init__()
    
    def PaletteUI(self):
        setColors = ['#CC0066', '#990066']
        Palette = QPalette()
        gradient = QLinearGradient(QRectF(
            self.rect()).topLeft(),
            QRectF(self.rect()).topRight()
        )
        gradient.setColorAt(0.0, setColors[0])
        gradient.setColorAt(1.0, setColors[1])
        Palette.setBrush(QPalette.Background, QBrush(gradient))

        path = QPainterPath()
        path.addRoundedRect(self.rect(), 4, 4)
        region = QRegion(path.toFillPolygon().toPolygon())

        self.setMask(region)
        self.setPalette(Palette)

#-----------------------------------------------------#
# Mouse Event
# Windowをリサイズ
#-----------------------------------------------------#
class setMainWindow(maskUI):
    def __init__(self):
        super(setMainWindow, self).__init__()
       # 受け取るボタンをinstallEventFilterという関数でeventに登録
        self.installEventFilter(self)
        self.resize_mode = None

    def mouseReleaseEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()

    #-------------------------------------------------#
    # 上下左右斜のそれぞれ端から8pxの位置に
    # マウスを押した場合、どの位置にあるかを取得する
    #-------------------------------------------------#    
    def mousePressEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()
        borderWidth = 8
        resizeWidth = self.minimumWidth() != self.maximumWidth()
        resizeHeight = self.minimumHeight() != self.maximumHeight()

        self.pre_size_x = self.size().width()
        self.pre_size_y = self.size().height()
        self.size_w = self.size().width()
        self.size_h = self.size().height()
        self.sub_w = self.size_w - self.mc_x
        self.sub_h = self.size_h - self.mc_y
        resize_mode = None

        # Width のリサイズ
        if resizeWidth is True:
            if self.mc_x < borderWidth:
                resize_mode = "left"
            if self.sub_w < borderWidth:
                resize_mode = "right"
        
        # Height のリサイズ
        if resizeHeight is True:
            if self.mc_y < borderWidth:
                resize_mode = "top"
            if self.sub_h < borderWidth:
                resize_mode = "bottom"

        # Width と Height のリサイズ
        if resizeWidth is True and resizeHeight is True:
            if self.mc_x <= borderWidth and self.mc_y <= borderWidth:
                resize_mode = 'top_left'
            if self.sub_w <= borderWidth and self.sub_h <= borderWidth:
                resize_mode = 'bottom_right'
            if self.sub_w <= borderWidth and self.mc_y <= borderWidth:
                resize_mode = 'top_right'
            if self.mc_x <= borderWidth and self.sub_h <= borderWidth:
                resize_mode = 'bottom_left'
            if self.mc_x >= borderWidth and self.mc_y >= borderWidth\
                and self.sub_w >= borderWidth\
                    and self.sub_h >= borderWidth:
                resize_mode = 'center'

        self.resize_mode = resize_mode
        return self.resize_mode

    #-------------------------------------------------#
    # eventを受け取る
    #-------------------------------------------------#
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            return True
        if event.type() == QEvent.Type.HoverMove:
            pos = event.pos()
            cur_dict = {
                'right': Qt.SizeHorCursor,
                'left': Qt.SizeHorCursor,
                'top': Qt.SizeVerCursor,
                'bottom': Qt.SizeVerCursor,
                'top_left': Qt.SizeFDiagCursor,
                'bottom_right': Qt.SizeFDiagCursor,
                'top_right': Qt.SizeBDiagCursor,
                'bottom_left': Qt.SizeBDiagCursor,
                'center': Qt.ArrowCursor,
                None: Qt.ArrowCursor
                }
            cur = cur_dict[self.resize_mode] 
            current_cur = QApplication.overrideCursor().shape()
            cur_set = cur_dict[self.resize_mode]
            if cur != current_cur:
                QApplication.changeOverrideCursor(cur_set)
                return True
            return True

        if event.type() == QEvent.Type.Leave:
            QApplication.restoreOverrideCursor()
            return True
        else:
            return False

    #-------------------------------------------------#
    # def mouseMoveEvent(self, pos)でどの位置にあるか
    # によってresize処理をどう実行させるかを設定
    #-------------------------------------------------#
    def mouseMoveEvent(self, pos):
        self.PaletteUI()
        self.win_x = pos.globalX() - self.mc_x
        self.win_y = pos.globalY() - self.mc_y

        if self.resize_mode is None:
            self.resize_mode = 'center'

        if self.resize_mode is 'center':
            self.move(self.win_x, self.win_y)

        else:
            self.re_w = self.size().width()
            self.re_h = self.size().height()
            if 'right' in self.resize_mode:
                self.re_w = pos.x() + self.sub_w
                self.resize(self.re_w, self.re_h)

            if 'bottom' in self.resize_mode:
                self.re_h = pos.y() + self.sub_h
                self.resize(self.re_w, self.re_h)

            if 'left' in self.resize_mode:
                self.resub_w = pos.x() - self.mc_x
                self.re_w = self.re_w - self.resub_w
                self.resize(self.re_w, self.re_h)
                if self.size().width() != self.pre_size_x:
                    self.win_x = pos.globalX() - self.mc_x
                    self.move(self.win_x, self.pos().y())
                self.pre_size_x = self.size().width() 

            if 'top' in self.resize_mode:
                self.resub_h = pos.y() - self.mc_y
                self.re_h = self.re_h - self.resub_h
                self.resize(self.re_w, self.re_h)
                if self.size().height() != self.pre_size_y:
                    self.win_y = pos.globalY() - self.mc_y
                    self.move(self.pos().x(), self.win_y)
                self.pre_size_y = self.size().height()

#-----------------------------------------------------#
# CloseButton 専用の class
# シグナル closed を作成し,Close専用の QPushButton を用意
#-----------------------------------------------------#
class SysButton(QPushButton):
    closed = Signal()

    def __init__(self, *args, **kwargs):
        super(SysButton, self).__init__(*args, **kwargs)
        self.clicked.connect(self.__closed)

    def __closed(self):
        self.closed.emit()

#-----------------------------------------------------#
# Pivot移動
#-----------------------------------------------------#
class movePivots(QWidget):
    def __init__(self, *args, **kwargs):
        super(movePivots, self).__init__(*args, **kwargs)
    
        #-----------------------------------------------------#
        # 空の格子状配置(Grid)レイアウトを作る
        self.QG = QGridLayout()
        self.setLayout(self.QG)
    
        #-----------------------------------------------------#
        #Center Pivot 
        self.btnCenter = QPushButton('Center Pivot')
        self.QG.addWidget(self.btnCenter, 1, 0, 1, 3)
        self.btnCenter.clicked.connect(self.centerPiv)
    
        #-----------------------------------------------------#
        # Add Line
        self.line = QFrame()
        self.line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.QG.addWidget(self.line, 2, 0, 1, 3)

        #-----------------------------------------------------#
        # Button of Select Move Pivot 
        self.btnXmax = QPushButton('X Max')
        self.QG.addWidget(self.btnXmax, 3, 0)
        self.btnXmax.clicked.connect(self.moveXmax)

        self.btnYmax = QPushButton('Y Max')
        self.QG.addWidget(self.btnYmax, 3, 1)
        self.btnYmax.clicked.connect(self.moveYmax)

        self.btnZmax = QPushButton("Z Max")
        self.QG.addWidget(self.btnZmax, 3, 2)
        self.btnZmax.clicked.connect(self.moveZmax)

        self.btnXmin = QPushButton('X Min')
        self.QG.addWidget(self.btnXmin, 4, 0)
        self.btnXmin.clicked.connect(self.moveXmin)
        
        self.btnYmin = QPushButton('Y Min')
        self.QG.addWidget(self.btnYmin, 4, 1)
        self.btnYmin.clicked.connect(self.moveYmin)

        self.btnZmin = QPushButton('Z Min')
        self.QG.addWidget(self.btnZmin, 4, 2)
        self.btnZmin.clicked.connect(self.moveZmin)
    #-----------------------------------------------------#
    def centerPiv(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots(bbox.center(), absolute=True, worldSpace=True)

    def moveXmax(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([bbox.max().x, pvt.y, pvt.z], absolute=True, worldSpace=True)

    def moveXmin(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([bbox.min().x, pvt.y, pvt.z], absolute=True, worldSpace=True)
    
    def moveYmax(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([pvt.x, bbox.max().y, pvt.z], absolute=True, worldSpace=True)
    
    def moveYmin(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([pvt.x, bbox.min().y, pvt.z], absolute=True, worldSpace=True)
    
    def moveZmax(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([pvt.x, pvt.y, bbox.max().z], absolute=True, worldSpace=True)
    
    def moveZmin(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([pvt.x, pvt.y, bbox.min().z], absolute=True, worldSpace=True)

#-----------------------------------------------------#
# トランスフォームの操作
#-----------------------------------------------------#
class Transform(QWidget):
    def __init__(self, *args, **kwargs):
        super(Transform, self).__init__(*args, **kwargs)
        
        self.QH = QHBoxLayout() # 空の格子状配置(Grid)レイアウトを作る
        self.setLayout(self.QH)

        self.btnFreeze = QPushButton('Freeze Transform')
        self.QH.addWidget(self.btnFreeze)
        self.btnFreeze.clicked.connect(self.freezeTrans)

        self.btnReset = QPushButton('Reset Transform')
        self.QH.addWidget(self.btnReset)
        self.btnReset.clicked.connect(self.resetTrans)

    #-----------------------------------------------------#
    def freezeTrans(self):
        cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True ,preserveNormals = True)
    def resetTrans(self):
        sel = pm.selected()[0]
        bbox = sel.getBoundingBox(space = 'world')
        pvt = sel.getPivots(worldSpace = True)[0]
        sel.setPivots([0, 0, 0], absolute=True, worldSpace=True)

#-----------------------------------------------------#
# ウィジェットの配置
#-----------------------------------------------------#
class MainWidget(QWidget):
    closed = Signal()

    def __init__(self):
        super(MainWidget, self).__init__()

        #-----------------------------------------------------#
        self.sysButton = SysButton()
        self.sysButton.setText('Close')
        self.sysButton.closed.connect(self.__close)
        #-----------------------------------------------------#
        # 空の縦レイアウトを作る
        self.QV = QVBoxLayout()
        self.setLayout(self.QV)

        #-----------------------------------------------------#
        # Close Button
        self.QV.addWidget(self.sysButton, 0, 1)        

        #-----------------------------------------------------#        
        # Move Pivots
        self.movePvt = movePivots(self)
        self.QV.addWidget(self.movePvt)
        
        #-----------------------------------------------------#
        # Add Line
        self.line = QFrame()
        self.line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.QV.addWidget(self.line)
        #-----------------------------------------------------#
        # Transform
        self.trans = Transform(self)
        self.QV.addWidget(self.trans)

    def __close(self):
        self.closed.emit()

#-----------------------------------------------------#


#-----------------------------------------------------#
class Example(setMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.setWidget()
        self.PaletteUI()

    def initUI(self):
        self.setWindowOpacity(0.85) # 透明度
        self.setGeometry(300, 300, 270, 250) # ウィンドウサイズ
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    #----------------- Call Widget -----------------#
    def setWidget(self):
        mainWidget = MainWidget()
        mainWidget.closed.connect(self.gui_Close)
        self.setCentralWidget(mainWidget)

    #--------------- Close Animation ---------------#
    def gui_Close(self):
        self.timer = QTimer()
        self.timer.setInterval(600)
        self.timer.timeout.connect(self.close)
        self.timer.start()
        self.fade = QPropertyAnimation(self, "windowOpacity")
        self.fade.setStartValue(0.85)
        self.fade.setEndValue(0.0)
        self.fade.setKeyValueAt(0.5, 0.0)
        self.fade.setEasingCurve(QEasingCurve.InOutCubic)
        self.fade.setDuration(600)
        self.fade.start()
       
#-----------------------------------------------------#
def Example_UI():
    global Example_UI_ex
    app = QApplication.instance()
    Example_UI_ex = Example()
    Example_UI_ex.show()
    sys.exit()
    app.exec_()