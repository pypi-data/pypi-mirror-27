#!/usr/bin/env python
import sys
from distutils.core import setup

try:
    import PIL
except ImportError:
    sys.exit("""You need Pillow!
                install it from https://pillow.readthedocs.io/en/latest/installation.html
                or run pip install PIL.""")
                
try:
    import shapely
except ImportError:
    sys.exit("""You need Shapely!
                install it from https://pillow.readthedocs.io/en/latest/installation.html
                or run pip install shapely.""")
                
try:
    import cv2
except ImportError:
    sys.exit("""You need opencv!
                install it from https://pillow.readthedocs.io/en/latest/installation.html
                or run pip install opencv-python.""")
                
setup(name='cloudcoverage',
      version='1.0',
      description='Used to calculate cloud coverage form an image.',
      author='Andrew Vadnais, Gage Davidson',
      author_email='avadnais@oswego.edu',
      packages=['cloudcoverage'],
      data_files=['*.xml'],
     )
     
