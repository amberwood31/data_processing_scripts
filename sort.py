#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:21:40 2019

@author: amber
"""

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# In[2]:


def sort(file_name):
#file_name = '/home/amber/Downloads/input_INTEL_g2o(1).g2o'
    df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(12))
    vertex = df.loc[df[0] == "VERTEX_SE2"]
    edges = df.loc[df[0] == "EDGE_SE2"]
    edges.columns = ['name', 'vertex_from', 'vertex_to', 'x', 'y', 'the', 'i0', 'i1', 'i2', 'i3', 'i4', 'i5']
    
    edges = edges.astype({'vertex_to': int, 'x': float, 'y': float, 'the': float})
    
    #edges['vertex_to']= edges['vertex_to'].astype(int)
    
    od_edges = edges.loc[(edges['vertex_to'] - edges['vertex_from']) == 1]
    lc_edges = edges.loc[(edges['vertex_to'] - edges['vertex_from']) != 1]
    
    if lc_edges.loc[lc_edges.index[-1], 'vertex_to']- lc_edges.loc[lc_edges.index[-1], 'vertex_from'] > 0:# if vertex_from < vertex_too
        #temp1 = edges.sort_values(by= 'vertex_to')
        sorted_edges = edges.sort_values(by= ['vertex_to', 'vertex_from'], ascending=[True, False])
    else:
        sorted_edges = edges.sort_values(by= 'vertex_from')
            
    sorted_edges.to_csv('sorted.g2o', header=None, index=None, sep=' ', float_format='%0.6f')
    #return sorted_edges

# In[3]:


#sort(str(sys.argv[1]))
print(sys.argv)
sort(str(sys.argv[1]))