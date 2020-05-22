import os
import numpy as np


dataset = ['manhattan']#['csail', 'manhattan', 'intel'] #, 'mit']
inliers_quantity = [1952]#[127, 1952, 256] #, 20]
poses_quantities = [3500]
inliers_percentages = [0.5, 0.6, 0.7, 0.8, 0.9]
sample_size = 10
methods = ['vertigo', 'dcs', 'cbsc', 'slampp']

outliers_quantity = []
for i in range(0, len(dataset)):
    outliers_quantity.append([])
    for inlier_percentage in inliers_percentages:
        inlier_n = inliers_quantity[i]
        outliers_quantity[-1].append(round(inlier_n / inlier_percentage - inlier_n))
#print(outliers_quantity)

os.chdir('/home/amber/stew/test_backend/'+dataset[0])

for i in range(0,len(dataset)):
    for j in range(0, len(inliers_percentages)):

        dataset_name = dataset[i]
        configuration_name = 'random' + str(outliers_quantity[i][j])

        os.chdir('slampp_' + dataset[i] + '_' + configuration_name)
        os.system('rm slampp_' + configuration_name)
        for k in range(1, sample_size+1):
            os.system('grep consistant clustering_analysis_' + str(k) + '.txt >> slampp_' + configuration_name)
            os.system('grep \'inliers are\' clustering_analysis_' + str(k) + '.txt >> slampp_inlier_' + configuration_name)
            os.system('grep \'outliers are\' clustering_analysis_' + str(k) + '.txt >> slampp_outlier_' + configuration_name)

        os.system('cp slampp_' + configuration_name + ' ../')
        os.system('cp slampp_inlier_' + configuration_name + ' ../')
        os.system('cp slampp_outlier_' + configuration_name + ' ../')
        os.chdir('../')