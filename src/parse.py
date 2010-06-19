import ast
import sys
import traceback

from pycado_obj import *

# used only for converting ast to source_code
# only debug purpose
from ast import *
import codegen

import glob
from math import *

# PRE COMPILER
# change "group" to object implementing group
#  + add main function for lonely instructions
#  + add some instructions
 
class pre_compiler(ast.NodeTransformer):
  def __init__(self):
    self.PRIMITIVES = ["point", "line", "coord_sys", "vector", "surface", "solid", "nurb"]
    
    l_str = "pycado_obj.__init__()"
    l_str += "\np0 = cs0.p0\nvx = cs0.vx\nvy = cs0.vy\nvz = cs0.vz"
    self.str_init_group = l_str
    self.parse_end_group = ast.parse("self.local_var_to_members(locals())")

  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)
  
  def visit_Module(self, node):
    
    new_body = []

    # create main function
    main = ast.FunctionDef()
    main.name = "pycado_main" 
    main.args = arguments([], None, None, [])
    main.decorator_list=[] 
    main.body = []
    
    for n in node.body:
      self.generic_visit(n)
      if isinstance(n, ast.FunctionDef) \
          and n.name.startswith("pycado_object_"):
        
        # transform group function in class
        n.name = n.name[14:]
        n.args.args = [ast.Name("self", ast.Load())] + n.args.args
        l_init = ast.parse(self.str_init_group) 
        l_init.body[0].value.args  = n.args.args
        for name in l_init.body[0].value.args:
          name.ctx = ast.Load()
          
        n.body = l_init.body + n.body + self.parse_end_group.body       
        class_def = ast.ClassDef()
        class_def.name = n.name
        class_def.bases = [ast.Name("group", ast.Load())]
        n.name="__init__"
        class_def.body = [n]
        class_def.decorator_list=[]
        new_body.append(class_def)
        
      elif not isinstance(n, ast.FunctionDef) \
            and not isinstance(n, ast.ClassDef):
        # add lonely node to main
        main.body.append(n)
        #new_body.append(n)
        
      else :
        new_body.append(n)
    
    # add initialisations to main    
    l_init = "p0 = point(None, 0, 0, 0)"
    l_init += "\n__p1 = point(None, 1, 0, 0)"
    l_init += "\n__p2 = point(None, 0, 1, 0)"
    l_init += "\n__p3 = point(None, 0, 0, 1)"
  
    l_init  += "\nvx = vector(None, p0, __p1)"
    l_init  += "\nvy = vector(None, p0, __p2)"
    l_init  += "\nvz = vector(None, p0, __p3)"
    l_init  += "\ncs0 = coord_sys(None, p0, vx, vy, vz)"
        
    main.body = ast.parse(l_init).body + main.body 
    #new_body = ast.parse(l_init).body + new_body 
    # add main locals to g_obj 
    l_end = "for k, v in locals().items():"
    l_end += "\n  if isinstance(v, pycado_obj):"
    l_end += "\n    v.name = k"
    l_end += "\n    v.parent = None"

    main.body = main.body + ast.parse(l_end).body
    #new_body = new_body + ast.parse(l_end).body
    new_body.append(main)  
    
    node.body = new_body   

  def visit_Call(self, node):    
    if isinstance(node.func, ast.Name):
      if node.func.id in self.PRIMITIVES:
        # add first arg cs0 in PRIMITIVES call
        node.args = [ast.Name("cs0", ast.Load())] + node.args    


# add lineno and col_offset to nodes
#TODO: apply function only on created nodes
class fix_tree(ast.NodeTransformer):
  def generic_visit(self, node):
    if not hasattr(node, 'lineno'):
      node.lineno = 0
    else:
      lineno = node.lineno
    if not hasattr(node, 'col_offset'):
      node.col_offset = 0
    else:
      col_offset = node.col_offset  
    ast.NodeVisitor.generic_visit(self, node)
    
    
def display_file(a_filename):
  try:               
    # READ FILE                                  
    l_f = file(a_filename, 'r')
    
    # TRANSFORM group x -> def pycado_object_x
    l_src = ""  
    l = l_f.readline()
    while l:
      if l.strip().startswith("group "):
        #todo: to improve. Here fails when several spaces between group and group name
        l = l.replace("group ", "def pycado_object_")
      l_src += l
      l = l_f.readline()
    
    l_f.close()
    
    # PERFORM PREPROCESSING:
    # - transform groups in classes with some initialisation
    # - add cs0 in primitives calling
    # - make a function grouping lonely instructions
        
    print l_src
    
    l_ast = ast.parse(l_src, a_filename)
    
    l_pre_compiler = pre_compiler()
    l_pre_compiler.visit(l_ast)
    #print dump(l_ast)
    
    fixer = fix_tree()
    fixer.visit(l_ast)
    
    # EXECUTE!
    print("# CODE GENERATED")
    print(codegen.to_source(l_ast))
    #print dump(l_ast)
    
    exec compile(l_ast, a_filename, 'exec') in globals()
    
  
    pycado_main()
    print("\n# PYCADO_OBJ LIST")
    
    for o in glob.get_objs():
      o.build()
      o.display()
      print o.name, o    

  except:
    print sys.exc_info()
    glob.log(traceback.format_exc())
  
