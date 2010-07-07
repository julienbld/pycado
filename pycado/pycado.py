#!/usr/bin/python

# ZetCode PyQt4 tutorial
#
# This example shows
# how to use QSplitter widget
# 
# author: Jan Bodnar
# website: zetcode.com
# last edited: February 2010


from PyQt4 import QtGui, QtCore
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython
from qt_display import qtViewer3d
import yaml
import cProfile
import OCC
#from OCC import Materials
import nspace
import os

from parse import *
  
  
class PycadoGui(QtGui.QMainWindow):
          
  def __init__(self):
    QtGui.QMainWindow.__init__(self) 
    
    # MENU BAR
    self.initMenuBar()      
    
    # EDITOR        
    self.editor = self.initEditor()
    
    # CANVA
    self.canva = qtViewer3d(self) 
    
    # CONSOLE
    self.console = QtGui.QTextBrowser(self)
    #bottom.setFrameShape(QtGui.QFrame.StyledPanel)

    # LAYOUT
    center = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout(center)
    hbox.setContentsMargins(0, 0, 0, 0)

    splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
    splitter1.addWidget(self.editor)
    splitter1.addWidget(self.canva)
    splitter1.setStretchFactor (0, 1)
    splitter1.setStretchFactor (1, 4)
    
    splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
    splitter2.addWidget(splitter1)
    splitter2.addWidget(self.console)
    splitter2.setStretchFactor (0, 6)
    splitter2.setStretchFactor (1, 1)

    hbox.addWidget(splitter2)

    
    self.setCentralWidget(center)
    
    # TITLE
    self.setWindowTitle(nspace.config['title'])
    self.setWindowIcon(QtGui.QIcon(nspace.config['icon'])) 
   
    # SIZE
    screen = QtGui.QDesktopWidget().screenGeometry()
    self.setGeometry(0, 20, screen.width()-50, screen.height()-150)     

    # INIT DISPLAY   
    #self.canva.InitDriver()
    #self.canva._display.SetBackgroundImage(get_abs_filename())
    #self.canva._display.View_Iso()
    ##self.canva._display.FitAll()
    

  def initMenuBar(self):
    menubar = self.menuBar()
    
    # F I L E
    menu_desc = nspace.config['menus']['file']
    menu = menubar.addMenu(menu_desc['name'])
    
    # New File
    action = self.action_menu(menu_desc['new-file'])
    self.connect(action, QtCore.SIGNAL('triggered()'), self.open_file)
    #menu.addAction(action)
    
    # Open file
    action = self.action_menu(menu_desc['open-file'])
    self.connect(action, QtCore.SIGNAL('triggered()'), self.open_file)
    menu.addAction(action)
    
    # Save
    action = self.action_menu(menu_desc['save'])
    self.connect(action, QtCore.SIGNAL('triggered()'), self.save)
    menu.addAction(action)
        
    # Save as
    action = self.action_menu(menu_desc['save-as'])
    self.connect(action, QtCore.SIGNAL('triggered()'), self.save)
    #menu.addAction(action)
        
    # Quit
    action = self.action_menu(menu_desc['quit'])
    self.connect(action, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
    menu.addAction(action)

  
  def action_menu(self, line_desc):
    action = QtGui.QAction(QtGui.QIcon(line_desc['icon']), line_desc['name'], self)
    action.setShortcut(line_desc['shortcut'])
    action.setStatusTip(line_desc['tip'])
    return action
  
  
  def initEditor(self):
    editor = QsciScintilla()

    ## define the font to use
    font = QtGui.QFont()
    #font.setFamily("Consolas")
    font.setFixedPitch(True)
    font.setPointSize(9)
    # the font metrics here will help
    # building the margin width later
    fm = QtGui.QFontMetrics(font)

    ## set the default font of the editor
    ## and take the same font for line numbers
    editor.setFont(font)
    editor.setMarginsFont(font)

    ## Line numbers
    # conventionnaly, margin 0 is for line numbers
    editor.setMarginWidth(0, fm.width( "0000"))
    editor.setMarginLineNumbers(0, True)

    ## Edge Mode shows a red vetical bar at 80 chars
    editor.setEdgeMode(QsciScintilla.EdgeLine)
    editor.setEdgeColumn(80)
    editor.setEdgeColor(QtGui.QColor("#FF0000"))

    ## Folding visual : we will use boxes
    editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

    ## Braces matching
    editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

    ## Editing line color
    editor.setCaretLineVisible(True)
    #editor.setCaretLineBackgroundColor(QtGui.QColor("#F5F5DC"))

    ## Margins colors
    # line numbers margin
    #editor.setMarginsBackgroundColor(QtGui.QColor("#333333"))
    #editor.setMarginsForegroundColor(QtGui.QColor("#CCCCCC"))

    # folding margin colors (foreground,background)
    #editor.setFoldMarginColors(QtGui.QColor("#99CC66"),QtGui.QColor("#333300"))

    ## Choose a lexer
    lexer = QsciLexerPython()
    lexer.setDefaultFont(font)
    editor.setLexer(lexer)

    ## Render on screen
    #editor.show()

    ## Show this file in the editor
    #editor.setText(open("examples\charriot_obj.txt").read())
    
    # Show all the methods of the editor
    #methods = sorted(QsciScintilla.__dict__.keys())
    #for m in methods :
    #    print m
    #editor.setWidth(400)
    
    editor.setEolMode(QsciScintilla.EolUnix)
    return editor
  
  def open_file(self, filename=None):
    if filename==None :
      filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
      
    fname = open(filename)
    data = fname.read()
    self.editor.setText(data) 
    
    nspace.set_file_name(str(filename)) 
    nspace.remove_all_objs()
    self.canva._display.EraseAll()
    #cProfile.run('display_file("' + str(filename) + '")')
    display_file(str(filename))
    
  def save(self):
    filename = nspace.get_file_name()
    f = file(filename, 'w')
    f.write(self.editor.text())
    f.close()
    nspace.remove_all_objs()
    self.canva._display.EraseAll()
    display_file(filename)
    
    
#TODO: CHANGE!!!
def get_abs_filename():
  import sys
  import os, os.path

  ''' Returns the absolute file name for the file default_background.bmp
  '''
  occ_package = sys.modules['OCC']
  bg_abs_filename = os.path.join(occ_package.__path__[0],'Display','default_background.bmp')
  if not os.path.isfile(bg_abs_filename):
      raise NameError('Not image background file found.')
  else:
      return bg_abs_filename

def main(argv=sys.argv):
  # CONFIG
  data_path = os.path.join(os.path.dirname(__file__),'data')
  nspace.config = yaml.load(file(os.path.join(data_path, 'config-en.yaml'), 'r'))

  # GUI
  app = QtGui.QApplication([])
  gui = PycadoGui()
  gui.showMaximized()

  # INIT DISPLAY   
  gui.canva.InitDriver()
  #gui.canva._display.SetBackgroundImage(nspace.config["background"])
  gui.canva._display.SetBackgroundImage(get_abs_filename())
  #gui.canva._display.GetViewer().GetObject().SetDefaultBackgroundColor(OCC.Quantity.Quantity_NOC_YELLOW)
  gui.canva._display.View_Iso()

    
  # GLOBAL GUI VARS
  #TODO: improve tab gestion

  nspace.displays.append(gui.canva._display)
  nspace.consoles.append(gui.console)
  nspace.objs.append([])
  nspace.file_names.append("")

  if(len(argv)>1):
    gui.open_file(argv[1])
    
  # EXEC
  app.exec_()
  


if __name__ == "__main__":
  main()
