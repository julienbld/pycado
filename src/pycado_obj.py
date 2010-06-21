from OCC.gp import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.BRepAlgo import *
from OCC.BRepFeat import *
from OCC.TopExp import *
from OCC.TopAbs import *

from OCC.TopoDS import *

import glob
import inspect
import numbers


class pycado_obj():
  
  def __init__(self, cs, *args):
    self._display = True
    if len(args)>0 and isinstance(args[0], coord_sys):
      self.cs0 = args[0]
      args = args[1:]
    else:
      self.cs0 = cs       
    
    self.args = args
    self.name = "anonym"
    self.parent = None
    self.data = None
    
    if len(args)>0 and args[0] == "intern":
      self.create(*args[1:])
    else: 
      glob.add_obj(self)
  
  def update_name(self):
    if self.parent != None:
      self.name = self.parent.name + "." + self.name
      
  def display(self):
    if self._display == True and self.name.find("anonym")==-1:
      glob.display(self.topology)
      #canva.DisplayShape()
    
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
  def create(self, gp_pnt):
    self.data = gp_pnt
    self.topology = BRepBuilderAPI_MakeVertex(self.data).Vertex()
    
  def build(self):
    self.update_name()
    args = self.args
    
    if isinstance(args[0], point):
      pt_or = args[0]
      args = args[1:]
    else:
      pt_or = None
            
    self.data = gp_Pnt(args[0], args[1], args[2])
    
    if pt_or != None:
      #TODO: Write real treatment (to check)
      self.data.Translate(self.cs0.p0.data, pt_or.data)
      
    if self.cs0!=None:
      if self.cs0.trsf != None:
        self.data.Transform(self.cs0.trsf)
                    
            
    self.topology = BRepBuilderAPI_MakeVertex(self.data).Vertex()

  def update(self, gp_pnt):
    self.data = gp_pnt
    self.topology = BRepBuilderAPI_MakeVertex(self.data).Vertex()        
  
  def __str__(self):
    ret = self.name 
    if self.data != None:
      ret += "=(" + str(self.data.X()) + ", " 
      ret += str(self.data.Y()) + ", "
      ret += str(self.data.Z()) + ")"
    return ret
    
