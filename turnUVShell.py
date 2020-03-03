import pymel.core as pm
import math

def getAngle( pt1, pt2 ):
    u = pt2[0] - pt1[0]
    v = pt2[1] - pt1[1]
    
    # x軸(u軸)からその座標までが描く弧(arc)を求める.戻り値はradian #
    rad = math.atan2( v, u )
    return math.degrees( rad )
    
def alignUvShell():
    # fl : flatten  省略せずに取得　#
    uvs = pm.selected( fl = True )
    # uvs[0]  : 1点目のUV
    # uvs[-1] :　最後のUV

    # polyEditUVを使ってUV座標を求める #
    # q : query 問い合わせフラグ 　　　　　#
    pt1 = pm.polyEditUV( uvs[0], q = True )
    pt2 = pm.polyEditUV( uvs[-1], q = True )
    angle = getAngle( pt1, pt2 )
    
    pm.runtime.SelectUVShell()
    pm.polyEditUV( pu = pt1[0], pv = pt1[1], a = 90-angle )
    
    
alignUvShell()