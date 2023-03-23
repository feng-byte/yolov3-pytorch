import os
import random
import xml.etree.ElementTree as ET

from utils.utils import get_classes

#--------------------------------------------------------------------------------------------------------------------------------#
#   annotation_mode用于指定该文件运行时计算的内容
#   annotation_mode为0代表整个标签处理过程，包括获得VOCdevkit/VOC2007/ImageSets里面的txt以及训练用的2007_train.txt、2007_val.txt
#   annotation_mode为1代表获得VOCdevkit/VOC2007/ImageSets里面的txt
#   annotation_mode为2代表获得训练用的2007_train.txt、2007_val.txt
#--------------------------------------------------------------------------------------------------------------------------------#
annotation_mode     = 0
#-------------------------------------------------------------------#
#   
#   与训练和预测所用的classes_path一致即可
#   仅在annotation_mode为0和2的时候有效
#-------------------------------------------------------------------#
classes_path        = 'model_data/uav_classes.txt'
#--------------------------------------------------------------------------------------------------------------------------------#
#   trainval_percent用于指定(训练集+验证集)与测试集的比例，默认情况下 (训练集+验证集):测试集 = 9:1
#   train_percent用于指定(训练集+验证集)中训练集与验证集的比例，默认情况下 训练集:验证集 = 9:1  
#   仅在annotation_mode为0和1的时候有效
#--------------------------------------------------------------------------------------------------------------------------------#
trainval_percent    = 0.9
train_percent       = 0.9
#-------------------------------------------------------#
#   指向VOC数据集所在的文件夹
#   默认指向根目录下的VOC数据集
#-------------------------------------------------------#


classes, _      = get_classes(classes_path)


UAV_path="../DataBase/UAV_data/train"
UAV_sets=[('train'),('valid')]

train_filename="wg2022_ir_034_split_01"


def convert_annotation(image_id, list_file):
    
    in_file=open(os.path.join(UAV_path,train_filename,'Annotations/%s.xml'%(image_id)))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = 0 
        if obj.find('difficult')!=None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        
if __name__ == "__main__":
    random.seed(0)
    if annotation_mode == 0 or annotation_mode == 1:
        setspath=os.path.join(UAV_path,train_filename,'ImageSets')  #实验,用第一个训练
        if not os.path.exists(setspath):
            os.mkdir(setspath)
            
        print("Generate txt in ImageSets.")
       
        xmlfilepath=os.path.join(UAV_path,train_filename,'Annotations')
        saveBasePath=os.path.join(UAV_path,train_filename,'ImageSets')
        
        temp_xml        = os.listdir(xmlfilepath)
        total_xml       = []
        for xml in temp_xml:
            if xml.endswith(".xml"):
                total_xml.append(xml)

        num     = len(total_xml)  
        list    = range(num)  
        tv      = int(num*trainval_percent)  
        tr      = int(tv*train_percent)  
        trainval= random.sample(list,tv)  
        train   = random.sample(trainval,tr)  
        
        print("train and valid size",tv)
        print("train size",tr)
        ftrainval   = open(os.path.join(saveBasePath,'trainvalid.txt'), 'w')  
        ftest       = open(os.path.join(saveBasePath,'test.txt'), 'w')  
        ftrain      = open(os.path.join(saveBasePath,'train.txt'), 'w')  
        fval        = open(os.path.join(saveBasePath,'valid.txt'), 'w')  
        
        for i in list:  
            name=total_xml[i][:-4]+'\n'  
            if i in trainval:  
                ftrainval.write(name)  
                if i in train:  
                    ftrain.write(name)  
                else:  
                    fval.write(name)  
            else:  
                ftest.write(name)  
        
        ftrainval.close()  
        ftrain.close()  
        fval.close()  
        ftest.close()
        print("Generate txt in ImageSets done.")

    if annotation_mode == 0 or annotation_mode == 2:
        

        
        
        print("Generate UAV_train.txt and UAV_valid.txt for train.")
        for image_set in UAV_sets:
            image_ids=open(os.path.join(UAV_path,train_filename,'ImageSets','%s.txt'%(image_set))).read().strip().split()
            list_file=open('%s_%s.txt'%(train_filename,image_set),'w')
            for image_id in image_ids:
                list_file.write('%s/%s/%s.jpg'%(os.path.abspath(UAV_path),train_filename,image_id))
                convert_annotation(image_id, list_file)
                list_file.write('\n')
            list_file.close()
        print("Generate UAV_train.txt and UAV_val.txt for train done.")
        