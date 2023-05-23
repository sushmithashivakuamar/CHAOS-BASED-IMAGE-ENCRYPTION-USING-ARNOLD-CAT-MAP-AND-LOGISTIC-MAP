# -*- coding: utf-8 -*-
import cv2
from encrypt import Encrypt
from decrypt import Decrypt
from constants import Constants
image_name = "picka"
ext = ".png"
key = 20
key_log = "abcdefghijklm"


enc = Encrypt()
enc.ArnoldCat( image_name+ext, key)
enc.Logistic(image_name +ext ,key_log)


dec = Decrypt()
dec.ArnoldCat( image_name + ext ,key)
dec.Logistic(image_name + ext,key_log)