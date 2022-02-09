#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 15:47:29 2021

@author: aaa
"""
import scipy.io as sp
import cv2
import pickle
import pdb
import numpy as np
import os
import pdb
import argparse
import scipy.io as sp
from PIL import ImageFont, ImageDraw, Image
import pandas as pd


head_model='24'
person_id='17'
trial_id='1'
filename='test_trial'

#path_to_pickle file
data = pd.read_pickle('D:/Academic/RIT/4-summer/Summer Co-op working repository/RIT_Eyes_RenderingPipeline/RITeyes_pipeline_(26MAY2021)/GIW_Data/giw_blink/PrIdx_'+person_id+'_TrIdx_'+trial_id+'.p')
#path_to_renderings
path='D:/Academic/RIT/4-summer/Summer Co-op working repository/RIT_Eyes_RenderingPipeline/RITeyes_pipeline_(26MAY2021)/renderings/'+head_model+'/'+filename+'/PrIdx_'+person_id+'_TrIdx_'+trial_id+'/'+'synthetic'

size=(1280,480)
out = cv2.VideoWriter(os.path.join(path,'real-syn.avi'),cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
cap = cv2.VideoCapture('/media/aaa/backup/Data_from_RC/FinalSet/'+person_id+'/'+trial_id+'/eye1.mp4')

for i in range (len(data['frame_no'])-2):
    cap.set(cv2.CAP_PROP_POS_FRAMES, data['frame_no'][i+1])
    print('Position:'+ str( int(cap.get(cv2.CAP_PROP_POS_FRAMES))) +'  frame number:'+str(i))
    ret, frame = cap.read()
    if ret:
        syn=cv2.imread(os.path.join(path,'synthetic',str(i+1).zfill(4)+'.tif'))
        print (i, syn.shape, frame.shape,person_id,trial_id)
        frame=Image.fromarray(np.uint8(frame))
        file_to_save=np.concatenate((frame,syn),axis=1)
        out.write(file_to_save)
print ('Completed')
out.release()

