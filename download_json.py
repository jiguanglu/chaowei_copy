#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Time    : 2020-03-26 16:39
# @Author  : jiguang

import os
# from urllib import request
import urllib.request as ur


def download_json(json_url,file_name):
    takePhotoTime = '2020-03-25'
    localTime = str(123456789)
    CabinetInfo = 'H0102'

    # file_path = '/Users/jiguang/my_disk/keras-yolo3-master/my_folder/'+takePhotoTime+'/'+localTime+'_'+CabinetInfo+'/'
    # file_path = '/Users/jiguang/my_disk/keras-yolo3-master/my_folder/json/'
    file_path = '/var/www/html/static/recognize/original/resize_json'
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 文件夹
    try:
        if not os.path.exists(file_path):
            print('文件夹',file_path,'不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        #获得json后缀
        file_suffix = os.path.splitext(json_url)[1]
        print('file_suffix:  ',file_suffix)
        #拼接json名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
        # print('file_name: ',filename)
        #下载json文件，并保存到文件夹中
        ur.urlretrieve(json_url,filename=filename)
        return filename
    except IOError as e:
        print('文件操作失败',e)
    except Exception as e:
        print('错误 ：',e)

#if __name__ == '__main__':
# def run_download_json(takePhotoTime,localTime,CabinetInfo):
def run_download_json():
    json_url = 'http://192.168.113.233:8080/ResizePic/NormalJson/normal_tx2.json'
    file_name = download_json(json_url,'resize')
    print(file_name)
    # return file_name
