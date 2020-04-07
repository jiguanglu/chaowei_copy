# -*- coding:utf-8 -*-
#author : jiguanglu
#e-mail : jiguang125@gmail.com


from delaudey_01 import *
from load_json import *
from data2json import *
from create_json import *
import argparse
import json
import time
import warnings
import sys
import os
import requests
import gc
import traceback

def change_json(dis_points,json_ori_path,picId_picUrl, ori_same_points_color):
    # 读取config文件，取出识别后的图片存放的地址，和url访问图片的ip地址
    # cur_points_color = load_cur_color(json_cur_path)

    with open(json_ori_path, 'r', encoding='utf-8') as json_file:
        # 加载json数据
        data1 = json.load(json_file)
        # data1是dict，取出 picContentList
        for k in data1:
            # print(k)
            if k == 'picContentList':
                picContentList = data1[k]
                for j in picContentList:
                    for color_points in ori_same_points_color:
                        if color_points[0] == j['picId']:
                            for i in j['resizePointList']:
                                point = [i['resizePointXmin'], i['resizePointYmin']]

                                for color_point in color_points[1]:
                                    if color_point[0] == point:
                                        i['rightColorName'] = color_point[1]
                    for pic in dis_points:
                        # print('dis_points ================',dis_points)
                        if pic[0] == j['picId']:
                            # print('pic =========',pic[0])
                            for picid_picurl in picId_picUrl:
                                if picid_picurl[0]==j['picId']:
                                    j['picUrl'] = picid_picurl[1]
                            for i in j['resizePointList']:
                                # print([i['resizePointXmin'], i['resizePointYmin']])
                                point = [i['resizePointXmin'], i['resizePointYmin']]
                                # print('pic[1]===',pic[1])
                                if pic[1] != 'no points find':
                                    if point in pic[1]:
                                        # print(point)
                                        i['rightColorName'] = ''
                                        i['rightColorCode'] = ''


    json_file.close()                                     
    return data1


def rewrite_json_file(filepath, json_data):
    # with open(filepath, 'w') as f:
    #     json.dump(json_data, f)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_data, indent=2, ensure_ascii=False))
    file.close()


def save_compare_json(dis_points, json_output_path,json_ori_path,picId_picUrl,ori_same_points_color):
    change_data = change_json(dis_points,json_ori_path,picId_picUrl,ori_same_points_color)
    rewrite_json_file(json_output_path,change_data)

# change_json('1.json')
# save_compare_json([[686,491]],'1.json','2.json')


class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass



