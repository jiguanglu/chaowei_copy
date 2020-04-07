# -*- coding:utf-8 -*-
#author : jiguanglu
#e-mail : jiguang125@gmail.com
#date   : 2020-03-1314:12

import requests


# 定义一个函数 测试一个服务接口
def test_everything():

    # 构造服务接口地址
    # url = 'http://localhost:{0}/'.format(5001)
    #url = 'http://127.0.0.2:{0}/'.format(8888)
    #url = 'http://127.0.0.1:{0}/'.format(5000)

    # 构造请求体 请求体将被转换为 JSON 格式
    request_body = {"PicPath": "/home/dcm360/object-detection/ori",
                    "IsNormal":"true",
                    "CabinetInfo":"H0102",
                    "TimeStamp" : 123456789}
   # 向指定服务接口发送 POST 请求
    r0 = requests.post(url="http://0.0.0.0:8888/flask_server",json=request_body)

    # 解析 JSON 格式的响应体 并打印
    print('Response info:', r0.json())


if __name__ == '__main__':

    test_everything()

