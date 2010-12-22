=============================================
PROJECT
Pycado alpha version

=============================================
DESCRIPTION
Pycado is an object oriented 3D CAD scripting language based on pythonocc with a graphical interactive editor

=============================================
AUTHORS
Julien Blanchard - julienbld --- yahoo --- fr
Charles Clément - caratorn --- gmail --- com

=============================================
HOMEPAGE
https://github.com/julienbld/pycado



1 - PRESENTATION
================

Pycado is an object oriented scripting language for 3D CAD. It's based upon the
pythonocc library and written in Python. The language itself is a python subset.
Pycado is also an IDE for the scripting language. This IDE contains three main
parts:

- a text editor, to edit scripts
- a graphical window where 3D components are drawn
- a log viewer

The object part of the language is really important because it allows to
instantiate objects and build new objects based on shared components. "Object"
must be understood as "mechanical part" rather than traditional computer
language meaning.

Each object owns a coordinate system and attribute members. Instantiation are
achieved by choosing a coordinate system and attribute values for a new object
instance.

The language is a python subset, so the scripts can be parsed by the python
parser and cad objects are added in memory. This strategy was chosen to update
a part of an assembly or a component without compiling all the scripts and called
objects, only impacted parts are updated. To achieve this, Pycado is using a
dependency tree.



2 - INSTALLATION
================
Pycado is based on pythonocc, so the first step is to install pythonocc, which
depends on the OpenCASCADE library (http://www.opencascade.org/) and swig
(http://www.swig.org/).



3 - PROGRESS - TODO
===================
Pycado is on very early stage, kind of proof of concept. Some example scripts
were written. They are quite simple but give a good preview of our objectives.

Here are some directions to improve the application:
- complete the base API (point / line / curve ...). This API should stay simple
  and should be associated with an integrated help in the IDE
- create interaction between the graphical window and text editor, e.g. copy
  the name of the selected component to paste it in the editor
- write a complex example of 3D CAD object to figure the limits of our approach
