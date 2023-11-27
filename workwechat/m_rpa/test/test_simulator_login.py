# -*- encoding=utf8 -*-
__author__ = "zyh"

import site
import os
import sys
from time import sleep

from airtest.core.android.adb import ADB
from airtest.core import api as air_api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from logging import Logger
from datetime import datetime,timedelta


class phone():
    def __init__(self):
        # log = Logger(level='debug')
        # self.log = log.logger
        self.dev = None
        self.poco = None
        self.adb = None

    def connect(self):
        '''
        connect and init dev/poco
        '''
        self.adb = ADB()
        self.adb.start_server()
        self.dev = air_api.connect_device("android:///127.0.0.1:21503")  #连接到逍遥模拟器:21503-21513-21523/夜神:62001-62025-62026/mumu:7555
        self.poco = AndroidUiautomationPoco(self.dev, use_airtest_input=True, screenshot_each_action=False)
        xy = self.poco.get_screen_size()
        self.x = xy[0]
        self.y = xy[1]
        

    def operator(self):
        self = phone()
        self.connect()
        # 打开企微
        self.dev.start_app('com.tencent.wework')

        while True:
            try:
                self.poco(text='手机号登录').wait_for_appearance(timeout=10)
                self.poco(text='手机号登录').click()
                break
            except Exception as e:
                print(f'未找到手机号登录:{e},当前界面是{self.dev.get_top_activity()}')
                self.dev.stop_app('com.tencent.wework')
                self.dev.start_app('com.tencent.wework')

        try:
            self.poco(text='同意').wait_for_appearance(timeout=5)
            while True:
                try:
                    self.poco(text='同意').click()
                    self.poco(text='同意').wait_for_disappearance(timeout=5)
                    break
                except Exception as e:
                    print(f'点击同意失败:{e}')
        except Exception as e:
            print(f'未弹出勾选用户协议:{e}')

        while True:
            try:
                self.poco(text='下一步').wait_for_appearance(timeout=5)
                self.dev.text('18101830253',enter=False)
                self.poco(text='18101830253').wait_for_appearance(timeout=5)
                self.poco(text='下一步').click()                # 可能会出现手机号错误的情况
                sleep(1)
                if self.poco(text='请输入验证码').exists():
                    break
                else:
                    print(f'手机号输入错误,当前页面是{self.dev.get_top_activity()}')
                    if self.poco(text='18101830253').exists:
                        self.poco(text='18101830253').long_click(duration=2.0)
                    return 1
            except Exception as e:
                print(f'未到输入手机号页面:{e},当前页面是{self.dev.get_top_activity()}')

        try:
            self.poco(text='请输入验证码').wait_for_appearance(timeout=5)
            print('请输入获取到的验证码:')
            pin = sys.stdin.readline().strip()
            self.dev.text(pin,enter=False)
            self.poco(text='下一步').click()                #可能会出现验证码输入错误的情况
        except Exception as e:
            print(f'未到输入验证码页面:{e},当前页面是{self.dev.get_top_activity()}')

        try:
            self.poco(text='上海心莲信息科技有限公司').wait_for_appearance(timeout=10)
            while True:
                try:
                    self.poco(text='上海心莲信息科技有限公司').click()
                    break
                except Exception as e:
                    print(f'点击公司失败:{e}')
        except Exception as e:
            print(f'未出现公司选项:{e}')

        try:
            self.poco(text='进入').wait_for_appearance(timeout=10)
            while True:
                try:
                    self.poco(text='进入').click()
                    break
                except Exception as e:
                    print(f'点击进入失败:{e}')
        except Exception as e:
            print(f'未出现进入选项:{e}')
    

    def test(self):
        '''
        '''
        pass


if __name__ == "__main__":
    r = phone()
    print("start...")
    r.operator()










