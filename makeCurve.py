import pymel.core as pm
import math

height = 1.4 # math.sqrt(2./3.)*2

a1 = (0, height, 0)
a2 = (0, -height, 0)
b1 = (-1, 0, -1)
b2 = (1, 0, 1)
c1 = (-1, 0, 1)
c2 = (1, 0, -1)


# d : degree�@�Ȑ��̎����@#
# n : name �I�u�W�F�N�g�̖��O�@#
tmpCurve = pm.curve(d = 1, p = [b1, c1, a1, b2, c2, a1, b1, a2, c2, b1, c1, a2, b2, c1], n = 'square' )
# rpo : replaceOriginal�@���̃J�[�u�������̃J�[�u�ɒu�������� #
pm.closeCurve( tmpCurve, rpo = True )
