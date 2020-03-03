import pymel.core as pm
import math

height = 1.4 # math.sqrt(2./3.)*2

a1 = (0, height, 0)
a2 = (0, -height, 0)
b1 = (-1, 0, -1)
b2 = (1, 0, 1)
c1 = (-1, 0, 1)
c2 = (1, 0, -1)


# d : degree　曲線の次数　#
# n : name オブジェクトの名前　#
tmpCurve = pm.curve(d = 1, p = [b1, c1, a1, b2, c2, a1, b1, a2, c2, b1, c1, a2, b2, c1], n = 'square' )
# rpo : replaceOriginal　元のカーブを閉じた後のカーブに置き換える #
pm.closeCurve( tmpCurve, rpo = True )
