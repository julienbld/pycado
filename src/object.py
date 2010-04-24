from primitive import Primitive

from OCC.gp import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *

import display
import inspect

class pt(Primitive):
  def __init__(self, x, y, z):
    self.value = [x, y, z]
    self.data = gp_Pnt(x, y, z)
    Primitive.__init__(self)

class ln(Primitive):
  def __init__(self, pt_1, pt_2):
    self.value = [pt_1, pt_2]
    self.data = gp_Lin(gp_Ax1(pt_1.data, gp_Dir(pt_2.value[0], pt_2.value[1], pt_2.value[2])))
    Primitive.__init__(self)

class su(Primitive):
  def __init__(self, *args):
    self.value = args
    Primitive.__init__(self)

# OBJECT su_square(side)
# pre-processor replaces instruction by
class su_square(su):
  def __init__(self, side):
# end replace + auto increment
    self.test = pt(0,0,0)
    pt_1 = pt(0,0,0)
    pt_2 = pt(side,0,0)
    ln_1 = ln(pt_1, pt_2)
    ln_2 = ln(pt_2, pt(side, side, 0))
    ln_3 = ln(pt(side, side, 0), pt(0, side, 0))
    #ln_4 = ln(pt(0, side, 0), pt_1)
    ln_4 = ln(pt_1, pt(0, side, 0))

# OBJECT = su(ln_1, ln_2, ln_3, ln_4)
# pre-processor replaces instruction by
    su(self, ln_1, ln_2, ln_3, ln_4)
    Primitive.add_objects(self, inspect.getargspec(self.__init__)[0], locals())
# end insert


