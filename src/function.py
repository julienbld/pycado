from OCC.gp import *
from OCC.BRepPrimAPI import *

def extrude(shape, x, y, z):
    vector = gp_Vec(x, y, z)

    return BRepPrimAPI_MakePrism(shape, vector)
