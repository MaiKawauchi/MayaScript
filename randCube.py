import pymel.core as pm
import random as rand

count = 0
while count < 300:
    Cube = pm.polyCube()
    
    # uniform : ���z����͈͂��w�� #
    # gauss : �K�E�X���z�@#
    # gammavariate : �K�E�X���z�Ɋ�Â��������@#
    x = rand.gammavariate(1, 10)
    y = rand.gammavariate(1, 10)
    z = rand.gammavariate(1, 10)
    
    pm.move(x, y, z, a = True)
    count += 1
