#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:18:08 2019

@author: amber
"""

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# In[2]:

DIMENSION = 2
def uniquify(file_name, output_name):
#file_name = '/home/amber/Downloads/input_INTEL_g2o(1).g2o'
    if DIMENSION == 2:
        df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(12))
    else:
        df = pd.read_csv(file_name, delimiter = " ", header = None, names = range(31))
    
    df = df.drop_duplicates([1,2])
    
    

            
    df.to_csv(output_name, header=None, index=None, sep=' ', float_format='%0.6f')
    #return sorted_edges

# In[3]:


#sort(str(sys.argv[1]))
print(sys.argv)
uniquify(str(sys.argv[1]), str(sys.argv[2]))
