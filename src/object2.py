from OCC.gp import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.BRepAlgo import *
from OCC.BRepFeat import *
from OCC.TopExp import *
from OCC.TopAbs import *

from OCC.TopoDS import *

import display
import inspect
import numbers

class Object2():
  def display(self):
    display.display.DisplayShape(self.topology)  
  
class pt(Object2):  
  def __init__(self, cs, *args):
    if isinstance(args[0], pt):
      va_x = args[1]
      va_y = args[2]
      va_z = args[3]
      self.value = [va_x, va_y, va_z]
      tmp = gp_Pnt(va_x, va_y, va_z)
      self.data = tmp.Translated(gp().Origin(), args[0].data)
    else:
      va_x = args[0]
      va_y = args[1]
      va_z = args[2]
      self.value = [va_x, va_y, va_z]
      self.data = gp_Pnt(va_x, va_y, va_z)
    
    if cs!=None:
      if cs.pt_0.value != [0, 0, 0]:
        self.data = self.data.Translated(gp().Origin(), cs.pt_0.data) 
      
    self.topology = BRepBuilderAPI_MakeVertex(self.data).Vertex()
  
    
class ve():
  def __init__(self, cs, *args):
    if args[0] == "x":
      self.value = [pt(cs, 0, 0, 0), pt(cs, 1, 0, 0)]
    elif args[0] == "y":
      self.value = [pt(cs, 0, 0, 0), pt(cs, 0, 1, 0)]
    elif args[0] == "z":
      self.value = [pt(cs, 0, 0, 0), pt(cs, 0, 0, 1)]
    else:
      self.value = [args[0], args[1]]

    self.data = gp_Vec(self.value[0].data, self.value[1].data)
    self.topology = BRepBuilderAPI_MakeEdge(self.value[0].data, self.value[1].data).Edge()
  
  def __mul__(self, other):
    if isinstance(other, numbers.Number):
      ve_new = ve(None, self.value[0], self.value[1])
      ve_new.data = ve_new.data.Multiplied(other) 
      return ve_new 

  def __rmul__(self, other):
    return self.__mul__(other)     
    
    
class cs():
  def __init__(self, cs, *args):
    self.pt_0 = args[0]
    self.ve_x = args[1]
    self.ve_y = args[2]
    self.ve_z = args[3]
  
class ob():
  def __init__(self, cs, *args):
    a = 2      
       
class ln(Object2):
  def __init__(self, cs, pt_1, pt_2):
    self.value = [pt_1, pt_2]
    #self.data = gp_Lin(gp_Ax1(pt_1.data, gp_Dir(pt_2.value[0], pt_2.value[1], pt_2.value[2])))
    self.topology = BRepBuilderAPI_MakeEdge(pt_1.data, pt_2.data).Edge()
  

class su(Object2):
  def __init__(self, cs, *args):
    if isinstance(args[0], str):
      if args[0] == "cut":
        self.data = BRepAlgo_Cut(args[1].topology, args[2].topology)
        ex = TopExp_Explorer()
        ex.Init(self.data.Shape(), TopAbs_FACE)
        self.topology = TopoDS().Face(ex.Current())
    else:
      self.value = args
      self.data = BRepBuilderAPI_MakeWire()
      for i in args:
          self.data.Add(i.topology)
      self.topology = BRepBuilderAPI_MakeFace(self.data.Wire()).Face()


class so(Object2):
  def __init__(self, cs, *args):
    if isinstance(args[0], str):
      if args[0] == "extrusion": 
        self.topology = BRepPrimAPI_MakePrism(args[1].topology, args[2].data).Shape() 
