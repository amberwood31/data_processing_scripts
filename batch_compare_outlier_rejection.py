import os
import numpy as np
import matplotlib.pyplot as plt
import sys


dataset = ['manhattan']#['csail', 'manhattan', 'intel'] #, 'mit']
inliers_quantity = [1952]#[127, 1952, 256] #, 20]
poses_quantities = [3500]
inliers_percentages = [0.9, 0.8, 0.7, 0.6, 0.5]
sample_size = 10
methods = ['vertigo', 'dcs', 'cbsc', 'slampp']
method_name = ['SC', 'DCS', 'CBOR', 'POFC']
comparison_set = sys.argv[1]

outliers_quantity = []
for i in range(0, len(dataset)):
    outliers_quantity.append([])
    for inlier_percentage in inliers_percentages:
        inlier_n = inliers_quantity[i]
        outliers_quantity[-1].append(round(inlier_n / inlier_percentage - inlier_n))
#print(outliers_quantity)

os.chdir('/home/amber/stew/test_backend/'+dataset[0])


outliers_mean_std = np.zeros((5, 8))

for i in range(0,len(dataset)):
    for j in range(0, len(inliers_percentages)):

        outliers_accepted = np.ones((sample_size, 4)) 

        dataset_name = dataset[i]
        configuration_name = 'random' + str(outliers_quantity[i][j])
        
        for m in range(0, len(methods)):
            method = methods[m]
            f = open(method + '_outlier_' + configuration_name, 'r')
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
            
            if method == 'vertigo':
                k = 0
                for line in content:
                    line_content = line.split(' ')
                    #print(line_content)
                    value = float(int(line_content[3])) / outliers_quantity[i][j]
                    outliers_accepted[k,0] = value
                    print(value)
                    k += 1

            if method == 'dcs':
                k = 0
                for line in content:
                    line_content = line.split(' ')
                    if len(line_content) == 6:
                        value = float(int(line_content[-1])) / outliers_quantity[i][j]
                        outliers_accepted[k,1] = value
                        print(value)
                        k += 1

            if method == 'cbsc':
                k = 0
                for line in content:
                    line_content = line.split(' ')
                    #print(line_content)
                    value = float(int(line_content[3])) / outliers_quantity[i][j]
                    outliers_accepted[k,2] = value
                    print(value)
                    k += 1

            if method == 'slampp':
                if content == []:
                    print('slampp acceptted all inliers')
                else:
                    k=0
                    for line in content:
                        line_content = line.split(' ')
                        print(line_content)
                        outliers_accepted[k,3] = float(int(line_content[0])) / outliers_quantity[i][j]
                        k += 1

            
        outliers_accepted_mean = np.mean(outliers_accepted, axis = 0)
        outliers_accepted_std = np.std(outliers_accepted, axis = 0)

        for m in range(0, len(methods)):
            outliers_mean_std[j, m*2] = outliers_accepted_mean[m]
            outliers_mean_std[j, m*2+1] = outliers_accepted_std[m]


fig, ax = plt.subplots()
mean = outliers_mean_std[:,0]
std = outliers_mean_std[:,1]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean,  c='#E84354', label=method_name[0], alpha=1, linewidth=3, marker='v', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#E84354', alpha=0.35)


mean = outliers_mean_std[:,2]
std = outliers_mean_std[:,3]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean,  c='#3DDC97', label=method_name[1], alpha=1, linewidth=2, linestyle=':', marker='*', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#3DDC97', alpha=0.35)

mean = outliers_mean_std[:,4]
std = outliers_mean_std[:,5]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean,  c='#FFCC00', label=method_name[2], alpha=1, linewidth=2, linestyle='-.', marker='P', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#FFCC00', alpha=0.35)

mean = outliers_mean_std[:,6]
std = outliers_mean_std[:,7]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean,  c='#0055D4', label=method_name[3], alpha=1, linewidth=1, marker='X', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#0055D4', alpha=0.35)





legend = ax.legend(loc=(0.03, 0.35), fontsize='large')
plt.xticks([1.5,3.5, 5.5, 7.5, 9.5], [10,20,30,40,50], fontsize = 12)

ax.set_xlabel('number of outliers (%)', fontsize='large')
ax.set_ylabel('outliers acceptted (%)', fontsize='large')

plt.savefig(dataset_name + '_' + comparison_set + '_outliers_accepted.png')
plt.show()
                


