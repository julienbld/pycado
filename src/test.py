from object import *
from primitive import pycado_dict
from function import *

### BEGIN USER PROGRAM


su_square_1 = su_square(10)

#su_square_1.surface.display()

print su_square_1.surface.face
solid = extrude(su_square_1.surface.face.Face(), 0, 0, 2)

display.display.DisplayShape(solid.Shape())

#display.display.DisplayShape(su_square_1.face.Face())

#vertex_1 = BRepBuilderAPI_MakeVertex(gp_Pnt(-2,1,3))
#display.display.DisplayShape(vertex_1.Vertex())

#box = BRepPrimAPI_MakeBox(10,10,10).Shape()
#display.display.DisplayShape(box)

for k, v in pycado_dict.items():
  print k, " = ", v


display.start_display()
