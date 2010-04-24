### PYCADO LIBRARY

import inspect

pycado_dict = dict()

class Primitive:
    "store file metadata"              
    def memorise_object(self):   
      """ Add this object in global dict pycado_dict
      The key is found by inspecting stack trace
      Returns object without any change"""
      global pycado_dict
      name = None 
      for stack in inspect.stack():
        parent_var = stack[4][0].split("=")
        if len(parent_var)>1:
          if name == None:
            name = parent_var[0].strip();
          else:
            name = parent_var[0].strip() + "." + name
      pycado_dict[name] = self.value
      
    
    def add_objects(self, function_args, vars):
      for k, v in vars.items():
        if k not in function_args and has_pycado_prefix(k):
          setattr(self, k, v)
      
      
      
def has_pycado_prefix(var):
  l_prefix = ["pt_", "ln_", "ci_", "el_", "sp_", "su_", "so_"]
  for pref in l_prefix:
    if var.startswith(pref):
      return True
  return False
  
  
class pt(Primitive):
  def __init__(self, x, y, z):
    self.value = [x, y, z]
    Primitive.memorise_object(self)

class ln(Primitive):
  def __init__(self, pt_1, pt_2):
    self.value = [pt_1, pt_2]
    Primitive.memorise_object(self)

class su(Primitive):
  def __init__(self, *args):
    self.value = args
    Primitive.memorise_object(self)

### END PYCADO LIBRARY


### BEGIN USER PROGRAM

# OBJECT su_square(side)
# pre-processor replaces instruction by
class su_square(su):
  def __init__(self, side):
# end replace + auto increment
    test = pt(0,0,0)
    pt_1 = pt(0,0,0)
    pt_2 = pt(side,0,0)
    ln_1 = ln(pt_1, pt_2)
    ln_2 = ln(pt_2, pt(side, side, 0))
    ln_3 = ln(pt(side, side, 0), pt(0, side, 0))
    ln_4 = ln(pt(0, side, 0), pt_1)
  
# OBJECT = su(ln_1, ln_2, ln_3, ln_4)
# pre-processor replaces instruction by
    su(self, ln_1, ln_2, ln_3, ln_4)
    Primitive.add_objects(self, inspect.getargspec(self.__init__)[0], locals())
# end insert    
su_square_1 = su_square(10)

print su_square_1.pt_1.value
print su_square_1.ln_4.value
print su_square_1.test

#for k, v in pycado_dict.items():
#  print k, " = ", v
