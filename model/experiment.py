


nfold = 10
confusion = np.zeros([2, 2])


base_dir = '../data/f0train/train'
for fold in range(nfold):

    (pred_label, valid_label) = fold_train_test(fold)


accuracy = (confusion[0, 0] + confusion[1, 1]) * 1.0 / np.sum(confusion)

print('the confusion matrix is ', confusion)
print('the accuracy is  ', confusion)






