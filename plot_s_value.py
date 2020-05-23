#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:09:10 2019

@author: amber
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from file_read_backwards import FileReadBackwards as readreverse
import math


iteration = 30
threshold = 0.5  # to determine whether it's switched on or off after optimization



#pose_quantity = 808 # manhattan: 3499 garage: 1660 csail: 1044 mit: 808
#inlier_quantity = 20 # manhattan: 2097 garage: 4615 csail: 128 mit: 20
#outlier_quantity = 5

# In[]:

def process():
    
    #inlier_quantity = 256
    #outlier_quantity = 256
    
    
    print(sys.argv)
    
    if len(sys.argv) > 1:
        inlier_quantity = int(sys.argv[1])
        outlier_quantity = int(sys.argv[2]) 
    
    
    posegraph_input_path = "input.g2o" #"/home/amber/stew/test_backend/MIT_random10_dcs50/mit_seed_1/input.g2o"#
    text_output_path = "s_value.txt"    
    lc_edge_quantity = inlier_quantity + outlier_quantity 
    
    # In[]:
       
    # read input file, find last N edges
    #find all edge ID-pair and outlier ID-pair
    f = open(posegraph_input_path, "r")
    i = 0
    all_lc_edge_pair_search_phrases = []    # list of [str0, str1], each strpair represents one loop closure
    outlier_pair_search_phrases = []        # list of [str0, str1], each strpair represents one loop closure
    all_lc_edge_value = pd.DataFrame(columns = range(0, lc_edge_quantity), index=range(0, iteration+2))
    # 0th row: vertex_from
    # 1st row: vertex_to
    # 1st row: scale value
    
    with readreverse(posegraph_input_path, encoding="utf-8") as obj:
        while i < outlier_quantity + inlier_quantity:
            line = obj.readline()
            line_stripped = line.strip('\n')
            line_splitted = line_stripped.split(' ')
            all_lc_edge_pair_search_phrases.append([line_splitted[1], line_splitted[2]])
            all_lc_edge_value[lc_edge_quantity - i - 1].iloc[0] = int(line_splitted[1]) # fill from the last column
            all_lc_edge_value[lc_edge_quantity - i - 1].iloc[1] = int(line_splitted[2]) # fill from the last column
            if i < outlier_quantity:
                outlier_pair_search_phrases.append([line_splitted[1], line_splitted[2]])
                
            i += 1
            
    all_lc_edge_pair_search_phrases = all_lc_edge_pair_search_phrases[::-1]  #reverse
    outlier_pair_search_phrases = outlier_pair_search_phrases[::-1]          #reverse
    # In[]:
    
    all_lc_edge_value = all_lc_edge_value.sort_values(by=0, axis=1)
    input_edge_sequence = pd.DataFrame(all_lc_edge_value.columns) 
    # append the sorted edge_sequence to last row, so later can be used to reverse the sorting
    # In[]:
    all_lc_edge_value.columns = range(0, lc_edge_quantity) # refresh the columns
    
    all_lc_edge_value = all_lc_edge_value.append(input_edge_sequence.transpose(), ignore_index=True)
    
    # In[]:
    
    #read s_value_file
    
    
    
    f = open(text_output_path, "r")
    i = 0
    while i < (lc_edge_quantity) *iteration: 
        line = f.readline()
        line_stripped = line.strip('\n')
        line_splitted = line_stripped.split(' ')
        if len(line_splitted) > 1:           
            
            if i < lc_edge_quantity:        
                all_lc_edge_value[i].iloc[2] = float(line_splitted[1])
            else:
                all_lc_edge_value[i%lc_edge_quantity].iloc[i//lc_edge_quantity+2] = float(line_splitted[1])
            
        i += 1
    
    # In[]:
    # revert the sorting
    all_lc_edge_value = all_lc_edge_value.sort_values(by=32, axis=1)
    # In[]:
        
    
    #for i in range(2, iteration+2): # starts from 2nd row, 0th and 1st row are for intpair
    inlier_value=all_lc_edge_value.iloc[31,0:inlier_quantity]
    rejected_inlier = 0
    print('rejected inliers: ')
    for i in range(0, inlier_quantity):
        if inlier_value.iloc[i] < threshold:
            print([all_lc_edge_value.iloc[0,i], all_lc_edge_value.iloc[1,i]], inlier_value.iloc[i])
            rejected_inlier += 1
    print('Num of rejected inliers: ', rejected_inlier)
    fig, ax = plt.subplots()
    plt.plot(range(0,inlier_quantity), inlier_value, 'o-')
    plt.legend(("inlier value",))
    plt.savefig("inlier_value_iteration_"+str(31-1))
    plt.show()
    
    # In[]:
    acceptted_outlier = 0
    print('acceptted outliers: ')
        
    outlier_value=all_lc_edge_value.iloc[31,inlier_quantity:lc_edge_quantity]
    for i in range(0, outlier_quantity):
        if outlier_value.iloc[i] > threshold:
            print([all_lc_edge_value.iloc[0,i+inlier_quantity], all_lc_edge_value.iloc[1,i+inlier_quantity]], outlier_value.iloc[i])
            acceptted_outlier += 1
    
    print('Num of acceptted outliers: ', acceptted_outlier)
    fig, ax = plt.subplots()
    plt.plot(range(0,outlier_quantity), outlier_value, 'ro-')
    plt.legend(("outlier value",))
    plt.savefig("outlier_value_iteration_"+str(31-1))
    plt.show()

# In[]:
process()
