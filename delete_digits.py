#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:18:08 2019

@author: amber
"""

# In[1]:


import pandas as pd
import numpy as np
import sys

# In[2]:


DIMENSION = 2
dataset_name = sys.argv[1]
SEED = 10


def delete_digits(file_name, output_name):
#file_name = '/home/amber/Downloads/input_INTEL_g2o(1).g2o'

    f = open(file_name, "r")
    content = f.readlines()
    f.close()

    vertex = []
    edge = []
    for line in content:
        line_stripped = line.strip('\n')
        line_splitted = line_stripped.split(' ')
        if DIMENSION == 2:
            if line_splitted[0] == 'VERTEX_SE2':
                vertex.append(line_splitted)
            elif line_splitted[0] == 'EDGE_SE2':
                edge.append(line_splitted)
            else:
                sys.exit("file template wrong")
        elif DIMENSION == 3:
            if line_splitted[0] == 'VERTEX_SE3':
                vertex.append(line_splitted)
            elif line_splitted[0] == 'EDGE_SE3':
                edge.append(line_splitted)
            else:
                sys.exit("file template wrong")
        else:
            sys.exit("dimension value wrong")

    df_vertex = pd.DataFrame(vertex)
    df_edge = pd.DataFrame(edge)
    
    df_edge[2] = df_edge[2].astype(float)
    df_edge[2] = df_edge[2].astype(int)
    

            
    df_vertex.to_csv(output_name, header=None, index=None, sep=' ', float_format='%0.6f')
    df_edge.to_csv(output_name, mode='a', header=None, index=None, sep=' ', float_format='%0.6f')
    #return sorted_edges

# In[3]:



print(sys.argv)
file_list = []


file_name = dataset_name + '.g2o_unique.g2o'
delete_digits(file_name, file_name)

file_name = dataset_name + '.g2o_unique.g2o_del0.g2o'
delete_digits(file_name, file_name)


for i in range(1, SEED+1):

    file_del0_name = dataset_name + '.g2o_unique.g2o_seed_' + str(i) + '_del0.g2o'
    file_list.append(file_del0_name)

for file_one in file_list:
    delete_digits(file_one, file_one)

print('Cleaned ' + str(len(file_list)+2) + ' files')


#sort(str(sys.argv[1]))
