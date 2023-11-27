# -*- encoding=utf8 -*-
__author__ = "zyh"

import site
import os

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
        # devices = self.adb.devices()[0][0]                  #获取device
        # print("\n\t本机的设备是 %s" % devices)
        self.dev = air_api.connect_device("android:///127.0.0.1:62001")  #连接到device
        self.poco = AndroidUiautomationPoco(self.dev, use_airtest_input=True, screenshot_each_action=False)
        xy = self.poco.get_screen_size()
        self.x = xy[0]
        self.y = xy[1]
        

    def operator(self):
        self = phone()
        self.connect()
        # sop_msg = self.poco(name='com.tencent.wework:id/gb8')
        # sop = []
        # for i in sop_msg:
        #     sop.append(i)
        # for i in sop_msg[::-1]:
        #     print(type(i))

        # print(len(sop_msg[::-1]))
        # for i in sop:
        #     print(i)
        #     print(type(i))

        # ROAMING_PATH = os.getenv("APPDATA")
        # DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
        # UI_PATH = os.path.join(DATA_PATH, "ui")
        # s_time = datetime.now()
        # adb_path = site.getsitepackages()[1] + r'\airtest\core\android\static\adb\windows\adb.exe'
        # self.dev.shell("/system/bin/screencap -p /sdcard/screenshot.png")
        # os.system(f'{adb_path} pull /sdcard/screenshot.png {UI_PATH}\\SCREENSHOT.png')
        # e_time = datetime.now()
        # print((e_time-s_time).total_seconds())

        # self.dev.shell("pull /sdcard/screenshot.png F:\\mvp")
        # freeze_poco = self.poco.freeze()
        # print('2')
        # #sop pyq
        # a = freeze_poco(name='com.tencent.wework:id/cfo')
        # for i in a:
        #     for x in i.child():
        #         print(x.get_name())
        
        # b = freeze_poco(text='名片用户').exists()
        # print(b)

        # group send 1v1
        # a = freeze_poco(name='com.tencent.wework:id/g16')
        # for i in a:
        #     print(i)


        # self.poco.post_action(action='click',ui=back,args=pos_in_percentage)

        # self.adb.start_server()
        # self.adb.kill_server()

        # self.dev.unlock()   #解锁手机
        
        print(self.dev.get_top_activity())  #获取当前屏幕的包、activity

        print(self.dev.get_top_activity_name())  #获取当前屏幕的包、activity

        # print(self.dev.list_app())    #查询该设备所有的应用包

        # print(self.dev.check_app('com.tencent.wework')) #查询包的存在性

        # self.dev.start_app('com.tencent.wework') #打开对应的包/活动

        # print(self.poco.agent.hierarchy.dump())   #打印Ui树

        # get children
        # child = self.poco(name='com.tencent.wework:id/v7').child()
        # for x in child:
        #     print(x.attr('name'))

        # get descendants
        # child = self.poco(name='com.tencent.wework:id/v7').offspring(name='com.tencent.wework:id/ftj')
        # for x in child:
        #     print(x.attr('text'))

        # text = self.poco(name='com.tencent.wework:id/gft').get_text()
        # time = text.split('\n')[0] + text.split('\n')[3].split(':')[0][-2:] + ':' + text.split('\n')[3].split(':')[1][0:2:1]
        # time = datetime.strptime(time,'%Y年%m月%d日%H:%M')
        # print(time)

        # yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y年%m月%d日') + '22:00'
        # yesterday_str = datetime.strptime(yesterday_str,'%Y年%m月%d日%H:%M')
        # print(yesterday_str)

        # print(yesterday_str > time)
        # if not(yesterday_str > time):
        #     print('no')
        pass
    
    def test(self):
        '''
        '''
        pass


if __name__ == "__main__":
    r = phone()
    print("start...")
    r.operator()










