import os
import re
import numpy as np
from PIL import Image

path="../DataBase/UAV_data/train"
train_filename="wg2022_ir_034_split_01"



def j2voc(data_num):
    filenames=os.listdir(path)
    cur_path=os.path.join(path,filenames[data_num])
    json_path=os.path.join(cur_path,'IR_label.json')
    with open(json_path) as f:
        lines=f.readlines()
        split_list=re.split('[:]',str(lines))
        labels=split_list[1][2:-12]
        labels.replace(" ","")
        labels=re.split('[,]',labels)
        labels=np.array(labels,dtype=np.int32)
        
        rects=split_list[2][2:-4]
        pattern=re.compile(r'(\[[^\]]+\])')
        rects=re.findall(pattern,rects)        #将四维坐标分割
        for i in range(len(rects)):
            rects[i]=rects[i][1:-1].split(',') #去除[]后分割
        
        rects=np.array(rects,dtype=np.int32)
        f.close()
        
    #创建Annotations文件夹
    xml_path=os.path.join(cur_path,'Annotations')
    if not os.path.exists(xml_path):
        os.mkdir(xml_path)
        
    jpglist=os.listdir(cur_path)
    
    '''
    print(labels.size)
    print(rects.shape)
    print(len(jpglist))
    if len(labels)>len(rects):
        len_l=len(labels)
        len_r=len(rects)
        while len_l!=len_r:
            
            np.r_[rects,np.array([[0,0,0,0]])]
            print(len(rects))
            len_r=len_r+1
    print(rects.shape)
    print(str(rects))
    '''
    
    for jpg in jpglist:
        if not jpg.endswith(".jpg"):
            continue
        im=Image.open(cur_path+'/'+jpg)
        width,height=im.size
        
        image_name=jpg[:-4]  #去除.jpg
        index=int(image_name)-1
        
        xml_file=open(xml_path+'/'+image_name+'.xml','w')
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>UAV_data</folder>\n')
        xml_file.write('    <filename>' + image_name + '.jpg' + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')
        
        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + str(labels[index]) + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(rects[index][0]) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(rects[index][1]) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(rects[index][0]+rects[index][2]) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(rects[index][1]+rects[index][3]) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')
        xml_file.write('</annotation>')
        xml_file.close()
        #print(filenames[data_num]+'/'+image_name+'.xml generate successfully!')


    
        
    
    
if __name__ == "__main__":
    filenames=os.listdir(path)
    index=filenames.index(train_filename)
    print(index)
    j2voc(index)
    
    
    
    #j2voc(8)
    #for i in range(0,len(filenames)):
    #    j2voc(i)
    