#!/usr/bin/env python
import sys
from distutils.core import setup

try:
    import PIL
except ImportError:
    sys.exit("""You need Pillow!
                install it from https://pypi.org/project/Pillow/
                or run pip install Pillow.""")
                
try:
    import shapely
except ImportError:
    sys.exit("""You need Shapely!
                install it from https://pypi.org/project/Shapely/
                or run pip install shapely.""")
                
try:
    import cv2
except ImportError:
    sys.exit("""You need opencv!
                install it from https://pypi.org/project/opencv-python/
                or run pip install opencv-python.""")
                
setup(name='cloudcoverage',
      version='2.2.1',
      description='Calculates cloud coverage from an image and sends email alerts when waterspouts are detected.',
      author='Andrew Vadnais, Gage Davidson, Peter Bush',
      author_email='avadnais@oswego.edu',
      packages=['cloudcoverage'],
      url="https://github.com/GDave50/Cloud-Coverage-Calculator",
      license='MIT',
     )
     
