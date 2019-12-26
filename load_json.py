from create_json import *
import json




# 加载json数据，并生成{picId : pointsList}
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        #加载json数据
        data1 = json.load(json_file)
        # data1是dict，取出 picContentList
        pic_dict = {}
        for k in data1:

            if k == 'picContentList':
                picContentList = data1[k]
                cabinetId = data1['cabinetId']
                #创建一个空字典，以后存储图片id和其对应的图片中的点的坐标

                for i in picContentList:
                    picId = i['picId']
                    # print(picId)
                    points = []
                    for j in i['resizePointList']:
                        points.append([j['resizePointXmin'], j['resizePointYmin']])
                    pic_dict[picId] = points
        return pic_dict


def load_json_color(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        #加载json数据
        data1 = json.load(json_file)
        # data1是dict，取出 picContentList
        pic_dict = {}
        for k in data1:

            if k == 'picContentList':
                picContentList = data1[k]
                #创建一个空字典，以后存储图片id和其对应的图片中的点的坐标

                for i in picContentList:
                    picId = i['picId']
                    # print(picId)
                    points = []
                    for j in i['resizePointList']:
                        points.append([j['resizePointXmin'], j['resizePointYmin'] ,j['rightColorName']])
                    pic_dict[picId] = points
        return pic_dict