class line(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    p1 = args[0]
    p2 = args[1]
    #self.data = gp_Lin(gp_Ax1(pt_1.data, gp_Dir(pt_2.value[0], pt_2.value[1], pt_2.value[2])))
    self.topology = BRepBuilderAPI_MakeEdge(p1.data, p2.data).Edge()

class circle(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    print args
    p = args[0]
    v_norm = args[1]
    r = args[2]
    self.data = gp_Circ(gp_Ax2(p.data, gp_Dir(v_norm.data)), r)
    self.topology = BRepBuilderAPI_MakeEdge(self.data).Edge()
    
    
class vector(pycado_obj):
  def create(self, gp_pnt, gp_vec):
    #todo: check: maybe a bug!
    self.data = gp_vec
    self.p1 = point(None, "intern", gp_pnt)
    self.p2 = point(None, "intern", gp_pnt.Translated(gp_vec))
    self.topology = BRepBuilderAPI_MakeEdge(self.p1.data, self.p2.data).Edge()
    # = point(self.cs0, 0, 0, 0)
    #self.p1.build()
    #self.p2 = point(self.cs0, 0, 0, 1)
    #self.p2.build() 

  def build(self): 
    self.update_name()
    args = self.args
    self._display = False
    if args[0]=="mul":
      self.data = args[1].data.Multiplied(args[2])
      self.p1 = point(None, "intern", args[1].p1.data)
      self.p2 = point(None, "intern", self.p1.data.Translated(self.data)) 
      
    elif args[0]=="add":
      self.data = args[1].data.Added(args[2].data)
      self.p1 = point(None, "intern", args[1].p1.data)
      self.p2 = point(None, "intern", self.p1.data.Translated(self.data)) 
    else:
      self.p1 = args[0]
      self.p2 = args[1]
      self.data = gp_Vec(self.p1.data, self.p2.data)

    self.topology = BRepBuilderAPI_MakeEdge(self.p1.data, self.p2.data).Edge() 

  def update(self, gp_pnt, gp_vec):
    #todo: check: maybe a bug!
    self.data = gp_vec
    self.p1.update(gp_pnt)
    self.p2.update(gp_pnt.Translated(gp_vec))
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

  def __add__(self, other):
    if isinstance(other, vector):
      ve_new = vector(self.cs0, "add", self, other)
      return ve_new

  def __radd__(self, other):
    return self.__add__(other)

  def __str__(self):
    ret = self.name + "=[" + str(self.p1) + " - " + str(self.p2) + "]"
    return ret


class coord_sys(pycado_obj):
  """
  def __init__(self, cs, *args):
    pycado_obj.__init__(self, cs, *args)
    #self.args = self.args[0]
    self.trsf = None
    self.data = gp_Ax3(gp().XOY())
    self.p0 = point(None, 0, 0, 0)
    self.p0.build()
    p1 = point(None, 1, 0, 0)
    p1.build()
    p2 = point(None, 0, 1, 0)
    p2.build()
    p3 = point(None, 0, 0, 1)
    p3.build()
    self.vx = vector(None, self.p0, p1)
    self.vx.build()
    self.vy = vector(None, self.p0, p2)
    self.vy.build()
    self.vz = vector(None, self.p0, p3)
    self.vz.build()
    #self.update(self.data)
  """ 
   
  #def create(self, gp_ax3):
  def __init__(self, cs, *args):
    pycado_obj.__init__(self, cs, *args)
    self.data = gp_Ax3(gp().XOY())  
    self.p0 = point(None, "intern", self.data.Location())
    self.vx = vector(None, "intern", self.p0.data, gp_Vec(self.data.XDirection()))
    self.vy = vector(None, "intern", self.p0.data, gp_Vec(self.data.YDirection()))
    self.vz = vector(None, "intern", self.p0.data, gp_Vec(self.data.Direction()))
    self.trsf = None
    
  def build(self):
    self.update_name()
    args = self.args

    if self.cs0 != None:
      self.data = gp_Ax3(self.cs0.data.Ax2())
    
    self._display = False
    self.trsf = gp_Trsf()
     
    # TODO: REMOVE?   
    if isinstance(args[0], point):
      self.p0 = args[0]
      self.vx = args[1]
      self.vy = args[2]
      self.vz = args[3] 
    elif args[0] == "translate":
      v_trans = args[1].data
      self.data.Translate(v_trans)
      self.update(self.data)
      
    elif args[0] == "rotate":
      v_rot = args[1]
      angle = args[2]
      self.data.Rotate(gp_Ax1(v_rot.p1.data, gp_Dir(v_rot.data)), angle)
      self.update(self.data)
    
  def update(self, gp_ax3):
    self.data = gp_ax3
    self.p0.update(gp_ax3.Location())
    self.vx.update(self.p0.data, gp_Vec(gp_ax3.XDirection()))
    self.vy.update(self.p0.data, gp_Vec(gp_ax3.YDirection()))
    self.vz.update(self.p0.data, gp_Vec(gp_ax3.Direction()))    
    self.trsf.SetTransformation(self.data, gp_Ax3(gp().XOY()))
    
    
  def __str__(self):
    ret = self.name + "{" 
    ret += str(self.p0) + ", " + str(self.vx) + ", " + str(self.vy)
    ret += ", " + str(self.vz) + "}"
    return ret
                    
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

class nurb(pycado_obj):
  def build(self):
    self.update_name()
    args = self.args
    self.topology = BRepBuilderAPI_NurbsConvert(args[0].topology).Shape()

class group(pycado_obj): 
  def display(self):
    pass
       
  def hide(self):
    for k, v in inspect.getmembers(self):
      if isinstance(v, pycado_obj):
        v._display = False

  def show(self):
    for k, v in inspect.getmembers(self):
      if isinstance(v, pycado_obj):
        v._display = True



# GLOBAL VARS  

CUT = "cut"
EXTRUSION = "extrusion"
TRANSLATE = "translate"
ROTATE = "rotate"