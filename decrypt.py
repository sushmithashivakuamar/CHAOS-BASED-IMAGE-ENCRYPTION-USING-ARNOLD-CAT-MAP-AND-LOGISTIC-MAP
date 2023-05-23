# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import os
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import cv2 
import random
from math import log
from constants import Constants
from encrypt import Encrypt
from util import Util
class Decrypt:
    
    def ArnoldCat(self,imageName, key):
        cvimg = cv2.imread(Constants.ENCRYPTED_FOLDER + imageName.split('.')[0] + "_ArnoldCat.png")
        print(Constants.ENCRYPTED_FOLDER + imageName)
        plt.imshow(cvimg)
        x, y, channel = cvimg.shape
        dim = x
        dec_iteration = dim
        if (dim%2==0) and 5**int(round(log(dim/2,5))) == int(dim/2):
            dec_iteration = 3*dim
        elif 5**int(round(log(dim,5))) == int(dim):
            dec_iteration = 2*dim
        elif (dim%6==0) and  5**int(round(log(dim/6,5))) == int(dim/6):
            dec_iteration = 2*dim
        else:
            dec_iteration = int(12*dim/7)
        for i in range(key,dec_iteration):
            cvimg = Util.ACTransform(cvimg, i)
        cv2.imwrite(Constants.DECRYPTED_FOLDER + imageName.split('.')[0] + "_ArnoldCat.png",cvimg)
        plt.imshow(cvimg)
        return cvimg

    def Logistic(self,imageName, key):
        N = 256
        array_key = [ord(x) for x in key]
    
        G = [array_key[0:4] ,array_key[4:8], array_key[8:12]]
        g = []
        R = 1
        for i in range(1,4):
            s = 0
            for j in range(1,5):
                s += G[i-1][j-1] * (10**(-j))
            g.append(s)
            R = (R*s) % 1
        
        L_x = (R + array_key[12]/256) % 1
        S_x = round(((g[0]+g[1]+g[2])*(10**4) + L_x *(10**4)) % 256)
        V1 = sum(array_key)
        V2 = array_key[0]
        for i in range(1,13):
            V2 = V2 ^ array_key[i]
        V = V2/V1
    
        L_y = (V+array_key[12]/256) % 1
        S_y = round((V+V2+L_y*10**4) % 256)
        C1_0 = S_x
        C2_0 = S_y
        
        C = round((L_x*L_y*10**4) % 256)
        I_prev = C
        I_prev_r = C
        I_prev_g = C
        I_prev_b = C
        I = C
        I_r = C
        I_g = C
        I_b = C
        x_prev = 4*(S_x)*(1-S_x)
        y_prev = 4*(L_x)*(1-S_y)
        x = x_prev
        y = y_prev
        mat_img,dimX, dimY, color = Util.createImgMat(Constants.ENCRYPTED_FOLDER+imageName.split(".")[0] +"_Logistic.png")
    
        image_logistic = []
        for i in range(dimX):
            row = []
            for j in range(dimY):
                while x <0.8 and x > 0.2 :
                    x = 4*x*(1-x)
                while y <0.8 and y > 0.2 :
                    y = 4*y*(1-y)
                X = round((x*(10**4))%256)
                Y = round((y*(10**4))%256)
                C1 = X ^ ((array_key[0]+X) % N) ^ ((C1_0 + array_key[1])%N)
                C2 = X ^ ((array_key[2]+Y) % N) ^ ((C2_0 + array_key[3])%N) 
                if color:
                    I_r = ((((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((I_prev_r + array_key[7]) % N) ^ mat_img[i][j][0]) + N-array_key[6])%N
                    I_g = ((((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((I_prev_g + array_key[7]) % N) ^ mat_img[i][j][1]) + N-array_key[6])%N
                    I_b = ((((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((I_prev_b + array_key[7]) % N) ^ mat_img[i][j][2]) + N-array_key[6])%N
                    I_prev_r = mat_img[i][j][0]
                    I_prev_g = mat_img[i][j][1]
                    I_prev_b = mat_img[i][j][2]
                    row.append((I_r,I_g,I_b))
                    x = (x +  mat_img[i][j][0]/256 + array_key[8]/256 + array_key[9]/256) % 1
                    y = (x +  mat_img[i][j][0]/256 + array_key[8]/256 + array_key[9]/256) % 1  
                else:
                    I = ((((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((I_prev+array_key[7]) % N) ^ mat_img[i][j]) + N-array_key[6])%N
                    I_prev = mat_img[i][j]
                    row.append(I)
                    x = (x +  mat_img[i][j]/256 + array_key[8]/256 + array_key[9]/256) % 1
                    y = (x +  mat_img[i][j]/256 + array_key[8]/256 + array_key[9]/256) % 1
                for ki in range(12):
                    array_key[ki] = (array_key[ki] + array_key[12]) % 256
                    array_key[12] = array_key[12] ^ array_key[ki]
            image_logistic.append(row)
        if color:
            im = Image.new("RGB", (dimX, dimY))
        else: 
            im = Image.new("L", (dimX, dimY)) # L is for Black and white pixels
        pix = im.load()
        for x in range(dimX):
            for y in range(dimY):
                pix[x, y] = image_logistic[x][y]
        im.save(Constants.DECRYPTED_FOLDER+imageName.split('_')[0] + "_Logistic.png", "PNG")