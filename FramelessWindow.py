import os
import re
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

class setMainWindow(QMainWindow):
    def __init__(self):
        super(setMainWindow, self).__init__(parent)
    
    
    # マウスで移動するイベント処理
    def mouseReleaseEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()
    
    # x(), y() : マウスのプッシュ/リリース時のマウスカーソル位置情報を取得
    def mousePressEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()
    
    # globalX(), globalY() : イベント発生時のマウスカーソルのグローバル位置情報を取得
    def mouseMoveEvent(self, pos):
        winX = pos.globalX() - self.mc_x
        winY = pos.globalY() - self.mc_y
        # move : Windowを移動させる
        self.move(winX, winY)
        
        
    def paletteUI(self):
        setColors = ['#54354e', '#6a86c7']
        
        Palette = QPalette()
        gradient = QLinearGradient(QRectF(
        self.rect()).topLeft(),
        QRectF(self.rect()).topRight()
        )
        
        gradient.setColorAt(0.0, setColors[0])
        gradient.setColorAt(1.0, setColors[1])
        Palette.setBrush(QPalette.Background, QBrush(gradient))
        self.setPalette(Palette)

        # ウィンドウ自体の角を丸くする
        path = QPainterPath() # Pathを使って図形を作ることができる
        path.addRoundedRect(self.rect(), 10, 10)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region) # Window自体をマスク


# setMainWindowクラスを継承
class Example(setMainWindow):
    def __init__(self):
        # コンストラクタはsetMainWindowでmayaをparentしているので空
        super(Example, self).__init__()
        self.initUI()
        self.setButton()
        
    def initUI(self):
        self.setWindowOpacity(0.85)
        self.setGeometry(300, 300, 200, 150)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint) # フレームレスにする
        self.paletteUI() # ウィンドウの角を丸くする
    
    def setButton(self):
        btn = QPushButton("Close", self)
        btn.move(50, 50)
        btn.clicked.connect(self.close)
    
def Example_UI():
    global Example_UI_ex
    app = QApplication.instance()
    Example_UI_ex = Example()
    Example_UI_ex.show()
    sys.exit()
    app.exec_()
    

Example_UI()
