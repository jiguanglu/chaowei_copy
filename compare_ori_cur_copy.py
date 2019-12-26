###  load基准库的点的坐标， load 图像识别后点的坐标， 并进行比较
from delaudey_01 import *
from load_json import *
from data2json import *
from create_json import *
import argparse
import json
import time
import warnings




"把比对后的结果放到基准库的json文件中，消失的点颜色变成''，输出的pic_url变成识别后的图片存放路径，而且名字一定要对上"
def change_json(dis_points,json_ori_path,picId_picUrl):
    # 读取config文件，取出识别后的图片存放的地址，和url访问图片的ip地址

    with open(json_ori_path, 'r', encoding='utf-8') as json_file:
        # 加载json数据
        data1 = json.load(json_file)
        # data1是dict，取出 picContentList
        for k in data1:
            if k == 'picContentList':
                picContentList = data1[k]
                for j in picContentList:
                    for pic in dis_points:
                        if pic[0] == j['picId']:
                            for picid_picurl in picId_picUrl:
                                if picid_picurl[0]==j['picId']:
                                    j['picUrl'] = picid_picurl[1]
                            for i in j['resizePointList']:
                                point = [i['resizePointXmin'], i['resizePointYmin']]
                                if pic[1] != 'no points find':
                                    if point in pic[1]:
                                        i['rightColorName'] = ''
                                        i['rightColorCode'] = ''

    json_file.close()
    return data1


def rewrite_json_file(filepath, json_data):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_data, indent=2, ensure_ascii=False))
    file.close()


def save_compare_json(dis_points, json_output_path,json_ori_path,picId_picUrl):
    change_data = change_json(dis_points,json_ori_path,picId_picUrl)
    rewrite_json_file(json_output_path,change_data)


def compare_ori_cur(img_path, json_output_path, compare_json_path):
    # 识别-保存到json
    data2json(img_path, json_output_path)

    picId_picUrl = []
    pics_index = []
    with open(json_output_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        for i in json_data:
            if i == 'picContentList':
                pic_list = json_data[i]
                for j in pic_list:
                    url = j['picUrl']
                    pic_id = j['picId']
                    pic_index = j['picIndex']
                    picId_picUrl.append([pic_id,url])
    # 当compare_json_path 存在的时候，进行对比，当其不存在的时候，直接返回空。
    if compare_json_path:
        ori_points = load_json(compare_json_path)
        cur_points = load_json(json_output_path)
        dis_points = []
        # 因为检测的是同一个机柜，机柜里的照片是一样的，根据dict里的pic_id比对
        for pic_id in ori_points:
            ori_points_ = ori_points[pic_id]
            cur_points_ = cur_points[pic_id]
            ori_angles = return_angles(ori_points_, 'ori_pic: '+pic_id)
            cur_angles = return_angles(cur_points_,'cur_pic: '+pic_id)
            if ori_angles != 'n_points<3' and cur_angles != 'n_points<3':


                compar_v = compare_v_angles(ori_angles, cur_angles)
                if compar_v != 'not points find':

                    dis_point = compare_inner_angles(compar_v, ori_angles, cur_angles)

                    "((694, 391, 698, 502, 970, 392), [70.04, 2.641535411395946])， 中间的点就是inner_point"
                    dis_points.append([pic_id,dis_point])
                    print('图%s所有消失的点的坐标为 ====='%pic_id, dis_point)

        save_compare_json(dis_points, json_output_path, compare_json_path,picId_picUrl)
        return dis_points

    else:
        print('This is the first time to check')


#
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
