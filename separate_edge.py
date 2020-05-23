#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:51:08 2019

@author: amber
"""

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# In[2]:

EDGE_KEYWORD = "EDGE3"
VERTEX_KEYWORD = "VERTEX3"


def separate_edge(file_name, output_name, dimension):
#file_name = '/home/amber/Downloads/input_INTEL_g2o(1).g2o'
    
    if int(dimension) == 2:
        df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(12))
        vertex = df.loc[df[0] == "VERTEX_SE2"]
        edges = df.loc[df[0] == "EDGE_SE2"]
        edges.columns = ['name', 'vertex_from', 'vertex_to', 'x', 'y', 'the', 'i0', 'i1', 'i2', 'i3', 'i4', 'i5']
        edges = edges.astype({'vertex_to': int, 'x': float, 'y': float, 'the': float})
    elif int(dimension) == 3:
        if EDGE_KEYWORD == "EDGE_SE3:QUAT":
            df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(31))
        elif EDGE_KEYWORD == "EDGE3":
            df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(30))
        vertex = df.loc[df[0] == VERTEX_KEYWORD]
        edges = df.loc[df[0] == EDGE_KEYWORD]
        if EDGE_KEYWORD == "EDGE_SE3:QUAT":
            edges.columns = ['name', 'vertex_from', 'vertex_to', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw', 'i11', 'i12', 'i13', 'i14', 'i15', 'i16', 'i22', 'i23', 'i24', 'i25','i26','i33', 'i34', 'i35','i36', 'i44', 'i45', 'i46', 'i55', 'i56', 'i66']
        elif EDGE_KEYWORD == "EDGE3":
            edges.columns = ['name', 'vertex_from', 'vertex_to', 'x', 'y', 'z', 'ro', 'pit', 'yaw', 'i11', 'i12', 'i13', 'i14', 'i15', 'i16', 'i22', 'i23', 'i24', 'i25','i26','i33', 'i34', 'i35','i36', 'i44', 'i45', 'i46', 'i55', 'i56', 'i66']

        edges = edges.astype({'vertex_to': int, 'x': float, 'y': float, 'z': float})
    
    
    #edges['vertex_to']= edges['vertex_to'].astype(int)
    
    od_edges = edges.loc[(edges['vertex_to'] - edges['vertex_from']) == 1]
    lc_edges = edges.loc[(edges['vertex_to'] - edges['vertex_from']) != 1]
    
    sorted_od_edges = od_edges.sort_values(by= ['vertex_from'], ascending=[True])
    
    if lc_edges.loc[lc_edges.index[-1], 'vertex_to']- lc_edges.loc[lc_edges.index[-1], 'vertex_from'] > 0:# if vertex_from < vertex_too
        #temp1 = edges.sort_values(by= 'vertex_to')
        sorted_edges = edges.sort_values(by= ['vertex_to', 'vertex_from'], ascending=[True, False])
    else:
        sorted_edges = edges.sort_values(by= ['vertex_from', 'vertex_to'], ascending=[True, True])
            
    sorted_od_edges.to_csv(output_name, header=None, index=None, sep=' ', float_format='%0.6f')
    #return sorted_edges

# In[3]:


#sort(str(sys.argv[1]))
print(sys.argv)
separate_edge(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
