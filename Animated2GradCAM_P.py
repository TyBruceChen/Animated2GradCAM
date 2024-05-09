# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:35:05 2024

@author: tc922
"""


import torch
from torch import nn
import timm

import numpy as np
import pandas as pd
from GradCAM import *
from nparr2csv import *


###############################################
root_path = '../'

#load the model and conduct prediction
model_path = root_path + 'models/densenet121-lr_1e-3/COVID_balancedpaper1_.pt'
model = torch.load(model_path)

#read the img test file path
test_file_path = root_path + 'processed/test.txt'
separator = '  '
#####
layer_idx = 3
grad_cam_manipul = 'Normal'  #the pre-manipulation before grad-cam 'Normal' -> None for CNN. 'ViT' for transformers
class_list = ['COVID-19', 'Lung_Opacity','Normal','Pneumonia']
save_path = 'Images/'
df_name_path = 'temp_name-densenet121.csv'
generate_new_img = True  #True: generate the csv file and gradcam imgs, False: only generate csv file 
    #(the generatetion of img csv is in the next part)
relu_threshold = 8 #default is 8
#####
csv_save_mode = ''
img_name_extra = '' #extra suffix of image path
H,W = (200,200)
df_path = 'temp-densenet121'
limit_itr = 430 #the max number of images you want to generate in csv file

df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])

###############################################

with open(test_file_path) as f:
    line = [line for line in f]

line = line[:]

label_list = []
img_path_list = []
for img_info in line:
    img_path, label = img_info.strip().split(separator)
    img_path_list.append(root_path + img_path)
    label_list.append(int(label))
    
    
#generate CAMs
###############################################
"""
layer_idx = 6
class_list = ['COVID-19', 'Lung_Opacity','Normal','Pneumonia']
save_path = 'Images/'
df_name_path = 'temp_name.csv'
generate_new_img = False  #True: generate the csv file and gradcam imgs, False: only generate csv file 
    #(the generatetion of img csv is in the next part)
"""
###############################################

class_index_counter = {}
for label in class_list:
    class_index_counter[label] = 0

df_name = pd.DataFrame(columns = ['img_index','img_type','Index','Type']) 
#img_indx is individual id for each img. img_type is the GT of image, Index is the id with same GT type of image
    #Type is the prediction type from the model
for i,img_path in enumerate(img_path_list):
    cam = GradCAM(model, img_path, layer_idx = layer_idx, model_type= grad_cam_manipul, relu_threshold= relu_threshold)
    cam()
    confidence = cam.confidence
    
    if generate_new_img == True:
        cam.imposing_visualization(save_path = save_path + str(i)+ '.png')
    
    if label_list[i] != cam.result_class:
        Type = 'Negative: ' + class_list[int(cam.result_class)]
    else:
        Type = 'Positive'
        
    df_name_item = pd.DataFrame([[i,
                                  class_list[label_list[i]],
                                  class_index_counter[class_list[label_list[i]]],
                                  Type,
                                  confidence]],
                                columns = ['img_index','img_type','Index','Type','Confidence (%)'])
    df_name = pd.concat([df_name,df_name_item])
    
    class_index_counter[class_list[label_list[i]]] += 1 #increase the class_index
    if i == limit_itr:
        break
    
#convert np.ndarray into csv: https://www.geeksforgeeks.org/convert-numpy-array-into-csv-file/
df_name[:].to_csv(df_name_path)

#save the img information into csv file (img_pixels (row, columns, color_channel_value), img_index (for select))
###############################################
"""
img_name_extra = '' #extra suffix of image path
H,W = (200,200)
df_path = 'temp'
limit_itr = 695

df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])
"""
###############################################
resize_h = H
resize_w = W

if csv_save_mode == 'Overall':
    for i in range(len(line)):
        #generate the (Grad-CAM) image path for reading pixel
        img_path = save_path + str(df_name.iloc[i,0]) + img_name_extra + '.png'
        df_item = pil_nparr2csv(img_path,resize_h, resize_w)
        df_item['img_index'] = np.tile(i,resize_h**2)
        df = pd.concat([df,df_item])
        print(i)
        if i == limit_itr:  #sometimes there are too many images for limited PC RAM, you can set to load portion of them
            break
    df.to_csv(df_path + '.csv')

else:
    resize_h = int(H/2 + 40)
    resize_w = int(W/2 + 40)
    
    img_name_extra = '-origin'
    for i in range(len(line)):
        #generate the (Grad-CAM) image path for reading pixel
        img_path = save_path + str(df_name.iloc[i,0]) + img_name_extra + '.png'
        df_item = pil_nparr2csv(img_path,resize_h, resize_w)
        df_item['img_index'] = np.tile(i,resize_h**2)
        df = pd.concat([df,df_item])
        print(i)
        if i == limit_itr:  #sometimes there are too many images for limited PC RAM, you can set to load portion of them
            break
    df.to_csv(df_path + img_name_extra + '.csv')
    df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])
        
    img_name_extra = '-overlapped'
    for i in range(len(line)):
        #generate the (Grad-CAM) image path for reading pixel
        img_path = save_path + str(df_name.iloc[i,0]) + img_name_extra + '.png'
        df_item = pil_nparr2csv(img_path,resize_h, resize_w)
        df_item['img_index'] = np.tile(i,resize_h**2)
        df = pd.concat([df,df_item])
        print(i)
        if i == limit_itr:
            break
    df.to_csv(df_path+ img_name_extra + '.csv')
    df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])
    
    img_name_extra = '-heatmap'
    for i in range(len(line)):
        #generate the (Grad-CAM) image path for reading pixel
        img_path = save_path + str(df_name.iloc[i,0]) + img_name_extra + '.png'
        df_item = pil_nparr2csv(img_path,resize_h, resize_w)
        df_item['img_index'] = np.tile(i,resize_h**2)
        df = pd.concat([df,df_item])
        print(i)
        if i == limit_itr:
            break
    df.to_csv(df_path+ img_name_extra + '.csv')
    df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])
    
    img_name_extra = '-colormap'
    for i in range(len(line)):
        #generate the (Grad-CAM) image path for reading pixel
        img_path = save_path + str(df_name.iloc[i,0]) + img_name_extra + '.png'
        df_item = pil_nparr2csv(img_path,resize_h, resize_w)
        df_item['img_index'] = np.tile(i,resize_h**2)
        df = pd.concat([df,df_item])
        print(i)
        if i == limit_itr:
            break
    df.to_csv(df_path+ img_name_extra + '.csv')
    df = pd.DataFrame(columns = ['row(height)','column(width)','color(hex)','img_index','label'])

#save dataframes
###############################################
#df_name.to_csv(df_name_path)


