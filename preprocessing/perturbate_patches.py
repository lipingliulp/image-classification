import scipy
from scipy import misc
from scipy.ndimage import filters
import glob
import numpy as np
import re
import csv

def perturbate_patch(color_img):

    fsize = 128 
    img_fsize = scipy.misc.imresize(color_img, [fsize, fsize])

    pwidth = 10
    img_pad = np.pad(img_fsize, [(pwidth, pwidth), (pwidth, pwidth), (0, 0)]) 
        
    nperm = 32
    for iperm in range(nperm)  
        img_rotat = scipy.ndimage.rotate(img_pad, rdeg, reshape=False)
    
        img_rotat[img_rotat == 0] =  



