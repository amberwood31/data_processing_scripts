#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# In[2]:


def plot_trajectory(*argv):
    print(argv[0])
    df = pd.read_csv(argv[0], delimiter = " ", header = None, names = range(12))
    vertex = df.loc[df[0] == "VERTEX_SE2"]
    edges = df.loc[df[0] == "EDGE_SE2"]
    od_edges = edges.loc[(edges[2] - edges[1]) == 1]
    lc_edges = edges.loc[(edges[2] - edges[1]) != 1]

    vertex = vertex.sort_values(by = 1) # sorting vertex indexes after rrr
    trajectory_x = np.array(vertex[[2]]) # 2D_trajectory_x
    trajectory_y = np.array(vertex[[3]]) # 2D_trajectory_y

    fig, ax = plt.subplots()
    plt.plot(trajectory_x, trajectory_y, 'b')
    
    for index in lc_edges.index:
        plt.plot([trajectory_x[lc_edges.loc[index, 1]][0], trajectory_x[int(lc_edges.loc[index, 2])][0]], [trajectory_y[lc_edges.loc[index, 1]][0], trajectory_y[int(lc_edges.loc[index, 2])][0]], 'r')

    plt.axis('equal')
    filename = argv[0].split(".")
    plt.savefig(filename[0])
    plt.show()

# In[3]:


print ('READ g2o file: ' + str(sys.argv[1]))
plot_trajectory(str(sys.argv[1]))



# In[ ]:





# In[ ]:





# In[ ]:




                                                       


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




