from OCC.Display.SimpleGui import *

set_backend("qt")

display, start_display, add_menu, add_function_to_menu = init_display()

def exit():
	sys.exit()

add_menu("test")
add_function_to_menu("test", exit)


display.View_Iso()
display.FitAll()


#start_display()
