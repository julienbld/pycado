# used to read/write cross-module variables 

curr_tab = 0
objs = []
consoles = []
displays = []
file_names = []

def log(msg):
  print msg
  consoles[curr_tab].append(str(msg))
  
def display(topo):
  displays[curr_tab].DisplayShape(topo)

def add_obj(data):
  objs[curr_tab].append(data)

def remove_all_objs():
  objs[curr_tab][:] = []

def get_objs():
  return objs[curr_tab]

def set_file_name(name):
  file_names[curr_tab] = name
  
def get_file_name():
  return file_names[curr_tab]     