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
from util import Util

class Encrypt:
   
    
    
    
    
    def ArnoldCat(self,imageName, key):
        img = cv2.imread(Constants.IMAGE_FOLDER + imageName)
        for i in range (0,key):
            img = Util.ACTransform(img, i)
        cv2.imwrite(Constants.ENCRYPTED_FOLDER + imageName.split('.')[0] + "_ArnoldCat.png", img)
        plt.imshow(img)
        return img
    
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
    
        L = (R + array_key[12]/256) % 1
        S_x = round(((g[0]+g[1]+g[2])*(10**4) + L *(10**4)) % 256)
        V1 = sum(array_key)
        V2 = array_key[0]
        for i in range(1,13):
            V2 = V2 ^ array_key[i]
        V = V2/V1
    
        L_y = (V+array_key[12]/256) % 1
        S_y = round((V+V2+L_y*10**4) % 256)
        C1_0 = S_x
        C2_0 = S_y
        C = round((L*L_y*10**4) % 256)
        C_r = round((L*L_y*10**4) % 256)
        C_g = round((L*L_y*10**4) % 256)
        C_b = round((L*L_y*10**4) % 256)
        x = 4*(S_x)*(1-S_x)
        y = 4*(S_y)*(1-S_y)
        
        img_mat,dimX, dimY, color = Util.createImgMat(Constants.IMAGE_FOLDER+imageName)
        img_logistic = []
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
                  C_r =((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((array_key[6]+img_mat[i][j][0]) % N) ^ ((C_r + array_key[7]) % N)
                  C_g =((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((array_key[6]+img_mat[i][j][1]) % N) ^ ((C_g + array_key[7]) % N)
                  C_b =((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((array_key[6]+img_mat[i][j][2]) % N) ^ ((C_b + array_key[7]) % N)
                  row.append((C_r,C_g,C_b))
                  C = C_r
    
                else:
                  C = ((array_key[4]+C1) % N) ^ ((array_key[5]+C2) % N) ^ ((array_key[6]+img_mat[i][j]) % N) ^ ((C + array_key[7]) % N)
                  row.append(C)
    
                x = (x + C/256 + array_key[8]/256 + array_key[9]/256) % 1
                y = (x + C/256 + array_key[8]/256 + array_key[9]/256) % 1
                for ki in range(12):
                    array_key[ki] = (array_key[ki] + array_key[12]) % 256
                    array_key[12] = array_key[12] ^ array_key[ki]
            img_logistic.append(row)
    
        im = Image.new("L", (dimX, dimY))
        if color:
            im = Image.new("RGB", (dimX, dimY))
        else: 
            im = Image.new("L", (dimX, dimY)) # L is for Black and white pixels
          
        pix = im.load()
        for x in range(dimX):
            for y in range(dimY):
                pix[x, y] = img_logistic[x][y]
        im.save(Constants.ENCRYPTED_FOLDER+imageName.split('.')[0] + "_Logistic.png", "PNG")