# -*- coding:utf-8 -*-
from threading import Thread, Lock
from flask_server import *

def prt():
    print('开始多线程：')



def py_thread():
    th_1 = Thread(target=run_server, args=(), daemon=False)
    th_1.start()


if __name__ == "__main__":
    py_thread()
    print("starting")