def compare_ori_cur(img_path, json_output_path, compare_json_path):
    # 识别cur_pic-----》保存到json
    recom = data2json(img_path, json_output_path)

    picId_picUrl = []
    with open(json_output_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        for i in json_data:
            if i == 'picContentList':
                pic_list = json_data[i]
                for j in pic_list:
                    url = j['picUrl']
                    pic_id = j['picId']
                    picId_picUrl.append([pic_id,url])
    # print(picId_picUrl)
    # 当compare_json_path 存在的时候，进行对比，当其不存在的时候，直接返回空。
    if compare_json_path and recom != 'no pictures find':
        ori_points = load_json(compare_json_path)
        cur_points = load_json(json_output_path)
        # print('ori_points ===', ori_points)

        '返回颜色'
        cur_points_color = load_json_color(json_output_path)
        dis_points = []
        ori_same_color = []
        # 因为检测的是同一个机柜，机柜里的照片是一样的，根据dict里的pic_id比对
        for pic_id in ori_points:

            # print(ori_points[pic_id])
            # print(cur_points[pic_id])
            if pic_id in cur_points_color:
                cur_color = cur_points_color[pic_id]
                # print('cur_color ========',cur_color)
                ori_points_ = ori_points[pic_id]
                cur_points_ = cur_points[pic_id]
                
                
                #print(type(ori_points))
                #print(type(cur_points))


                # print('pic_id ===', [pic_id,ori_points_])
                if len(cur_points_) >= 3:

                    "对points进行排序，以防止比对错误例如 [1,2,3,4,5]   [5,2,6,1]"

                    ori_points_.sort()
                    cur_points_.sort()
                    test_ori_angle = all_points_angles_ratio(ori_points_)
                    test_cur_angle = all_points_angles_ratio(cur_points_)

                   # "画出plot图，可以直观的看到消失的点"

                    # ori_plot = draw_plot(ori_points_, 'ori_pic: ' + pic_id)
                    # cur_plot = draw_plot(cur_points_, 'cur_pic: ' + pic_id)

                    result = compare_all_points(test_ori_angle,test_cur_angle, ori_points_, cur_points_, cur_color)

                    if result != -1:


                           # "((694, 391, 698, 502, 970, 392), [70.04, 2.641535411395946])， 中间的点就是inner_point"
                            dis_points.append([pic_id,result[0]])
                            ori_same_color.append([pic_id,result[1]])
                            print('图%s所有消失的点的坐标为 ====='%pic_id, result[0])
                            # print('图%s所有相同的点的坐标颜色 ====='%pic_id, result[1])
                elif len(cur_points_) == 0:
                    print('开始比对=====================================================================================================')
                    dis_points.append([pic_id,ori_points_])
                    # dis_points.append(ori_points_)
                    ori_same_color.append([pic_id, ''])
                    # print(dis_points)
                    print('图%s所有点都消失了～～～～～～～～～～～～～～～～～～～～～～～～～～～' % pic_id)
                    # print('cur dis points==',dis_points)
                else:
                    result = compare_less_points(ori_points_, cur_points_, cur_color)
                    dis_points.append([pic_id, result[0]])
                    ori_same_color.append([pic_id, result[1]])
                    print('图%s所有消失的点的坐标为 =====' % pic_id, result[0])
            else:
                ori_points_ = ori_points[pic_id]
                # cur_points_ = cur_points[pic_id]
                print('开始比对=====================================================================================================')
                dis_points.append([pic_id, ori_points_])
                # dis_points.append(ori_points_)
                ori_same_color.append([pic_id, ''])
                # print(dis_points)
                print('图%s不存在～～～～～～～～～～～～～～～～～～～～～～～～～～～' % pic_id)
                    # print(result)
                # print('ori_same_color======',ori_same_color)
        save_compare_json(dis_points, json_output_path, compare_json_path,picId_picUrl,ori_same_color)
        return dis_points
    elif recom == 'no pictures find':
        return 'no pictures find'
    else:
        return 'This is the first time to check'




def post_requests(ErrorNo,Message,IsNormal,JsonPath):
    # url="http://192.168.216.180:8080/api/resizeResult"
    url = 'http://10.7.6.144:8080/api/resizeResult'
    #url = 'http://192.168.216.62:8001/api/recognition'
    payload={
        "ErrorNo": ErrorNo,
        "Message": Message,
        "IsNormal": IsNormal,
        "DataUrl": JsonPath
    }
    try:
        r = requests.post(url, timeout=5, json=payload)
        print(r.status_code)
        print(r.content)
        print(r.text)
        print('success')
    except requests.exceptions.RequestException as e:
        print(e)



if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    start = time.clock()
    #打印日志
    sys.stdout = Logger("/home/dcm360/object-detection/log/%starget_file.txt"%start)
   # sys.stdout = Logger("/home/dcm360/object-detection/log/log_file.txt")



    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="image path")
    parser.add_argument("jop", help="json output path")
    parser.add_argument("--cjp", help="compare_json_path")
    args = parser.parse_args()

    img_path = args.ip
    cur_json_path = args.jop
    compare_json_path = args.cjp
    # is_normal = True
    # errorno = -1
    # message = ''
    # data_url = 'http://10.7.6.144:8080/ResizePic/resize_data.json'


    #dis = compare_ori_cur(img_path, cur_json_path, compare_json_path)
    # """
    print('开始识别')

    if compare_json_path:
        JsonPath = 'http://10.7.6.1:8081/static/recognize/original/resize_json/resize.json'
    else:
        JsonPath = 'http://10.7.6.1:8081/static/recognize/original/normal_json/normal.json'

    print(JsonPath)
    try:
        dis = compare_ori_cur(img_path,cur_json_path, compare_json_path)
        if dis == 'This is the first time to check':
            print('第一次拍摄基准照，并返回结果到json')
            # message = '第一次拍摄基准照，并返回结果到json'
            post_requests(0,'First time check success',1,JsonPath)
            # if time.sleep(3):
        elif dis == 'no pictures find':
            print('没有找到图片')
            JsonPath = ''
            # message = 'no pictures find'
            post_requests(-1, 'No pictures find', -1,JsonPath)
        elif len(dis)!=0:
            # message = '一些点消失了'
            print('一些点消失了')
            post_requests(0, 'Compare  success', 0,JsonPath)
    except Exception:
        print('没有识别成功')
        f = open('/home/dcm360/object-detection/log/error_%starget_file.txt'%start, 'w+')
       # f = open('/home/dcm360/object-detection/log/error_log_file.txt', 'w+')
        f.writelines(str(traceback.format_exc()))
        f.close()
        JsonPath = ''
        message = '没有识别成功'
        post_requests(-1,'Recognition fails',-1,JsonPath)
    # """
    end = time.clock()
    print('Running time: %s Seconds' % (end - start))





