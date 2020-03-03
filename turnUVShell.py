import pymel.core as pm
import math

def getAngle( pt1, pt2 ):
    u = pt2[0] - pt1[0]
    v = pt2[1] - pt1[1]
    
    # x��(u��)���炻�̍��W�܂ł��`����(arc)�����߂�.�߂�l��radian #
    rad = math.atan2( v, u )
    return math.degrees( rad )
    
def alignUvShell():
    # fl : flatten  �ȗ������Ɏ擾�@#
    uvs = pm.selected( fl = True )
    # uvs[0]  : 1�_�ڂ�UV
    # uvs[-1] :�@�Ō��UV

    # polyEditUV���g����UV���W�����߂� #
    # q : query �₢���킹�t���O �@�@�@�@�@#
    pt1 = pm.polyEditUV( uvs[0], q = True )
    pt2 = pm.polyEditUV( uvs[-1], q = True )
    angle = getAngle( pt1, pt2 )
    
    pm.runtime.SelectUVShell()
    pm.polyEditUV( pu = pt1[0], pv = pt1[1], a = 90-angle )
    
    
alignUvShell()