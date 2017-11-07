import scipy
from scipy import misc
from scipy.ndimage import filters
import glob
import numpy as np
import re
import csv

def extract_patch(col_img):

    image = np.mean(col_img[:, :, 0:2].astype(np.int), axis=2)

    filt1 = [[  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
             [  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
             [  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
             [  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
             [  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
             [  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
             [  -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1],
             [  -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1],
             [  -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1],
             [  -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1],
             [  -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1]
             ]
 
    threshold = np.sum(np.equal(filt1, 1).astype(np.int))

    filt2 = np.flipud(filt1)
    filt3 = np.fliplr(filt1)
    filt4 = np.fliplr(filt2)

    #filt = np.tile([[-1], [-1], [-1], [1], [1], [1], [1], [1]], [1, 15]) 

    signal1 = scipy.ndimage.filters.convolve((image == 0).astype(np.float), filt1) 
    signal2 = scipy.ndimage.filters.convolve((image == 0).astype(np.float), filt2) 
    signal3 = scipy.ndimage.filters.convolve((image == 0).astype(np.float), filt3) 
    signal4 = scipy.ndimage.filters.convolve((image == 0).astype(np.float), filt4) 

    expand = [np.shape(filt1)[0] / 2, np.shape(filt1)[1] / 2]

    tl_coord = np.where(signal1 >= threshold)
    bl_coord = np.where(signal2 >= threshold)
    tr_coord = np.where(signal3 >= threshold)
    br_coord = np.where(signal4 >= threshold)

    print(tl_coord,
    bl_coord,
    tr_coord,
    br_coord)   
    # test unique response of corners, and corners of rectangular 
    unique_response = (len(tl_coord[0]) == 1) and (len(tr_coord[0]) == 1) and (len(bl_coord[0]) == 1) and (len(br_coord[0]) == 1)
    at_corner = (tl_coord[0][0] == tr_coord[0][0]) and \
                (bl_coord[0][0] == br_coord[0][0]) and \
                (tl_coord[1][0] == bl_coord[1][0]) and \
                (tr_coord[1][0] == br_coord[1][0])

    if not (unique_response and at_corner):
        print(tl_coord)
        print(tr_coord)
        print(bl_coord)
        print(br_coord)
    
    xcoord = [tr_coord[1][0], tl_coord[1][0]]
    ycoord = [bl_coord[0][0], tl_coord[0][0]]

    print(xcoord)
    print(ycoord)

    patch = col_img[ycoord[0] : ycoord[1] + 1, xcoord[0] : xcoord[1] + 1, :]

    # check the patch -- it should has a margin with width 1 
    psum = np.sum(patch[:, :, 0:3], axis=2)
    col_sum = np.sum(psum, axis=1)
    row_sum = np.sum(psum, axis=0)
    if not (col_sum[0] == 0 and col_sum[-1] == 0 and row_sum[0] == 0 and row_sum[-1] == 0):
        raise Exception('The patch is not correct')

    patch = patch[1:-1, 1:-1, :]

    return patch



def read_label():
    
    file_name = '../data/labels.csv'
    with open(file_name, mode='r') as infile:
        reader = csv.reader(infile)
        label_dict = {rows[0]:rows[1] for rows in reader}

    print(label_dict)
    return label_dict





paths = glob.glob("../data/images/*.png")
label_dict = read_label()

label_list = []
for i in range(1, len(paths) + 1): 
    
    # read image from image path
    image_path = paths[len(paths) - i]
    col_img = misc.imread(image_path)
    print(image_path)

    # look up image label 
    match = re.search('[0-9]{1,2}\.[0-9]{1,2}', image_path)
    name = match.group(0)
    tokens = name.split('.')
    name = (tokens[0] if len(tokens[0]) >= 2 else '0' + tokens[0]) + '_' + tokens[1]
    print(name)
    label = label_dict[name]

    # extract patch
    patch = extract_patch(col_img)
    
    # check the patch

    misc.imsave('../data/patches/' + label + '/' + name + '.png', patch) 


