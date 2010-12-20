=============================================
PROJECT
Pycado alpha version

=============================================
DESCRIPTION
3D CAD scripting language based on pythonocc
+ graphical interactive editor 
	
=============================================
AUTHORS
Julien Blanchard - julienbld@yahoo.fr
Charles Clément - charles.clement@gmail.com

=============================================
HOMEPAGE
https://github.com/julienbld/pycado



1 - PRESENTATION
================

Pycado is an object oriented scripting language for 3D CAD. It's based upon the pythonocc library and it's written in Python. The language itself is a python subset.
Pycado is also an IDE for the scripting language. This IDE contains three main parts:
- a text editor, where scripts are written
- a graphical window where 3D components are printed
- a message board

The object part of the language is really important because it allows to instanciate object and build new objects based on shared components. 
"Object" must be understood as "mechanical part" rather than traditional computer language meaning.  
Each object owns a coordinate system and members attributes. Instanciation are achieved by choosing a coordinate system and attributes values. 

The language is a python subset, so the scripts can be parsed by the python parser and cad objects are added in memory. This strategy was choosen to update a part of an assembly or a component without compiling all the script and called objects, only impacted parts are updated. To achieve this, Pycado is using a dependencies tree. 
  


2 - INSTALLATION
================
Pycado is based on pythonocc, so, first step is to install pythonocc.

Charles tu avais bossé là dessus, je ne me rappelle plus trop...



3 - PROGRESS - TODO
===================
Pycado is on very early stage, kind of proof of concept.
Some example scripts were written and are working. They are quite simple but they give a good preview of our objectives.

Here are some directions to improve the application:
- complete the based API (point / line / curve ...). This API should stay really simple and should go with an integrated help in the IDE
- create interaction between graphical window and text editor.
e.g. copy name of the selected component to paste it in the editor
- write a complex example of 3D CAD object to figure the limits of our approach.