import yaml
import sys

# global
g_expr_sep = [" ", "(", ")", "+", "-", '*', "/", ","];
g_prefixes = ["va_", "pt_", "ln_", "ve_", "re_", "ci_", "el_", \
                "sp_", "su_", "so_", "ob_", "fn_", "pa_"]
                
# utils function
def has_pycado_prefix(var):
  if isinstance(var, str):  
    for pref in g_prefixes:
      if var.startswith(pref):
        return True
  return False

# dependancies
def get_deps(a_instr):
  l_deps = set()
  if isinstance(a_instr, str):
    l_deps.update(get_pyc_objs(a_instr))
      
  if isinstance(a_instr, list):
    for elt in a_instr:
      l_deps.update(get_deps(elt))       
          
  return l_deps


def get_pyc_objs(a_str):
  l_current_str = ""
  l_pyc_objs = []
  a_str = a_str + " "
  for c in a_str:
    if c in g_expr_sep:
      if l_current_str != "":
        if has_pycado_prefix(l_current_str):
          l_pyc_objs.append(l_current_str)
        l_current_str = ""
    else:
      l_current_str += c
      
  return l_pyc_objs


# instruction for objects instances
def get_instantiated_instruction(a_instr, a_inst_name):
  if isinstance(a_instr, str):
    l_new_instr = ""
    l_current_str = ""
    l_str = a_instr + " "
    for c in l_str:
      if c in g_expr_sep:
        if l_current_str != "":
          if a_inst_name!=None and has_pycado_prefix(l_current_str):
            l_current_str = a_inst_name + "." + l_current_str
          
          l_new_instr += l_current_str
              
          l_current_str = ""
  
        if c != " ":
          l_new_instr += c
      else:
        l_current_str += c
    
    return l_new_instr
      
  elif isinstance(a_instr, list):
    if not isinstance(a_instr[0], str) or not a_instr[0].startswith("re_"):
      a_instr.insert(0, "re_0")

    l_instrs = []
    for elt in a_instr:
      l_instrs.append(get_instantiated_instruction(elt, a_inst_name))       

    return l_instrs
  
  else:
    return a_instr
  

# add call to global dict
def get_call_to_dict(a_instr):
  if isinstance(a_instr, str):
    l_new_instr = ""
    l_current_str = ""
    l_str = a_instr + " "
    for c in l_str:
      if c in g_expr_sep:
        if l_current_str != "":
          if has_pycado_prefix(l_current_str):
            l_current_str = "g_i['" + l_current_str + "']"
          else:
            try:
              float(l_current_str)
            except ValueError:
              l_current_str = "'" + l_current_str + "'"
              
          l_new_instr += l_current_str      
          l_current_str = ""
        l_new_instr += c
  
      else:
        l_current_str += c
    return l_new_instr
        
  elif isinstance(a_instr, list):
    l_instrs = []
    for elt in a_instr:
      l_instrs.append(get_call_to_dict(elt))       

    return l_instrs
  else:
    return a_instr
  



class DefObj:
  def __init__(self, a_name, a_map):
    self.m_name = a_name
    self.m_instrs = a_map
  
  def get_instantiated_instrs(self, a_inst_name):
    l_instrs = {} 
    for k, v in self.m_instrs.items():
      if k == "params":
        # add parameters initialisations instructions
        for i in range(len(v)):
          l_instrs[a_inst_name + "." + v[i]] = g_instrs[a_inst_name][i]
      elif k == "return":
        # object instance = alias on returned object
        l_instrs[a_inst_name] = get_instantiated_instruction(v, a_inst_name)  
      else:
        l_instrs[a_inst_name + "." + k] = get_instantiated_instruction(v, a_inst_name)
    
    return l_instrs
      
  

class Instance:
  def __init__(self, a_key_instr, a_deps, a_forced_instr=""):
    self.m_deps = a_deps
    
    if a_forced_instr=="" :
      self.m_call = self.instr_to_call(a_key_instr, g_instrs[a_key_instr])
    else: 
      self.m_call = self.instr_to_call(a_key_instr, a_forced_instr) 
      
    self.draw()
    self.is_resolved = True
    
  def instr_to_call(self, a_key_instr, a_instr):
    l_instr = get_call_to_dict(a_instr)
    if isinstance(l_instr, list):
      l_instr_str = a_key_instr.rpartition(".")[2][:2] + "("
       
      for expr in l_instr:
        l_instr_str += str(expr) + ", "
      
      if l_instr_str.endswith(", "):
        l_instr_str = l_instr_str[0:len(l_instr_str)-2] + ")"
        
    else:
      l_instr_str = l_instr      
    
    return a_key_instr, l_instr_str
    
    
  def draw(self):           
    print "g_i['" + self.m_call[0] + "'] = " + str(self.m_call[1])
      
  

def instanciate(a_inst_name):
  if a_inst_name not in g_i or not g_i[a_inst_name].is_resolved:
    l_instr = g_instrs[a_inst_name]
    l_deps = get_deps(l_instr)
    if len(l_deps) != 0:
      for l_elt in l_deps:
        instanciate(l_elt)
    
    g_i[a_inst_name] = Instance(a_inst_name, l_deps)      
              
    

def load_prog(a_map, a_parent):
  # separate instructions and definitions of object
  for k, v in a_map.items(): 
    if k.strip().startswith("def"):
      l_obj_name = k.strip()[4:].strip() 
      g_def_objs[l_obj_name] = DefObj(l_obj_name, v)
    else: 
      g_instrs[k] = get_instantiated_instruction(v, None) #v
      
  
  # add all instructions corresponding to objects instanciations
  l_new_instrs = {}
  for k, v in g_instrs.items():
    if k.startswith("ob_"):
      obj_name = k[0: 6 + k[6:].find("_")]
      l_new_instrs.update(g_def_objs[obj_name].get_instantiated_instrs(k))
      g_instrs.update(l_new_instrs)
      
  # instanciate each instruction
  for k, v in g_instrs.items():
    instanciate(k)
    #print k, " = ", v

         

# MAIN
stream = file(sys.argv[1], 'r')
src_code = yaml.load(stream)

g_def_objs = {}
g_instrs = {}
g_i = {}

# Initial referentiel
g_i["pt_0"] = Instance("pt_0", [], "default_pycado_value")
g_i["ve_x"] = Instance("ve_x", [], "default_pycado_value")
g_i["ve_y"] = Instance("ve_y", [], "default_pycado_value")
g_i["ve_z"] = Instance("ve_z", [], "default_pycado_value")
g_i["re_0"] = Instance("re_0", [], "default_pycado_value")

load_prog(src_code, "")



                  
    
  
    
     