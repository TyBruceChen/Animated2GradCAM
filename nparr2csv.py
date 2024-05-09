# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 17:14:27 2024

@author: tc922
"""

from PIL import Image
import numpy as np
import pandas as pd


def pil_nparr2csv(img_path,resize_h = 30, resize_w = 30):
    img_pil = Image.open(img_path).resize((resize_h,resize_w)).convert('RGB')
    img_nparray = np.asarray(img_pil)

    h,w,_ = img_nparray.shape
    color_flatten_list = []
    #df = pd.DataFrame(img_nparray)
    for img_row in img_nparray:
      for img_row_column in img_row:
        color_v = ""   #merge 3 color channel into RGB order
        for color_c in img_row_column:
          color_v =  color_v + str(hex(color_c)).split('x')[1].upper().zfill(2)
        color_v = '#' + color_v
        color_flatten_list.append(color_v)

    #print(f'H:{h} W:{w}')
    row_order = np.arange(h-1,-1,-1)
    column_order = np.arange(0,w,1)
    row_order_list = np.repeat(row_order,resize_h)
    column_order_list = np.tile(column_order,resize_w)

    df = pd.DataFrame({'row(height)': row_order_list,
                  'column(width)': column_order_list,
                  'color(hex)': color_flatten_list})
    return df


