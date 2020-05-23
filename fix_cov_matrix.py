#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:30:11 2019

@author: amber
"""


# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# In[2]:

DIMENSION = 3
def fix_cov_matrix(file_name, output_name):
#file_name = '/home/amber/Downloads/input_INTEL_g2o(1).g2o'
    if DIMENSION == 2:
        df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(12))
    else:
        df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(31))
    
    lc_edges_information = []
    for i in df.index:
        if df.iloc[i,0] == "EDGE_SE3:QUAT" && (df.iloc[i,2] - df.iloc[i,1]) != 1:# odometry edge
            lc_edges_information.append([df.iloc[i, 25:30]])
            
    lc_edges_information_array = np.array(lc_edges_information)
    information = np.mean(lc_edges_information_array, axis=0)
    
    

            
    df.to_csv(output_name, header=None, index=None, sep=' ', float_format='%0.6f')
    #return sorted_edges

# In[3]:


#sort(str(sys.argv[1]))
print(sys.argv)
uniquify(str(sys.argv[1]), str(sys.argv[2]))