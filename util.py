# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from constants import Constants

class Util:
    
    @staticmethod
    def ACTransform(cvimg, num):
        x, y, channel = cvimg.shape
        n = x
        mat_img = np.zeros([x, y, channel])
        for i in range(0, x):
            for j in range(0, y):
                mat_img[i][j] = cvimg[(i+j)%n][(i+2*j)%n]  
        return mat_img 
    
    @staticmethod
    def createImgMat(imgaddress):
        
        img = Image.open(imgaddress) 
        pixelmat = img.load()
        color = 1
        if type(pixelmat[0,0]) == int:
          color = 0
        size = img.size 
        img_mat = []
        for w in range(int(size[0])):
            row = []
            for h in range(int(size[1])):
                    row.append((pixelmat[w,h]))
            img_mat.append(row)
        return img_mat, size[0], size[1],color
    

