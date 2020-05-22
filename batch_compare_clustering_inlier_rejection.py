import os
import numpy as np
import matplotlib.pyplot as plt
import sys


dataset = ['intel']#['csail', 'manhattan', 'intel'] #, 'mit']
inliers_quantity = [256]#[127, 1952, 256] #, 20]
poses_quantities = [1228]
inliers_percentages = [0.9, 0.8, 0.7, 0.6, 0.5]
sample_size = 10
methods = ['cbsc', 'slampp']
method_name = ['CPS', 'OFCC']
comparison_set = sys.argv[1]

outliers_quantity = []
for i in range(0, len(dataset)):
    outliers_quantity.append([])
    for inlier_percentage in inliers_percentages:
        inlier_n = inliers_quantity[i]
        outliers_quantity[-1].append(round(inlier_n / inlier_percentage - inlier_n))
#print(outliers_quantity)

print(os.getcwd())
#os.chdir('/home/amber/stew/test_backend/'+dataset[0]) # this is only useful when one wants to run this script from folders that are not the specific results folder
                                                        # it might cause confusion since later generated files are saved locally


inliers_mean_std = np.zeros((5, 4))

for i in range(0,len(dataset)):
    for j in range(0, len(inliers_percentages)):

        inliers_accepted = np.ones((sample_size, 2)) 

        dataset_name = dataset[i]
        configuration_name = 'random' + str(outliers_quantity[i][j])
        
        for m in range(0, len(methods)):
            method = methods[m]

            if method == 'cbsc':
                f = open(method + '_clustering_inlier_' + configuration_name, 'r')
                content = f.readlines()
                content = [x.strip() for x in content]
                f.close()
                k = 0
                for line in content:
                    line_content = line.split(' ')
                    #print(line_content)
                    value = float(int(line_content[3])) / inliers_quantity[i]
                    inliers_accepted[k,0] = 1.0 - value # the text file recorded rejected number
                    #print(value)
                    k += 1

            if method == 'slampp':
                f = open(method + '_inlier_' + configuration_name, 'r')
                content = f.readlines()
                content = [x.strip() for x in content]
                f.close()
                if content == []:
                    print('slampp acceptted all inliers')
                else:
                    k=0
                    for line in content:
                        line_content = line.split(' ')
                        #print(line_content)
                        inliers_accepted[k,1] = (inliers_quantity[i] - float(int(line_content[0]))) / inliers_quantity[i]
                        k += 1

        inliers_accepted_mean = np.mean(inliers_accepted, axis = 0)
        inliers_accepted_std = np.std(inliers_accepted, axis = 0)

        for m in range(0, len(methods)):
            inliers_mean_std[j, m*2] = inliers_accepted_mean[m]
            inliers_mean_std[j, m*2+1] = inliers_accepted_std[m]


np.savetxt('clustering_inlier_mean_std', inliers_mean_std)

fig, ax = plt.subplots()
mean = inliers_mean_std[:,0]
std = inliers_mean_std[:,1]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean*100,  c='#E84354', label=method_name[0], alpha=1, linewidth=3, marker='v', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#E84354', alpha=0.35)


mean = inliers_mean_std[:,2]
std = inliers_mean_std[:,3]
ax.plot([1.5,3.5, 5.5, 7.5, 9.5], mean*100,  c='#3DDC97', label=method_name[1], alpha=1, linewidth=2, linestyle=':', marker='*', markersize=10)
#ax.fill_between([1.5,3.5, 5.5, 7.5, 9.5], mean-std, mean+std, facecolor='#3DDC97', alpha=0.35)





legend = ax.legend(loc=(0.03, 0.35), fontsize='large')
plt.xticks([1.5,3.5, 5.5, 7.5, 9.5], [10,20,30,40,50], fontsize = 12)

ax.set_xlabel('number of outliers (%)', fontsize='large')
ax.set_ylabel('inliers accepted (%)', fontsize='large')

plt.savefig(dataset_name + '_' + comparison_set + '_clustering_inliers_accepted.png')
plt.show()
                


