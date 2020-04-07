# -*- coding:utf-8 -*-
#author : jiguanglu
#e-mail : jiguang125@gmail.com

from create_json import *
import json
#from opencv_darknet01 import *
from darknet import *
import os
from configparser import ConfigParser



"因为同一机柜下的图片的 点位-相机-丝杠 是不变的，" \
"所以根据下面的函数来实现图片的排列，输入参数是图片的name，输出是可以对图片排序的index"
def create_pic_index(pic_name):
    camera_id = int(pic_name.split('_')[1])
    slider_id = int(pic_name.split('_')[2])
    if camera_id == 0:
        if slider_id == 0:
            return 1
        elif slider_id == 1:
            return 4
        elif slider_id == 2:
            return 7
    elif camera_id == 1:
        if slider_id == 0:
            return 2
        elif slider_id == 1:
            return 5
        elif slider_id == 2:
            return 8
    elif camera_id == 2:
        if slider_id == 0:
            return 3
        elif slider_id == 1:
            return 6
        elif slider_id == 2:
            return 9

"图像识别，并把点坐标放在json中,把颜色也存在json中"
def data2json(img_path,json_output_path):
    # 读取config文件，取出识别后的图片存放的地址，和url访问图片的ip地址
    cfg = ConfigParser()
    # 修改为tx的配置文件地址
    cfg.read('/home/dcm360/jetsontx2/src/task_center/config/config.ini')
    url = 'http://'+cfg.get('publish', 'host')
    recognize_img_path = cfg.get('publish', 'publish_path')

    def get_img_file(file_name):
        imagelist = []
        for parent, dirnames, filenames in os.walk(file_name):
            for filename in filenames:
                if filename.lower().endswith(
                        ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    imagelist.append(os.path.join(parent, filename))
            return imagelist
    imagelist = get_img_file(img_path)

    # print(imagelist)

    darknet_out = output_points(img_path)
    # darknet_out = output_points(imagelist)
    k = 0
    if len(imagelist) !=0:
        picContentList = []

        for i in imagelist:
            output = []
            str1 = recognize_img_path.replace('/var/www/html', '')
            k = k + 1
            for j in darknet_out:
                #print(j)
                #if j[0] == i.split("/")[-1][0:5]:
                if j[0] == i.split("/")[-1][3:8]:
                    # print(j[0])
                    output.append([j[1],j[2]])
            # print(output)
            # darknet_out = output


            points = output[0][0]
            # if len(points)>0:
                # print(points)
                # 生成pic的ID，以后需要修改
            pic_id = (i.split('/')[-1]).split('_')[0:-1]
            #pic_id 是图片命名的前三位  巡检定位_摄影头_丝杆位置点_拍照时间.png
            pic_id = pic_id[0] + '_' + pic_id[1] + '_' + pic_id[2]
            # label_names = darknet_out[1]
            label_names = output[0][1]

            # pic_name = i.split('/')[-1].split('.')[0]+'.png'
            pic_name = i.split('/')[-1]
            pic_index = create_pic_index(pic_name)
            # print('pic_index = ', pic_index)
            resizePointList = []
            pointCount = len(points)
            # print(points[1])
            for j in range(pointCount):
                # print(label_names[j])
                resizePointList.append(ResizePointList(pointCreateTime=1, resizePointCreateTime=0, resizePointForword=False,resizePointHeight=30,
                                                       resizePointId=pic_id+'_'+str(j), resizePointName='sa',resizePointWidth=20,
                                                       resizePointXmin=int(points[j][0]), resizePointYmin=int(points[j][1]), rightColorCode=label_names[j],
                                                       rightColorName=label_names[j]))
            picContentList.append(PicContentList(innerPointCount=6, innerTopDegreeName='sas', picId=pic_id, picIndex= pic_index, picUrl=url+str1+'original/recognize_img/'+pic_name,
                                            pointCount=pointCount, resizePointList=resizePointList,sideScal = 0.0,topPointCount=1, topTopDegreeName='dsad'))


                #
        article_info = ori_info(cabinetId='21', cabinetName='first', picContentList=picContentList, resizePointCreateTime = 12, resizePointId = '2', resizePointName = 'ada')
        json_str = json.dumps(article_info, default=lambda o: o.__dict__, sort_keys=True, indent=4)


        print('pic_path ==========', url+str1+'original/recognize_img/'+pic_name)
        print(json_str)
        
        data = json.loads(json_str)
        with open(json_output_path,'w',encoding='utf-8') as file:
            file.write(json.dumps(data,indent=2,ensure_ascii=False))
    else:
        return 'no pictures find'


