#-----------------------------------------------------------------------#
#   predict.py将单张图片预测、摄像头检测、FPS测试和目录遍历检测等功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#-----------------------------------------------------------------------#
import time

import cv2
import os
import json
import numpy as np
from PIL import Image

from yolo import YOLO

if __name__ == "__main__":
    yolo = YOLO()
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'dir_predict'表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #----------------------------------------------------------------------------------------------------------#
    mode = "dir_predict"

    #-------------------------------------------------------------------------#
    #   dir_origin_path指定了用于检测的图片的文件夹路径
    #   dir_save_path指定了检测完图片的保存路径
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    
    predict_filename="20190925_124000_1_4"
    dir_save_path   = "img_out/"
    
    
    result_path="../DataBase/UAV_data/result"
    dir_origin_path = "../DataBase/UAV_data/test"
    

    if mode == "predict":
        '''
        1、如果想要进行检测完的图片的保存，利用r_image.save("img.jpg")即可保存，直接在predict.py里进行修改即可。 
        2、如果想要获得预测框的坐标，可以进入yolo.detect_image函数，在绘图部分读取top，left，bottom，right这四个值。
        3、如果想要利用预测框截取下目标，可以进入yolo.detect_image函数，在绘图部分利用获取到的top，left，bottom，right这四个值
        在原图上利用矩阵的方式进行截取。
        4、如果想要在预测图上写额外的字，比如检测到的特定目标的数量，可以进入yolo.detect_image函数，在绘图部分对predicted_class进行判断，
        比如判断if predicted_class == 'car': 即可判断当前目标是否为车，然后记录数量即可。利用draw.text即可写字。
        '''
        result_list={
            "res":[]
        }

        
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image, result_list)
                r_image.show()
                
            
            if not os.path.exists(result_path):
                os.mkdir(result_path)

            print(result_list)
            str=json.dumps(result_list)
            result_file=open(result_path+'/'+predict_filename+'.txt','w')
            result_file.write(str)
            result_file.close()
            
             



    elif mode == "dir_predict":
        import os

        from tqdm import tqdm
        
        filenames=os.listdir(dir_origin_path)
        for file in filenames:
            predict_path=os.path.join(dir_origin_path,file)

            img_names = os.listdir(predict_path)
        
            result_list={
                "res":[]
            }
        
            for img_name in tqdm(img_names):
                if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    image_path  = os.path.join(predict_path, img_name)
                    image       = Image.open(image_path)
                    r_image     = yolo.detect_image(image, result_list)
                    #if not os.path.exists(dir_save_path):
                    #    os.makedirs(dir_save_path)
                    #r_image.save(os.path.join(dir_save_path, img_name))
        
            
            if not os.path.exists(result_path):
                os.mkdir(result_path)
        
            result_file=open(os.path.join(result_path,"%s.txt"%(file)),'w')
            result_file.write(json.dumps(result_list))
            result_file.close()
            print("Generate "+result_path+"/"+file+".txt Done!")        
    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
