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


class pycado_obj():
  
  def __init__(self, cs, *args):
    self._display = True
    
    if isinstance(args[0], coord_sys):
      self.cs0 = args[0]
      args = args[1:]
    else:
      self.cs0 = cs       
    
    self.args = args
    self.name = "anonym"
    self.parent = None
    
    g_objs.append(self)
  
  def update_name(self):
    if self.parent != None:
      self.name = self.parent.name + "." + self.name
      
  def display(self):
    if self._display == True and self.name.find("anonym")==-1:
      display.display.DisplayShape(self.topology)
    
  def local_var_to_members(self, local_vars):
    for k, v in local_vars.items():
      if k != "self":
        setattr(self, k, v)
        if isinstance(v, pycado_obj):
          v.name = k
          v.parent = self 
  

  def show(self):
    self._display = True

  def hide(self):
    self._display = False
  
  def build(self):
    self.update_name()
      
class point(pycado_obj):
  def build(self):
    self.update_name()
    
    args = self.args
    
    if isinstance(args[0], point):
      pt_or = args[0]
      args = args[1:]
    else:
      pt_or = None
            
    self.data = gp_Pnt(args[0], args[1], args[2])
    
    if self.cs0!=None:
      self.data = self.data.Translated(gp().Origin(), self.cs0.p0.data)
      
    if pt_or != None:
      self.data = self.data.Translated(self.cs0.p0.data, pt_or.data)
      
    self.topology = BRepBuilderAPI_MakeVertex(self.data).Vertex()


class line(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    p1 = args[0]
    p2 = args[1]
    #self.data = gp_Lin(gp_Ax1(pt_1.data, gp_Dir(pt_2.value[0], pt_2.value[1], pt_2.value[2])))
    self.topology = BRepBuilderAPI_MakeEdge(p1.data, p2.data).Edge()

class vector(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    self._display = False
    if args[0]=="mul":
      self.data = args[1].data
      self.data = self.data.Multiplied(args[2])
      #todo: corriger
      self.p1 = point(self.cs0, 0, 0, 0)
      self.p1.build()
      self.p2 = point(self.cs0, 0, 0, 1)
      self.p2.build()  
    else:
      self.p1 = args[0]
      self.p2 = args[1]
      self.data = gp_Vec(self.p1.data, self.p2.data)

    self.topology = BRepBuilderAPI_MakeEdge(self.p1.data, self.p2.data).Edge()

  def __mul__(self, other):
    if isinstance(other, numbers.Number):
      #todo: corriger
      #ve_new = vector(None, self.value[0], self.value[1])
      #ve_new.data = ve_new.data.Multiplied(other)
      ve_new = vector(self.cs0, "mul", self, other)
      return ve_new

  def __rmul__(self, other):
    return self.__mul__(other)

class coord_sys(pycado_obj):
  def __init__(self, cs, *args): 
    self._display = False
    self.p0 = args[0]
    self.vx = args[1]
    self.vy = args[2]
    self.vz = args[3]
  

class surface(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
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


class solid(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    if isinstance(args[0], str):
      if args[0] == "extrusion":
        self.topology = BRepPrimAPI_MakePrism(args[1].topology, args[2].data).Shape()

class group(pycado_obj): 
  def display(self):
    a=2
       
  def hide(self):
    for k, v in inspect.getmembers(self):
      if isinstance(v, pycado_obj):
        v._display = False

  def show(self):
    for k, v in inspect.getmembers(self):
      if isinstance(v, pycado_obj):
        v._display = True



# GLOBAL VARS
# Initial coordinate system
g_objs = []          

CUT = "cut"
EXTRUSION = "extrusion"
