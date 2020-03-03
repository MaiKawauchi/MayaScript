import pymel.core as pm
import random as rand

count = 0
while count < 300:
    Cube = pm.polyCube()
    
    # uniform : 分布する範囲を指定 #
    # gauss : ガウス分布　#
    # gammavariate : ガウス分布に基づいた乱数　#
    x = rand.gammavariate(1, 10)
    y = rand.gammavariate(1, 10)
    z = rand.gammavariate(1, 10)
    
    pm.move(x, y, z, a = True)
    count += 1
