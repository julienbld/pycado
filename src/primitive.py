### PYCADO LIBRARY

import inspect

pycado_dict = dict()

class Primitive:
    "store file metadata"
    def __init__(self):
      self.memorise_object()

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

### END PYCADO LIBRARY


