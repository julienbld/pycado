#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name = 'pycado',
      version = '0.00001',
      description = '3D CAD language and editor based on pythonocc',
      author = 'Julien Blanchard',
      author_email = 'julienbld@yahoo.fr',
      maintainer = 'Charles Clément',
      url = 'http://github.com/julienbld/pycado',
      packages = ['pycado'],
      scripts = ['pycado/pycado'],
      package_dir = {'pycado': 'pycado'},
      package_data = {'pycado': ['data/config-en.yaml', 'data/images/*.png', 'examples/*.txt']},
     )
