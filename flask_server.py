# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
import json
from gevent import pywsgi
import time
import sys
from threading import Thread
from start_recognize import *
import os,stat
from download_json import *


# 创建一个服务
app = Flask(__name__)


# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route(rule='/flask_server', methods=['POST', 'GET'])
def everything():
    ex_python = 'python3'
    # script_path = '/Users/jiguang/my_disk/keras-yolo3-master/my_folder/chaowei/compare_ori_cur.py'
    script_path = '/home/dcm360/object-detection/compare_ori_cur.py'

    # 获取 JSON 格式的请求体 并解析
    if request.method == 'POST':
        # request_body = request.get_json()
        request_body = request.get_data()
        request_body = json.loads(request_body.decode('utf-8'))
        print('Request info: ', request_body)
        PicPath = request_body.get("PicPath")
        IsNormal = request_body.get("IsNormal")

        TimeStamp = request_body.get("TimeStamp")
        localTime = time.localtime(int(TimeStamp))
        takePhotoTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        print(takePhotoTime)

        # CabinetInfo = request_body.get('CabinetInfo')
        
        # 这里需要加上检测路径，文件存与否，时间紧急，以后加上
        compare_json_path = '/var/www/html/static/recognize/original/resize_json/resize.json'

        th_1 = Thread(target=run_download_json,args=(),daemon=False)
        th_1.start()
        th_1.join()

        #cur_json_path = 'http://10.7.6.1:8081/original/recognize_img/normal_json/normal.json'
        cur_json_path = '/var/www/html/static/recognize/original/normal_json/normal.json'
        th_2 = Thread(target=start_recognize, args=(IsNormal,ex_python, script_path, PicPath, cur_json_path, compare_json_path), daemon=False)
        th_2.start()

        response_info = {"ErrorNo": 0, "Message": 'Parameters received successfully'}
        # print('Response info:', response_info)

        # 将响应信息转换为 JSON 格式
        response_body = jsonify(response_info)
        return response_body

    else:
        return 'Receive post requests onl！'
    # 最终对请求进行相应
    # return response_body


if __name__ == '__main__':
#def run_server():
    try:
        app.run(host='0.0.0.0', port=8888, debug=True)
        #server = pywsgi.WSGIServer(('0.0.0.0', 8888), app)
        #server.serve_forever()
        print(sys.path)
    except Exception:
        print('服务器没开启')
