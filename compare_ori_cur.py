###  load基准库的点的坐标， load 图像识别后点的坐标， 并进行比较
from delaudey_01 import *
from load_json import *
from data2json import *
from create_json import *
import argparse
import json
import time
import warnings



# "读取当前指示灯的颜色"
# def load_cur_color(json_cur_path):
#     cur_points_color = {}
#     with open(json_cur_path, 'r', encoding='utf-8') as json_file:
#         cur_data = json.load(json_file)
#
#         for k in cur_data:
#             if k == 'picContentList':
#                 picContentList = cur_data[k]
#                 for j in picContentList:
#                     for point in j['resizePointList']:
#                         cur_points_color[point['resizePointId']] = point['rightColorName']
#     return cur_points_color


"把比对后的结果放到基准库的json文件中，消失的点颜色变成''，输出的pic_url变成识别后的图片存放路径，而且名字一定要对上"
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

def compare_ori_cur(img_path, json_output_path, compare_json_path):
    # 识别-保存到json
    data2json(img_path, json_output_path)

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
    if compare_json_path:
        ori_points = load_json(compare_json_path)
        cur_points = load_json(json_output_path)

        '返回颜色'
        cur_points_color = load_json_color(json_output_path)
        # print(ori_points)
        # print(cur_points_color)
        # for i in range(len(ori_points)):
        #     print(ori_points)
        dis_points = []
        ori_same_color = []
        # 因为检测的是同一个机柜，机柜里的照片是一样的，根据dict里的pic_id比对
        for pic_id in ori_points:
            # print(ori_points[pic_id])
            # print(cur_points[pic_id])
            cur_color = cur_points_color[pic_id]
            # print('cur_color ========',cur_color)
            ori_points_ = ori_points[pic_id]
            cur_points_ = cur_points[pic_id]
            ori_angles = return_angles(ori_points_, 'ori_pic: '+pic_id)
            cur_angles = return_angles(cur_points_,'cur_pic: '+pic_id)
            # if ori_angles != 'n_points<3' and cur_angles != 'n_points<3':

            compar_v = compare_v_angles(ori_angles, cur_angles,cur_color)
            if compar_v != -1:


                    "((694, 391, 698, 502, 970, 392), [70.04, 2.641535411395946])， 中间的点就是inner_point"
                    dis_points.append([pic_id,compar_v[0]])
                    ori_same_color.append([pic_id,compar_v[1]])
                    print('图%s所有消失的点的坐标为 ====='%pic_id, compar_v[0])
                    print('图%s所有相同的点的坐标为 ====='%pic_id, compar_v[1])

        # print('ori_same_color======',ori_same_color)
        save_compare_json(dis_points, json_output_path, compare_json_path,picId_picUrl,ori_same_color)

    else:
        print('This is the first time to check')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    start = time.clock()
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="image path")
    parser.add_argument("jop", help="json output path")
    parser.add_argument("--cjp", help="compare_json_path")
    args = parser.parse_args()

    img_path = args.ip
    cur_json_path = args.jop
    compare_json_path = args.cjp

    dis = compare_ori_cur(img_path,cur_json_path, compare_json_path)

    end = time.clock()
    print('Running time: %s Seconds' % (end - start))
