# -*- encoding=utf8 -*-
__author__ = "zyh"

from re import T
import site
import os
from time import sleep

from airtest.core.android.adb import ADB
from airtest.core import api as air_api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from logging import Logger
from datetime import datetime,timedelta
import multiprocessing


class phone():
    def __init__(self):
        self.dev = None
        self.poco = None
        self.adb = None

    def connect(self):
        '''
        connect and init dev/poco
        '''
        self.adb = ADB()
        self.adb.kill_server()
        for i in range(0,10):
            a = 62001
            if i >= 1:
                a = i + 62024
            try:
                self.dev = air_api.connect_device(f"android:///127.0.0.1:{a}")  #连接到device
            except:
                break
        devices = self.adb.devices()               #获取device
        devices_list = []
        for i in devices:
            if i[1] == 'device':
                devices_list.append(i[0])
        print(f"\n\t本机的设备有{len(devices_list)}个,分别是{devices_list}")
        q = multiprocessing.Queue()
        try:
            for i in range(len(devices_list)):
                dev = devices_list[i]
                p = multiprocessing.Process(target=self.operator, name='mrpa', args=(q,dev,))
                p.daemon = True  # 解决点击右上角关闭界面但子线程仍在运行
                p.start()
            p.join()
        except Exception as e:
            print(f'出现了错误:{e}')

    @staticmethod
    def operator(q,dev):
        print(f'—— 正在运行设备{dev}的RPA进程 ——')
        r = phone()
        r.connect_target(dev)
        print(f'—— 设备{dev}的RPA进程运行完毕！ ——')

    def connect_target(self,dev):
        print(f'***************任务运行中**************')
        while True:
            try:
                self.dev = air_api.connect_device(f"android:///{dev}")
                self.poco = AndroidUiautomationPoco(self.dev, use_airtest_input=True, screenshot_each_action=False)
                xy = self.poco.get_screen_size()
                self.x = xy[0]
                self.y = xy[1]
                # for test
                self.dev.start_app('com.tencent.wework')
                print(self.poco.agent.hierarchy.dump())   #打印Ui树
                print(f'设备信息:{self.dev},{self.x}x{self.y}')
                self.dev.home()
                break
            except Exception as e:
                print(f'{dev}设备连接出错：{e}')
        print(f'***************任务运行成功**************')

if __name__ == "__main__":
    multiprocessing.freeze_support()
    print("start...")
    for i in range(200):
        r = phone()
        r.connect()











