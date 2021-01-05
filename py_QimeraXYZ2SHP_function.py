# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 2021

@author: XLGEO
"""

import pandas as pd
import requests
import os
import glob
import zipfile
import geopandas as gpd
from shapely.geometry import Point
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from py_shared import XYZ2SHP
from py_shared import nameList_F_withExt
from py_shared import pathList_F_ext

for xyz in pathList_F_ext(os.path.dirname(__file__),'*.xyz'):
    XYZ2SHP(xyz)

