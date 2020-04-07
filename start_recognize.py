#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020-04-02 10:43
# @Author  : jiguang

import os


def start_recognize(IsNormal, ex_python, script_path, PicPath, cur_json_path,compare_json_path):
    args = '--cjp'
    if IsNormal == 'false':
        print('比对开始===================')
        # cur_json_path ='/var/www/static/recognize/original/'+takePhotoTime+'/'+localTime+'_'+CabinetInfo+'/normal.json'
        # compare_json_path = run_download_json(takePhotoTime, localTime, CabinetInfo)
        if compare_json_path != '':
            print('开始比对！！')
            os.system(
                ex_python + ' ' + script_path + ' ' + PicPath + ' ' + cur_json_path + ' ' + args + ' ' + compare_json_path)
            print(
                ex_python + ' ' + script_path + ' ' + PicPath + ' ' + cur_json_path + ' ' + args + ' ' + compare_json_path)

    elif IsNormal == 'true':
        print('识别基准照=================')

        print(ex_python + ' ' + script_path + ' ' + PicPath + ' ' + cur_json_path)
        # 启用另外一个异步
        os.system(ex_python + ' ' + script_path + ' ' + PicPath + ' ' + cur_json_path)
