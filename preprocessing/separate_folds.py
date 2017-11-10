import os
import numpy as np

# base data path
#data_path = '../data/patches/'
#save_path = '../data/'
data_path = '../data/fold0/train/'
save_path = '../data/f0train/'

# pos data and negative data at two different directories: pos = 2, neg = 1
pos_list = os.listdir(data_path + '2/') 
neg_list = os.listdir(data_path + '1/')

# separate data in different folds
# set random seed
np.random.seed(seed=27)
nfold = 10
for ifold in range(nfold):
    
    fold_path = save_path + 'fold' + str(ifold)
    if os.path.isdir(fold_path):
        print('Folder ' + fold_path + ' exists, removing it...')
        os.system('rm -r ' + fold_path)
    

    print('Create dir tree at ' + fold_path)
    # create training pos/neg folders
    neg_train_path = save_path + 'fold' + str(ifold) + '/train/1/'
    pos_train_path = save_path + 'fold' + str(ifold) + '/train/2/'
    os.system('mkdir -p ' + neg_train_path)
    os.system('mkdir -p ' + pos_train_path)

    # create validation pos/neg folders
    neg_valid_path = save_path + 'fold' + str(ifold) + '/validation/1/'
    pos_valid_path = save_path + 'fold' + str(ifold) + '/validation/2/'
    os.system('mkdir -p ' + neg_valid_path)
    os.system('mkdir -p ' + pos_valid_path)

    # random permute orders, divide random orders by nfold, and the reminder is the validation fold 
    pos_folds = np.random.permutation(len(pos_list))
    for ins, filename in enumerate(pos_list):
        # copy from pos set
        source = data_path + '2/' + filename
        if pos_folds[ins] % nfold == ifold:
            # in validation set 
            destination = (pos_valid_path + filename)
        else: 
            # in training set
            destination = (pos_train_path + filename)

        ret = os.system('cp ' + source + ' ' + destination)

    # same for test samples
    neg_folds = np.random.permutation(len(neg_list))
    for ins, filename in enumerate(neg_list):
        # copy from neg set
        source = data_path + '1/' + filename
        if neg_folds[ins] % nfold == ifold:
            destination = (neg_valid_path + filename)
        else:
            destination = (neg_train_path + filename)

        ret = os.system('cp ' + source + ' ' + destination)

