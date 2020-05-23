

import os


dataset = ['csail', 'manhattan', 'intel']
inliers_quantity = [127, 1952, 256]
inliers_percentages = [0.5]
outliers_quantity = [127, 1952, 256]
group_size = 8
outliers_group_quantity = outliers_quantity #[int(x/group_size) for x in outliers_quantity]
print(outliers_group_quantity)
sample_size = 10



#os.chdir('/home/amber/stew/pose_dataset/')

for i in range(0,len(dataset)):
    os.system('./create_new_dataset_folder.sh '+ dataset[i]+ ' group'+str(outliers_quantity[i]))
    print('adding new dataset folder: '+dataset[i]+'_'+'group'+str(outliers_quantity[i]))

for i in range(0, len(dataset)):
    dataset_name = dataset[i]
    configuration_name = 'group'+str(outliers_quantity[i])
    os.chdir(dataset_name + '_'+ configuration_name)
    os.system('python uniquify.py ' + dataset_name + '.g2o' + ' ' + dataset_name + '.g2o_unique.g2o')
    if dataset_name == 'mit':
        os.system('./generate_dataset.sh ' + dataset_name + '.g2o_unique.g2o ' + str(sample_size) + ' ' + str(outliers_group_quantity[i]) + ' ' + str(0) + ' ' + str(group_size))
    else:
        os.system('./generate_dataset.sh ' + dataset_name + '.g2o_unique.g2o ' + str(sample_size) + ' ' + str(outliers_group_quantity[i]) + ' ' + str(group_size))
    os.chdir('..')


